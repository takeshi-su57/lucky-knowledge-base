from lkb.models import Chunk


def apply_metadata_filters(chunks: list[Chunk], metadata_filters: dict | None = None) -> list[Chunk]:
    if not metadata_filters:
        return chunks

    source_paths = metadata_filters.get("source_paths")
    source_prefixes = metadata_filters.get("source_path_prefixes")
    heading_contains = metadata_filters.get("heading_contains")

    allowed_paths = {str(path) for path in source_paths} if source_paths else None
    allowed_prefixes = tuple(str(prefix) for prefix in source_prefixes) if source_prefixes else ()
    heading_needle = str(heading_contains).lower() if heading_contains else None

    filtered: list[Chunk] = []
    for chunk in chunks:
        if allowed_paths is not None and chunk.source_path not in allowed_paths:
            continue
        if allowed_prefixes and not chunk.source_path.startswith(allowed_prefixes):
            continue
        if heading_needle:
            heading = " > ".join(chunk.heading_path).lower()
            if heading_needle not in heading:
                continue
        filtered.append(chunk)
    return filtered
