from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MarkdownDocument:
    source_path: Path
    content: str


@dataclass(frozen=True)
class Chunk:
    source_path: str
    heading_path: list[str]
    text: str


@dataclass(frozen=True)
class ScoredChunk:
    chunk: Chunk
    score: float


@dataclass(frozen=True)
class AskResult:
    answer: str
    citations: list[str]
    top_chunks: list[ScoredChunk]
