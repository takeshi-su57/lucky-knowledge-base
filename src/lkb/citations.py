def format_citation(source_path: str, heading_path: list[str], score: float) -> str:
    heading = " > ".join(heading_path) if heading_path else "(no heading)"
    return f"- {source_path} :: {heading} (score={score:.2f})"
