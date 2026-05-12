def format_chunk_rows(chunks: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for chunk in chunks:
        heading_path = chunk.get("heading_path", [])
        heading = " > ".join(heading_path) if heading_path else "(no heading)"
        rows.append(
            {
                "source": str(chunk.get("source_path", "")),
                "heading": heading,
                "score": f"{float(chunk.get('score', 0.0)):.4f}",
                "text": str(chunk.get("text", "")),
            }
        )
    return rows


def citation_panel_render_success(chat_results: list[dict]) -> float:
    if not chat_results:
        return 0.0
    successes = 0
    for row in chat_results:
        if row.get("citations"):
            successes += 1
    return successes / len(chat_results)

