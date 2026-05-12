import argparse
import os
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Lucky Knowledge Base Streamlit UI")
    parser.add_argument("--api-base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--port", type=int, default=8501)
    args = parser.parse_args()

    env = os.environ.copy()
    env["LKB_API_BASE_URL"] = args.api_base_url
    app_path = Path(__file__).resolve().parents[1] / "apps" / "streamlit_app.py"
    subprocess.run(
        [
            "streamlit",
            "run",
            str(app_path),
            "--server.port",
            str(args.port),
            "--server.headless",
            "true",
        ],
        check=True,
        env=env,
    )


if __name__ == "__main__":
    main()

