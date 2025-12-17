from pathlib import Path

from buddy.filetypes import CODE_EXTENSIONS, SKIP_DIRS, is_code_file

def test_supported_extensions_basic():
    # core list we care about
    expected = {".js", ".ts", ".py", ".go", ".rs", ".sh", ".rb", ".java"}
    # we don't require exact equality, just that these are present
    for ext in expected:
        assert ext in CODE_EXTENSIONS


def test_is_code_file_true_for_supported_ext():
    assert is_code_file(Path("main.py"))
    assert is_code_file(Path("index.ts"))
    assert is_code_file(Path("script.sh"))
    assert is_code_file(Path("service.go"))


def test_is_code_file_false_for_unsupported_ext():
    assert not is_code_file(Path("README.md"))
    assert not is_code_file(Path("styles.css"))
    assert not is_code_file(Path("image.png"))


def test_skip_dirs_contains_common_junk():
    for d in [".git", "node_modules", ".venv", "__pycache__"]:
        assert d in SKIP_DIRS