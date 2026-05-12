from pathlib import Path

from lkb.citations import format_citation
from lkb.chunking import chunk_markdown_document
from lkb.markdown import load_markdown_documents
from lkb.models import AskResult
from lkb.prompting import GROUNDING_PROMPT_TEMPLATE
from lkb.retrieval import retrieve
from lkb.store import load_index, save_index

UNKNOWN_ANSWER = "I don't know based on the indexed notes."


def index_markdown_dir(kb_dir: Path, index_dir: Path, chunk_size: int = 120, overlap: int = 20) -> int:
    docs = load_markdown_documents(kb_dir)
    chunks = []
    for doc in docs:
        chunks.extend(
            chunk_markdown_document(doc.source_path, doc.content, chunk_size=chunk_size, overlap=overlap)
        )
    save_index(index_dir, chunks)
    return len(chunks)


def ask_question(question: str, index_dir: Path, top_k: int = 5, threshold: float = 0.2) -> AskResult:
    chunks = load_index(index_dir)
    top_chunks = retrieve(question, chunks, top_k=top_k)

    if not top_chunks or top_chunks[0].score < threshold:
        return AskResult(answer=UNKNOWN_ANSWER, citations=[], top_chunks=top_chunks)

    best = top_chunks[0]
    answer = best.chunk.text.strip() or UNKNOWN_ANSWER
    citations = [format_citation(row.chunk.source_path, row.chunk.heading_path, row.score) for row in top_chunks]

    context = "\n".join(
        f"[{i+1}] {row.chunk.source_path} :: {' > '.join(row.chunk.heading_path)}\n{row.chunk.text}"
        for i, row in enumerate(top_chunks)
    )
    _ = GROUNDING_PROMPT_TEMPLATE.format(question=question, context=context)

    return AskResult(answer=answer, citations=citations, top_chunks=top_chunks)


def inspect_retrieval(question: str, index_dir: Path, top_k: int = 5) -> list[str]:
    chunks = load_index(index_dir)
    scored = retrieve(question, chunks, top_k=top_k)
    lines = []
    for row in scored:
        heading = " > ".join(row.chunk.heading_path) if row.chunk.heading_path else "(no heading)"
        lines.append(f"score={row.score:.4f}\t{row.chunk.source_path}\t{heading}\t{row.chunk.text[:120]}")
    return lines
