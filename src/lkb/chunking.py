from pathlib import Path

from lkb.models import Chunk


def chunk_markdown_document(
    source_path: Path,
    content: str,
    chunk_size: int = 120,
    overlap: int = 20,
) -> list[Chunk]:
    lines = content.splitlines()
    heading_path: list[str] = []
    body_words: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            heading = stripped[level:].strip()
            if heading:
                heading_path = heading_path[: level - 1] + [heading]
        elif stripped:
            body_words.extend(stripped.split())

    chunks: list[Chunk] = []
    i = 0
    source_str = str(source_path)
    while i < len(body_words):
        text_words = body_words[i : i + chunk_size]
        chunks.append(Chunk(source_path=source_str, heading_path=list(heading_path), text=" ".join(text_words)))
        if i + chunk_size >= len(body_words):
            break
        i += max(1, chunk_size - overlap)

    if not chunks:
        chunks.append(Chunk(source_path=source_str, heading_path=list(heading_path), text=""))

    return chunks
