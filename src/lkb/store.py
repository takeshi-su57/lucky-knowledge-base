import json
from pathlib import Path

from lkb.models import Chunk


def save_index(index_dir: Path, chunks: list[Chunk]) -> None:
    index_dir.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            "source_path": c.source_path,
            "heading_path": c.heading_path,
            "text": c.text,
        }
        for c in chunks
    ]
    (index_dir / "chunks.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_index(index_dir: Path) -> list[Chunk]:
    payload = json.loads((index_dir / "chunks.json").read_text(encoding="utf-8"))
    return [Chunk(source_path=row["source_path"], heading_path=row["heading_path"], text=row["text"]) for row in payload]
