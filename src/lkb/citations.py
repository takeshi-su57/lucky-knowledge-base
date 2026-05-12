def format_citation(source_path: str, heading_path: list[str], score: float, chunk_id: int | None = None) -> str:
    heading = " > ".join(heading_path) if heading_path else "(no heading)"
    chunk_part = f", chunk_id={chunk_id}" if chunk_id is not None else ""
    return f"- {source_path} :: {heading} (score={score:.2f}{chunk_part})"
