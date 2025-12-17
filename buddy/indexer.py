import os
from pathlib import Path
from typing import Iterable, List, Tuple

from rich.progress import Progress

from .embeddings import embed_texts
from .db import insert_chunks, clear_repo

CODE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".go", ".rb", ".java", ".kt", ".rs"}


def iter_code_files(repo_root: Path) -> Iterable[Path]:
    for root, _, files in os.walk(repo_root):
        for name in files:
            path = Path(root) / name
            if path.suffix in CODE_EXTENSIONS:
                yield path


def chunk_content(content: str, max_lines: int = 80) -> List[str]:
    lines = content.splitlines()
    chunks: List[str] = []
    for i in range(0, len(lines), max_lines):
        chunk = "\n".join(lines[i : i + max_lines])
        chunks.append(chunk)
    return chunks


def index_repo(repo_root: Path) -> None:
    repo_root = repo_root.resolve()
    clear_repo(str(repo_root))

    files = list(iter_code_files(repo_root))
    if not files:
        return

    all_texts: List[str] = []
    meta: List[Tuple[str, str]] = []

    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        chunks = chunk_content(text)
        for chunk in chunks:
            all_texts.append(chunk)
            rel_path = str(path.relative_to(repo_root))
            meta.append((rel_path, chunk))

    if not all_texts:
        return

    with Progress() as progress:
        task = progress.add_task(f"Indexing {repo_root.name}", total=len(all_texts))
        batch_size = 64
        start = 0
        while start < len(all_texts):
            batch = all_texts[start : start + batch_size]
            embeddings = embed_texts(batch)
            items = []
            for (file_path, content), emb in zip(
                meta[start : start + batch_size], embeddings
            ):
                items.append((file_path, content, emb))
            insert_chunks(str(repo_root), items)
            start += batch_size
            progress.update(task, advance=len(batch))
