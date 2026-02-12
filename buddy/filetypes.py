from __future__ import annotations
from pathlib import Path
from typing import Set

CODE_EXTENSIONS: Set[str] = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".py",
    ".go",
    ".rs",   # Rust
    ".sh",   # Bash/shell
    ".bash",
    ".rb",   # Ruby
    ".java",
}

SKIP_DIRS: Set[str] = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".venv",
    "__pycache__",
}


def is_code_file(path: Path) -> bool:
    """Return True if the file has a supported extension."""
    return path.suffix in CODE_EXTENSIONS