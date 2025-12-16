from functools import lru_cache
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # lightweight


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts: List[str]) -> List[List[float]]:
    model = _get_model()
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embeddings.astype("float32").tolist()


def embed_single(text: str) -> List[float]:
    return embed_texts([text])[0]
