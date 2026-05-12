from dataclasses import asdict
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from lkb.pipeline import ask_question, index_markdown_dir, rebuild_index
from lkb.store import (
    answer_exists,
    list_bad_answer_logs,
    list_feedback_events,
    log_bad_answer,
    record_feedback_event,
    upsert_feedback,
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)
    threshold: float = Field(default=0.2, ge=0.0, le=1.0)
    retrieval_strategy: Literal["vector_only", "hybrid"] = "hybrid"


class ReindexRequest(BaseModel):
    full_rebuild: bool = False
    chunk_size: int = Field(default=120, ge=20, le=1000)
    overlap: int = Field(default=20, ge=0, le=200)


class FeedbackRequest(BaseModel):
    answer_id: int = Field(ge=1)
    rating: int = Field(ge=-1, le=1)
    comment: str = ""
    question: str = ""
    answer: str = ""
    retrieved_chunks: list[dict] = Field(default_factory=list)


def _serialize_chunk(row) -> dict:
    return {
        "chunk_id": row.chunk.chunk_id,
        "source_path": row.chunk.source_path,
        "heading_path": row.chunk.heading_path,
        "text": row.chunk.text,
        "score": row.score,
    }


def create_app(kb_dir: Path, index_dir: Path) -> FastAPI:
    kb_dir.mkdir(parents=True, exist_ok=True)
    index_dir.mkdir(parents=True, exist_ok=True)
    app = FastAPI(title="Lucky Knowledge Base API", version="0.5.0")

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.post("/chat")
    def chat(payload: ChatRequest) -> dict:
        result = ask_question(
            payload.question,
            index_dir=index_dir,
            top_k=payload.top_k,
            threshold=payload.threshold,
            retrieval_strategy=payload.retrieval_strategy,
        )
        return {
            "answer": result.answer,
            "citations": result.citations,
            "retrieved_chunks": [_serialize_chunk(row) for row in result.top_chunks],
            "query_id": result.query_id,
            "answer_id": result.answer_id,
        }

    @app.post("/upload")
    async def upload(file: UploadFile = File(...)) -> dict:
        filename = Path(file.filename or "uploaded.md").name
        if not filename.lower().endswith(".md"):
            raise HTTPException(status_code=400, detail="Only .md uploads are supported in Issue 05 scope.")
        target = kb_dir / filename
        content = await file.read()
        target.write_bytes(content)
        return {"filename": filename, "bytes_written": len(content)}

    @app.post("/reindex")
    def reindex(payload: ReindexRequest | None = None) -> dict:
        args = payload if payload is not None else ReindexRequest()
        if args.full_rebuild:
            report = rebuild_index(kb_dir, index_dir, chunk_size=args.chunk_size, overlap=args.overlap)
        else:
            report = index_markdown_dir(kb_dir, index_dir, chunk_size=args.chunk_size, overlap=args.overlap)
        return asdict(report)

    @app.post("/feedback")
    def feedback(payload: FeedbackRequest) -> dict:
        if not answer_exists(index_dir, payload.answer_id):
            raise HTTPException(status_code=404, detail="answer_id not found")

        upsert_feedback(index_dir, payload.answer_id, payload.rating, payload.comment)
        record_feedback_event(index_dir, payload.answer_id, payload.rating, payload.comment)

        if payload.rating < 0:
            log_bad_answer(
                index_dir=index_dir,
                answer_id=payload.answer_id,
                question=payload.question,
                answer_text=payload.answer,
                retrieval_trace=payload.retrieved_chunks,
            )

        return {"status": "ok"}

    @app.get("/feedback/events")
    def feedback_events() -> dict:
        return {"events": list_feedback_events(index_dir)}

    @app.get("/feedback/bad-answers")
    def bad_answers() -> dict:
        return {"bad_answers": list_bad_answer_logs(index_dir)}

    return app

