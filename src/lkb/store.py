import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from lkb.models import Chunk, LineageRow, ScoredChunk, StoredDocument


def get_sqlite_db_path(index_dir: Path) -> Path:
    return index_dir / "index.sqlite"


def _migration_up_path() -> Path:
    return Path(__file__).parent / "sql" / "001_issue02_schema_up.sql"


def _connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def _open_conn(db_path: Path):
    conn = _connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def ensure_schema(index_dir: Path) -> None:
    index_dir.mkdir(parents=True, exist_ok=True)
    db_path = get_sqlite_db_path(index_dir)
    sql = _migration_up_path().read_text(encoding="utf-8")
    with _open_conn(db_path) as conn:
        conn.executescript(sql)
        conn.commit()


def clear_all_data(index_dir: Path) -> None:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        conn.execute("DELETE FROM bad_answer_logs")
        conn.execute("DELETE FROM feedback_events")
        conn.execute("DELETE FROM feedback")
        conn.execute("DELETE FROM answers")
        conn.execute("DELETE FROM results")
        conn.execute("DELETE FROM queries")
        conn.execute("DELETE FROM embeddings")
        conn.execute("DELETE FROM chunks")
        conn.execute("DELETE FROM documents")
        conn.commit()


def get_document(index_dir: Path, source_path: str) -> StoredDocument | None:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        row = conn.execute(
            """
            SELECT id, source_path, content_hash, content, updated_at
            FROM documents
            WHERE source_path = ?
            """,
            (source_path,),
        ).fetchone()
    if row is None:
        return None
    return StoredDocument(
        id=row["id"],
        source_path=row["source_path"],
        content_hash=row["content_hash"],
        content=row["content"],
        updated_at=row["updated_at"],
    )


def insert_or_update_document(index_dir: Path, source_path: str, content_hash: str, content: str) -> StoredDocument:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        conn.execute(
            """
            INSERT INTO documents(source_path, content_hash, content)
            VALUES (?, ?, ?)
            ON CONFLICT(source_path) DO UPDATE SET
                content_hash = excluded.content_hash,
                content = excluded.content,
                updated_at = CURRENT_TIMESTAMP
            """,
            (source_path, content_hash, content),
        )
        conn.commit()
    stored = get_document(index_dir, source_path)
    if stored is None:
        raise RuntimeError("Document upsert failed")
    return stored


def list_document_source_paths(index_dir: Path) -> list[str]:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        rows = conn.execute("SELECT source_path FROM documents ORDER BY source_path").fetchall()
    return [str(row["source_path"]) for row in rows]


def delete_documents_not_in(index_dir: Path, valid_source_paths: set[str]) -> int:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        if valid_source_paths:
            placeholders = ",".join("?" for _ in valid_source_paths)
            sql = f"DELETE FROM documents WHERE source_path NOT IN ({placeholders})"
            cursor = conn.execute(sql, tuple(sorted(valid_source_paths)))
        else:
            cursor = conn.execute("DELETE FROM documents")
        conn.commit()
        return int(cursor.rowcount if cursor.rowcount is not None else 0)


def replace_document_chunks(index_dir: Path, document_id: int, chunks: list[dict]) -> int:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    inserted = 0
    with _open_conn(db_path) as conn:
        conn.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
        for row in chunks:
            cursor = conn.execute(
                """
                INSERT INTO chunks(document_id, chunk_index, heading_path, text)
                VALUES (?, ?, ?, ?)
                """,
                (
                    document_id,
                    int(row["chunk_index"]),
                    json.dumps(row["heading_path"]),
                    str(row["text"]),
                ),
            )
            chunk_id = int(cursor.lastrowid)
            conn.execute(
                """
                INSERT INTO embeddings(chunk_id, vector, model)
                VALUES (?, ?, ?)
                """,
                (
                    chunk_id,
                    json.dumps(row["embedding"]),
                    "token-count-v1",
                ),
            )
            inserted += 1
        conn.commit()
    return inserted


def record_query(index_dir: Path, question: str, top_chunks: list[ScoredChunk], answer: str) -> tuple[int, int]:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        cursor = conn.execute("INSERT INTO queries(question) VALUES (?)", (question,))
        query_id = int(cursor.lastrowid)
        for row in top_chunks:
            if row.chunk.chunk_id is None:
                continue
            conn.execute(
                """
                INSERT INTO results(query_id, chunk_id, score)
                VALUES (?, ?, ?)
                """,
                (query_id, row.chunk.chunk_id, row.score),
            )
        answer_cursor = conn.execute(
            "INSERT INTO answers(query_id, answer) VALUES (?, ?)",
            (query_id, answer),
        )
        answer_id = int(answer_cursor.lastrowid)
        conn.execute(
            "INSERT INTO feedback(answer_id, rating, comment) VALUES (?, ?, ?)",
            (answer_id, 0, ""),
        )
        conn.commit()
    return query_id, answer_id


def upsert_feedback(index_dir: Path, answer_id: int, rating: int, comment: str) -> None:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        cursor = conn.execute(
            """
            UPDATE feedback
            SET rating = ?, comment = ?, created_at = CURRENT_TIMESTAMP
            WHERE answer_id = ?
            """,
            (rating, comment, answer_id),
        )
        if int(cursor.rowcount if cursor.rowcount is not None else 0) == 0:
            conn.execute(
                "INSERT INTO feedback(answer_id, rating, comment) VALUES (?, ?, ?)",
                (answer_id, rating, comment),
            )
        conn.commit()


def record_feedback_event(index_dir: Path, answer_id: int, rating: int, comment: str) -> None:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        conn.execute(
            "INSERT INTO feedback_events(answer_id, rating, comment) VALUES (?, ?, ?)",
            (answer_id, rating, comment),
        )
        conn.commit()


def log_bad_answer(
    index_dir: Path,
    answer_id: int,
    question: str,
    answer_text: str,
    retrieval_trace: list[dict],
) -> None:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        conn.execute(
            """
            INSERT INTO bad_answer_logs(answer_id, question, answer_text, retrieval_trace)
            VALUES (?, ?, ?, ?)
            """,
            (answer_id, question, answer_text, json.dumps(retrieval_trace)),
        )
        conn.commit()


def answer_exists(index_dir: Path, answer_id: int) -> bool:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        row = conn.execute("SELECT 1 FROM answers WHERE id = ?", (answer_id,)).fetchone()
    return row is not None


def list_feedback_events(index_dir: Path) -> list[dict]:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        rows = conn.execute(
            "SELECT id, answer_id, rating, comment, created_at FROM feedback_events ORDER BY id"
        ).fetchall()
    return [
        {
            "id": int(row["id"]),
            "answer_id": int(row["answer_id"]),
            "rating": int(row["rating"]),
            "comment": str(row["comment"]),
            "created_at": str(row["created_at"]),
        }
        for row in rows
    ]


def list_bad_answer_logs(index_dir: Path) -> list[dict]:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        rows = conn.execute(
            "SELECT id, answer_id, question, answer_text, retrieval_trace, created_at FROM bad_answer_logs ORDER BY id"
        ).fetchall()
    return [
        {
            "id": int(row["id"]),
            "answer_id": int(row["answer_id"]),
            "question": str(row["question"]),
            "answer_text": str(row["answer_text"]),
            "retrieval_trace": json.loads(str(row["retrieval_trace"])),
            "created_at": str(row["created_at"]),
        }
        for row in rows
    ]


def load_index(index_dir: Path) -> list[Chunk]:
    db_path = get_sqlite_db_path(index_dir)
    if db_path.exists():
        ensure_schema(index_dir)
        with _open_conn(db_path) as conn:
            rows = conn.execute(
                """
                SELECT c.id AS chunk_id, d.source_path, c.heading_path, c.text, e.vector
                FROM chunks c
                JOIN documents d ON d.id = c.document_id
                JOIN embeddings e ON e.chunk_id = c.id
                ORDER BY d.source_path, c.chunk_index
                """
            ).fetchall()
        return [
            Chunk(
                source_path=str(row["source_path"]),
                heading_path=json.loads(str(row["heading_path"])),
                text=str(row["text"]),
                chunk_id=int(row["chunk_id"]),
                embedding={k: int(v) for k, v in json.loads(str(row["vector"])).items()},
            )
            for row in rows
        ]

    legacy_path = index_dir / "chunks.json"
    if not legacy_path.exists():
        raise FileNotFoundError(f"No SQLite or legacy index found at {index_dir}")

    payload = json.loads(legacy_path.read_text(encoding="utf-8"))
    return [Chunk(source_path=row["source_path"], heading_path=row["heading_path"], text=row["text"]) for row in payload]


def load_lineage(index_dir: Path, source_path: str | None = None) -> list[LineageRow]:
    ensure_schema(index_dir)
    db_path = get_sqlite_db_path(index_dir)
    with _open_conn(db_path) as conn:
        params: tuple[str, ...] = ()
        where_clause = ""
        if source_path is not None:
            where_clause = "WHERE d.source_path = ?"
            params = (source_path,)
        rows = conn.execute(
            f"""
            SELECT
                d.id AS document_id,
                d.source_path,
                d.content_hash,
                c.id AS chunk_id,
                c.chunk_index,
                c.heading_path,
                c.text,
                e.id AS embedding_id,
                e.vector
            FROM documents d
            JOIN chunks c ON c.document_id = d.id
            JOIN embeddings e ON e.chunk_id = c.id
            {where_clause}
            ORDER BY d.source_path, c.chunk_index
            """,
            params,
        ).fetchall()
    return [
        LineageRow(
            document_id=int(row["document_id"]),
            source_path=str(row["source_path"]),
            content_hash=str(row["content_hash"]),
            chunk_id=int(row["chunk_id"]),
            chunk_index=int(row["chunk_index"]),
            heading_path=json.loads(str(row["heading_path"])),
            text=str(row["text"]),
            embedding_id=int(row["embedding_id"]),
            vector=json.loads(str(row["vector"])),
        )
        for row in rows
    ]
