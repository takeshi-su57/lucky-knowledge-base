import hashlib


def compute_content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def should_reindex(previous_hash: str | None, current_hash: str) -> bool:
    if previous_hash is None:
        return True
    return previous_hash != current_hash
