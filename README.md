# buddy

# 🧠 Buddy — Your Private AI Onboarding Assistant for Codebases

**Buddy** helps developers understand complex codebases **fast**.  
It indexes your repositories locally and lets you ask natural language questions like:

> “Where is authentication handled?”  
> “Which files implement onboarding?”  
> “What calls this function?”  
> “How do these services connect?”

All AI runs **locally**, stays **private**, and requires **no cloud**

## 🚀 Why Buddy?

Modern engineering teams struggle with:

- ⚠️ Dozens of repos  
- ⚠️ Outdated or missing documentation  
- ⚠️ Tribal knowledge held by senior engineers  
- ⚠️ Onboarding that takes weeks or months  
- ⚠️ No safe way to use cloud AI (fintech, healthcare, enterprise, gov…)

Buddy solves this by:

- 📁 Indexing your entire codebase  
- 🧠 Using local embeddings + local LLMs (Ollama)  
- 🔍 Providing semantic search & RAG  
- 🗺️ Generating onboarding summaries  
- 🧑‍🏫 Acting as an “AI teammate” who understands your system  

All **100% private**, all **on your machine**.

## ✨ Features (MVP)

### 🔍 Semantic Code Search
Ask Buddy questions about your repos:

```bash
buddy ask "Where is login handled?"
```
Get answers referencing specific files & logic.

### 📚 Multi-Repo Indexing

```
buddy init ./backend ./frontend ./services/auth
```

Index many repos at once.

### 📝 Onboarding Summaries

```
buddy summary
```

Great for new developers joining a project.


## 🔒 Local-Only AI

* Embeddings run locally

* Vector DB stored locally (SQLite)

* LLM runs via Ollama

* No cloud, no telemetry, no API keys

* Buddy is private by design.


## 📦 Installation (via uv)

Clone the repo:

```
git clone https://github.com/YOURNAME/buddy
cd buddy
```

Create & activate environment:

```
uv venv
source .venv/bin/activate
```

Install Buddy:

```
uv pip install -e .
```

Ensure Ollama is installed:

```
brew install ollama
ollama pull phi3:mini   # recommended lightweight model
```

Test:

buddy --help

## 🧪 Usage

1. Index your repo(s)

```
buddy init ./path/to/repo
```

2. Ask questions

```
buddy ask "Where is the authentication implemented?"
```

3. Generate an onboarding summary

```
buddy summary
```


##  🧱 Internal Architecture (MVP)

```
buddy (Typer CLI)
     │
     ├── indexer.py     → walks repos, chunks code
     ├── embeddings.py  → local MiniLM embeddings
     ├── db.py          → SQLite vector store
     ├── rag.py         → semantic retrieval + RAG pipeline
     ├── llm.py         → Ollama integration (phi3:mini by default)
     └── config.py      → ~/.buddy paths + constants
```

* SQLite stores: file path, chunk text, embedding vector

* Retrieval uses cosine similarity

* LLM summarizes & answers using structured context

## 🧩 Roadmap

### Phase 1 — Python MVP (Current)

 CLI with Typer

 Multi-repo indexing

 Local embeddings (MiniLM)

 Vector storage in SQLite

 Local LLM via Ollama

 Ask + summary commands

 Privacy-first, no cloud

### Phase 2 — Improve Accuracy & Speed

 Better chunking and file heuristics

 Boost based on filenames (auth, login, user)

 Reranking results

 Smarter onboarding prompts

 Skip irrelevant dirs (node_modules, .venv, dist)

 Cache only changed files

### Phase 3 — Better Developer Experience

 Homebrew formula

 Config file under ~/.buddy/config.yaml

 Model selection: buddy model list

 Search command: buddy search <keyword>

 Minimal web UI (optional)

### Phase 4 — Introduce Rust

Rust will be added after validation to:

Package Buddy as a single static binary

Improve indexing speed

Enhance CLI UX

Enable brew install buddy


## 🔐 License

Apache 2.0 — permissive, open-source, business-friendly.


## 🤝 Contributing

Issues, ideas, and PRs are welcome! Help shape Buddy into the best private AI onboarding tool for developers.