import sys
from pathlib import Path

# Avoid shadowing stdlib inspect by scripts/inspect.py when run as a script.
script_dir = str(Path(__file__).parent.resolve())
sys.path = [p for p in sys.path if str(Path(p).resolve()) != script_dir]

import time

from lkb.pipeline import index_markdown_dir, ask_question


def main() -> None:
    kb_dir = Path("kb")
    index_dir = Path(".index")
    index_markdown_dir(kb_dir, index_dir)

    qa = [(f"What does topic {i:02d} describe?", f"topic-{i:02d}.md") for i in range(1, 21)]
    hits = 0
    latencies = []
    for question, expected_source in qa:
        start = time.perf_counter()
        result = ask_question(question, index_dir, top_k=5, threshold=0.1)
        latencies.append(time.perf_counter() - start)
        top_paths = [c.chunk.source_path for c in result.top_chunks]
        if any(expected_source in p for p in top_paths):
            hits += 1

    unknown_questions = [
        "What is quantum chromodynamics color confinement?",
        "Explain Byzantine fault tolerant consensus math proof.",
        "How to derive Navier-Stokes from first principles here?",
        "What is the capital of Mars colony one?",
        "Summarize the genetics of dragon species in these notes.",
    ]
    unknown_correct = 0
    for q in unknown_questions:
        result = ask_question(q, index_dir, top_k=5, threshold=0.8)
        if result.answer == "I don't know based on the indexed notes.":
            unknown_correct += 1

    retrieval_top5_accuracy = hits / len(qa)
    unknown_answer_accuracy = unknown_correct / len(unknown_questions)
    p95_query_latency = sorted(latencies)[max(0, int(0.95 * len(latencies)) - 1)]

    print(f"retrieval_top5_accuracy={retrieval_top5_accuracy:.2f}")
    print(f"unknown_answer_accuracy={unknown_answer_accuracy:.2f}")
    print(f"p95_query_latency={p95_query_latency:.4f}s")


if __name__ == "__main__":
    main()
