import argparse
import sys
from pathlib import Path

script_dir = str(Path(__file__).parent.resolve())
sys.path = [p for p in sys.path if str(Path(p).resolve()) != script_dir]

from lkb.pipeline import rebuild_index


def main() -> None:
    parser = argparse.ArgumentParser(description="Full rebuild of markdown index")
    parser.add_argument("--kb-dir", default="kb")
    parser.add_argument("--index-dir", default=".index")
    parser.add_argument("--chunk-size", type=int, default=120)
    parser.add_argument("--overlap", type=int, default=20)
    args = parser.parse_args()

    report = rebuild_index(Path(args.kb_dir), Path(args.index_dir), args.chunk_size, args.overlap)
    print(
        "Rebuilt chunks={chunks} indexed_docs={indexed} skipped_docs={skipped} "
        "reembedded_chunks={reembedded} deleted_docs={deleted}".format(
            chunks=report.total_chunks,
            indexed=report.indexed_documents,
            skipped=report.skipped_documents,
            reembedded=report.reembedded_chunks,
            deleted=report.deleted_documents,
        )
    )


if __name__ == "__main__":
    main()
