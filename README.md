# buddy

> *Archived: a 2-day MVP from December 2025 (plus one follow-up in February 2026). Not maintained.*

A small local CLI to ask questions about a codebase. It embeds code chunks locally, stores them in SQLite, retrieves the closest ones by cosine similarity and asks a local LLM (Ollama) to answer from them. Nothing leaves your machine.

I built it to try local RAG over code end to end. It works, but answer quality is rough.

## What it does

- `buddy init <path> [<path> ...]`: index one or more repos
- `buddy ask "Where is login handled?"`: answer a question from the top 8 retrieved chunks
- `buddy summary`: write a high-level overview of an indexed repo

## How it works

```
buddy (Typer CLI)
 ├── indexer.py            walks the repo (skips .git, node_modules, .venv, ...) and splits files into 80-line chunks
 ├── code_chunk_indexer.py AST-based chunking for Python (functions, classes, signatures)
 ├── embeddings.py         all-MiniLM-L6-v2 via sentence-transformers
 ├── db.py                 SQLite store at ~/.onboard_ai/index.sqlite
 ├── rag.py                brute-force cosine retrieval + prompt
 └── llm.py                Ollama chat (phi3:mini by default, override with BUDDY_MODEL)
```

## Status and limits

- The AST chunker is written but **not wired in yet**: indexing still embeds fixed 80-line chunks.
- Retrieval is a brute-force scan over every chunk. Fine for one repo, slow for many.
- Supported extensions: `.py .js .jsx .ts .tsx .go .rs .sh .bash .rb .java`.
- Tests are minimal (`tests/test_filetypes.py`).

## Run it

Requires Python 3.10+, [uv](https://docs.astral.sh/uv/) and [Ollama](https://ollama.com).

```bash
git clone https://github.com/13Mai13/buddy && cd buddy
uv venv && source .venv/bin/activate
uv pip install -e .
ollama pull phi3:mini
buddy init ./path/to/repo
buddy ask "Where is authentication implemented?"
```

## License

Apache 2.0
