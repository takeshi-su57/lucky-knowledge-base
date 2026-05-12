from pathlib import Path

from lkb.citations import format_citation
from lkb.chunking import chunk_markdown_document
from lkb.embeddings import embed_text
from lkb.incremental import compute_content_hash, should_reindex
from lkb.markdown import load_markdown_documents
from lkb.models import AskResult, IndexReport
from lkb.prompting import GROUNDING_PROMPT_TEMPLATE
from lkb.retrieval import retrieve
from lkb.store import (
    clear_all_data,
    delete_documents_not_in,
    get_document,
    insert_or_update_document,
    load_index,
    load_lineage,
    record_query,
    replace_document_chunks,
)

UNKNOWN_ANSWER = "I don't know based on the indexed notes."


def index_markdown_dir(kb_dir: Path, index_dir: Path, chunk_size: int = 120, overlap: int = 20) -> IndexReport:
    docs = load_markdown_documents(kb_dir)
    indexed_documents = 0
    skipped_documents = 0
    reembedded_chunks = 0
    current_paths: set[str] = set()

    for doc in docs:
        source_path = str(doc.source_path)
        current_paths.add(source_path)
        current_hash = compute_content_hash(doc.content)
        previous = get_document(index_dir, source_path)
        if not should_reindex(previous.content_hash if previous else None, current_hash):
            skipped_documents += 1
            continue

        stored = insert_or_update_document(index_dir, source_path, current_hash, doc.content)
        chunks = chunk_markdown_document(doc.source_path, doc.content, chunk_size=chunk_size, overlap=overlap)
        chunk_rows = []
        for idx, chunk in enumerate(chunks):
            chunk_rows.append(
                {
                    "chunk_index": idx,
                    "heading_path": chunk.heading_path,
                    "text": chunk.text,
                    "embedding": dict(embed_text(chunk.text)),
                }
            )
        reembedded_chunks += replace_document_chunks(index_dir, stored.id, chunk_rows)
        indexed_documents += 1

    deleted_documents = delete_documents_not_in(index_dir, current_paths)
    total_chunks = len(load_index(index_dir))
    return IndexReport(
        total_chunks=total_chunks,
        indexed_documents=indexed_documents,
        skipped_documents=skipped_documents,
        reembedded_chunks=reembedded_chunks,
        deleted_documents=deleted_documents,
    )


def rebuild_index(kb_dir: Path, index_dir: Path, chunk_size: int = 120, overlap: int = 20) -> IndexReport:
    clear_all_data(index_dir)
    return index_markdown_dir(kb_dir, index_dir, chunk_size=chunk_size, overlap=overlap)


def ask_question(question: str, index_dir: Path, top_k: int = 5, threshold: float = 0.2) -> AskResult:
    chunks = load_index(index_dir)
    top_chunks = retrieve(question, chunks, top_k=top_k)

    if not top_chunks or top_chunks[0].score < threshold:
        record_query(index_dir, question, top_chunks, UNKNOWN_ANSWER)
        return AskResult(answer=UNKNOWN_ANSWER, citations=[], top_chunks=top_chunks)

    best = top_chunks[0]
    answer = best.chunk.text.strip() or UNKNOWN_ANSWER
    citations = [
        format_citation(
            row.chunk.source_path,
            row.chunk.heading_path,
            row.score,
            chunk_id=row.chunk.chunk_id,
        )
        for row in top_chunks
    ]

    context = "\n".join(
        f"[{i+1}] chunk_id={row.chunk.chunk_id} {row.chunk.source_path} :: {' > '.join(row.chunk.heading_path)}\n{row.chunk.text}"
        for i, row in enumerate(top_chunks)
    )
    _ = GROUNDING_PROMPT_TEMPLATE.format(question=question, context=context)
    record_query(index_dir, question, top_chunks, answer)
    return AskResult(answer=answer, citations=citations, top_chunks=top_chunks)


def inspect_retrieval(question: str, index_dir: Path, top_k: int = 5) -> list[str]:
    chunks = load_index(index_dir)
    scored = retrieve(question, chunks, top_k=top_k)
    lines = []
    for row in scored:
        heading = " > ".join(row.chunk.heading_path) if row.chunk.heading_path else "(no heading)"
        lines.append(
            f"score={row.score:.4f}\tchunk_id={row.chunk.chunk_id}\t{row.chunk.source_path}\t{heading}\t{row.chunk.text[:120]}"
        )
    return lines


def inspect_lineage(index_dir: Path, source_path: str | None = None) -> list[str]:
    rows = load_lineage(index_dir, source_path=source_path)
    lines = []
    for row in rows:
        heading = " > ".join(row.heading_path) if row.heading_path else "(no heading)"
        lines.append(
            "document_id={document_id}\tchunk_id={chunk_id}\tembedding_id={embedding_id}\t"
            "source={source}\theading={heading}\ttext={text}".format(
                document_id=row.document_id,
                chunk_id=row.chunk_id,
                embedding_id=row.embedding_id,
                source=row.source_path,
                heading=heading,
                text=row.text[:120],
            )
        )
    return lines
