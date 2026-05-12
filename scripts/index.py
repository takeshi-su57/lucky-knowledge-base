import argparse
import sys
from pathlib import Path

script_dir = str(Path(__file__).parent.resolve())
sys.path = [p for p in sys.path if str(Path(p).resolve()) != script_dir]

from lkb.pipeline import index_markdown_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Index markdown notes")
    parser.add_argument("--kb-dir", default="kb")
    parser.add_argument("--index-dir", default=".index")
    parser.add_argument("--chunk-size", type=int, default=120)
    parser.add_argument("--overlap", type=int, default=20)
    args = parser.parse_args()

    total = index_markdown_dir(Path(args.kb_dir), Path(args.index_dir), args.chunk_size, args.overlap)
    print(f"Indexed {total} chunks from markdown notes.")


if __name__ == "__main__":
    main()
