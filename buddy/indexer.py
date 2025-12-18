from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List, Tuple

from rich.progress import Progress

from .embeddings import embed_texts
from .db import insert_chunks, clear_repo
from .filetypes import CODE_EXTENSIONS, SKIP_DIRS, is_code_file


def iter_code_files(repo_root: Path) -> Iterable[Path]:
    """Yield code files under repo_root, respecting supported extensions and SKIP_DIRS."""
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS] # To avoid chunking unwanted directories

        for name in files:
            path = Path(root) / name
            if is_code_file(path):
                yield path


def chunk_content(content: str, max_lines: int = 80) -> List[str]:
    lines = content.splitlines()
    chunks: List[str] = []
    for i in range(0, len(lines), max_lines):
        chunk = "\n".join(lines[i : i + max_lines])
        chunks.append(chunk)
    return chunks

def create_syntax_aware_chunks(content: str) -> List[str]:
    """
    Create syntax-aware chunks of code. We'll use the AST to create chunks that are more likely to be meaningful.
    """

    import ast 
    tree = ast.parse(content)




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
            continu
        import pdb; pdb.set_trace()
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
