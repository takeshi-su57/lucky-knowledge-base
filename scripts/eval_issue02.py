import sys
import tempfile
import time
from pathlib import Path

script_dir = str(Path(__file__).parent.resolve())
sys.path = [p for p in sys.path if str(Path(p).resolve()) != script_dir]

from lkb.pipeline import index_markdown_dir, rebuild_index
from lkb.store import load_index, load_lineage


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        kb_dir = root / "kb"
        index_dir = root / ".index"
        kb_dir.mkdir(parents=True, exist_ok=True)
        index_dir.mkdir(parents=True, exist_ok=True)

        for path in Path("kb").rglob("*.md"):
            rel = path.relative_to("kb")
            target = kb_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

        start = time.perf_counter()
        full = rebuild_index(kb_dir, index_dir)
        full_runtime = time.perf_counter() - start

        start = time.perf_counter()
        incremental = index_markdown_dir(kb_dir, index_dir)
        incremental_runtime = time.perf_counter() - start

        chunks = load_index(index_dir)
        lineage = load_lineage(index_dir)
        lineage_lookup_success_rate = len(lineage) / len(chunks) if chunks else 1.0
        runtime_reduction = 1 - (incremental_runtime / full_runtime if full_runtime else 0.0)

        print(f"full_rebuild_runtime={full_runtime:.6f}s")
        print(f"incremental_runtime={incremental_runtime:.6f}s")
        print(f"incremental_runtime_reduction={runtime_reduction:.2%}")
        print(f"lineage_lookup_success_rate={lineage_lookup_success_rate:.2f}")
        print(f"full_rebuild_chunks={full.total_chunks}")
        print(f"incremental_indexed_docs={incremental.indexed_documents}")
        print(f"incremental_skipped_docs={incremental.skipped_documents}")


if __name__ == "__main__":
    main()
