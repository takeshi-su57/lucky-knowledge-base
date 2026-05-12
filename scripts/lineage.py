import argparse
import sys
from pathlib import Path

script_dir = str(Path(__file__).parent.resolve())
sys.path = [p for p in sys.path if str(Path(p).resolve()) != script_dir]

from lkb.pipeline import inspect_lineage


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect document -> chunk -> embedding lineage")
    parser.add_argument("--index-dir", default=".index")
    parser.add_argument("--source-path", default=None)
    args = parser.parse_args()

    lines = inspect_lineage(Path(args.index_dir), source_path=args.source_path)
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
