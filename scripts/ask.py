import argparse
import sys
from pathlib import Path

script_dir = str(Path(__file__).parent.resolve())
sys.path = [p for p in sys.path if str(Path(p).resolve()) != script_dir]

from lkb.pipeline import ask_question


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a question against indexed markdown")
    parser.add_argument("question")
    parser.add_argument("--index-dir", default=".index")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--threshold", type=float, default=0.2)
    args = parser.parse_args()

    result = ask_question(args.question, Path(args.index_dir), args.top_k, args.threshold)
    print("Answer:")
    print(result.answer)
    print("\nCitations:")
    for citation in result.citations:
        print(citation)


if __name__ == "__main__":
    main()
