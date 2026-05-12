from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MarkdownDocument:
    source_path: Path
    content: str


@dataclass(frozen=True)
class Chunk:
    source_path: str
    heading_path: list[str]
    text: str
    chunk_id: int | None = None
    embedding: dict[str, int] | None = None


@dataclass(frozen=True)
class ScoredChunk:
    chunk: Chunk
    score: float


@dataclass(frozen=True)
class AskResult:
    answer: str
    citations: list[str]
    top_chunks: list[ScoredChunk]


@dataclass(frozen=True)
class IndexReport:
    total_chunks: int
    indexed_documents: int
    skipped_documents: int
    reembedded_chunks: int
    deleted_documents: int


@dataclass(frozen=True)
class StoredDocument:
    id: int
    source_path: str
    content_hash: str
    content: str
    updated_at: str | None


@dataclass(frozen=True)
class LineageRow:
    document_id: int
    source_path: str
    content_hash: str
    chunk_id: int
    chunk_index: int
    heading_path: list[str]
    text: str
    embedding_id: int
    vector: dict[str, Any]
