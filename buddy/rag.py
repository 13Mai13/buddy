from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from .db import fetch_chunks_for_repo, list_repos
from .embeddings import embed_single
from .llm import chat_ollama


@dataclass
class RetrievedChunk:
    file_path: str
    content: str
    score: float


def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) or 1e-8
    return float(np.dot(a, b) / denom)


def retrieve_chunks(repo_root: str, query: str, k: int = 8) -> List[RetrievedChunk]:
    query_emb = np.array(embed_single(query), dtype="float32")
    chunks = fetch_chunks_for_repo(repo_root)
    if not chunks:
        return []

    scores: List[Tuple[float, str, str]] = []
    for _, file_path, content, emb in chunks:
        emb_vec = np.array(emb, dtype="float32")
        score = _cosine_sim(query_emb, emb_vec)
        scores.append((score, file_path, content))

    scores.sort(key=lambda x: x[0], reverse=True)
    top = scores[:k]
    return [
        RetrievedChunk(file_path=fp, content=ct, score=sc)
        for sc, fp, ct in top
    ]


def answer_question(repo_root: str, question: str) -> str:
    retrieved = retrieve_chunks(repo_root, question, k=8)
    if not retrieved:
        return "No indexed data found for this repo. Run `onboard-ai init <path>` first."

    context_snippets = []
    for r in retrieved:
        context_snippets.append(
            f"File: {r.file_path}\nScore: {r.score:.3f}\nSnippet:\n{r.content}\n"
        )
    context = "\n\n---\n\n".join(context_snippets)

    prompt = [
        {
            "role": "system",
            "content": (
                "You are an assistant helping a developer understand a codebase. "
                "Use the provided file snippets to answer clearly and concisely. "
                "Reference file paths when relevant."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Question:\n{question}\n\n"
                f"Here are some relevant code snippets from the repo:\n\n{context}"
            ),
        },
    ]
    return chat_ollama(prompt)


def generate_summary(repo_root: str) -> str:
    # Very simple: treat "What does this codebase do?" as a question.
    return answer_question(repo_root, "Give me a high-level overview of this codebase.")
