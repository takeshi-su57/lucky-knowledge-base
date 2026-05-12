import argparse
import sys
from pathlib import Path

script_dir = str(Path(__file__).parent.resolve())
sys.path = [p for p in sys.path if str(Path(p).resolve()) != script_dir]

from lkb.pipeline import inspect_retrieval


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect retrieval results")
    parser.add_argument("question")
    parser.add_argument("--index-dir", default=".index")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    lines = inspect_retrieval(args.question, Path(args.index_dir), args.top_k)
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
