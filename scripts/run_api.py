import argparse
import sys
from pathlib import Path

import uvicorn

script_dir = str(Path(__file__).parent.resolve())
sys.path = [p for p in sys.path if str(Path(p).resolve()) != script_dir]

from lkb.api import create_app


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Lucky Knowledge Base FastAPI server")
    parser.add_argument("--kb-dir", default="kb")
    parser.add_argument("--index-dir", default=".index")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    app = create_app(Path(args.kb_dir), Path(args.index_dir))
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()

