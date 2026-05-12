from pathlib import Path

from lkb.models import MarkdownDocument


def load_markdown_documents(kb_dir: Path) -> list[MarkdownDocument]:
    docs = []
    for path in sorted(kb_dir.rglob("*.md")):
        content = path.read_text(encoding="utf-8").lstrip("\ufeff")
        docs.append(MarkdownDocument(source_path=path, content=content))
    return docs
