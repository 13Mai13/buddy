import json
import sqlite3
from pathlib import Path
from typing import Iterable, List, Tuple, Optional

from .config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root TEXT NOT NULL,
    file_path TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_repo_root ON chunks(repo_root);
"""



def get_conn(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.executescript(SCHEMA)
    return conn


def insert_chunks(
    repo_root: str,
    items: Iterable[Tuple[str, str, List[float]]],  # (file_path, content, embedding)
) -> None:
    conn = get_conn()
    with conn:
        conn.executemany(
            "INSERT INTO chunks (repo_root, file_path, content, embedding) VALUES (?, ?, ?, ?)",
            [
                (repo_root, file_path, content, json.dumps(embedding))
                for file_path, content, embedding in items
            ],
        )
    conn.close()


def fetch_chunks_for_repo(repo_root: str) -> List[Tuple[int, str, str, List[float]]]:
    conn = get_conn()
    cur = conn.execute(
        "SELECT id, file_path, content, embedding FROM chunks WHERE repo_root = ?",
        (repo_root,),
    )
    rows = cur.fetchall()
    conn.close()
    result = []
    for chunk_id, file_path, content, emb_json in rows:
        result.append((chunk_id, file_path, content, json.loads(emb_json)))
    return result


def list_repos() -> List[str]:
    conn = get_conn()
    cur = conn.execute("SELECT DISTINCT repo_root FROM chunks")
    roots = [row[0] for row in cur.fetchall()]
    conn.close()
    return roots


def clear_repo(repo_root: str) -> None:
    conn = get_conn()
    with conn:
        conn.execute("DELETE FROM chunks WHERE repo_root = ?", (repo_root,))
    conn.close()
