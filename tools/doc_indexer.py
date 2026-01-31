"""Simple document chunker + in-memory vector store for prototyping.

This module provides a small, dependency-light indexer for development and
can optionally use the `openai` package to compute embeddings when available.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
from typing import List, Dict, Any, Tuple

INDEX_PATH = os.path.join("data", "index.json")


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Chunk text into overlapping chunks by characters (simple but effective).

    Args:
        text: the input text
        chunk_size: target chunk size in characters
        overlap: overlap in characters between chunks
    """
    if chunk_size <= 0:
        return [text]
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        chunks.append(text[start:end])
        if end == length:
            break
        start = max(end - overlap, end) if overlap < chunk_size else end
    return chunks


def _hash_embed(text: str, dim: int = 128) -> List[float]:
    """Deterministic pseudo-embedding using SHA256 — fallback when no API.

    Produces a vector of floats in [-1, 1].
    """
    h = hashlib.sha256(text.encode("utf-8")).digest()
    vec = []
    # expand hash bytes to floats
    for i in range(dim):
        b = h[i % len(h)]
        vec.append((b / 255.0) * 2 - 1)
    # normalize
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def _try_openai_embed(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """Try to compute embeddings using OpenAI if available.

    Returns list of embedding vectors if successful, otherwise raises Exception.
    """
    try:
        import openai
        # OpenAI library expects API key in env var OPENAI_API_KEY
        resp = openai.Embedding.create(input=texts, model=model)
        return [item["embedding"] for item in resp["data"]]
    except Exception:
        raise


def get_embedding(text: str, dim: int = 128) -> List[float]:
    """Get an embedding for text, preferring OpenAI when available.

    Falls back to `_hash_embed` when OpenAI is unavailable or fails.
    """
    try:
        # try OpenAI with a single-item request (non-batched)
        vecs = _try_openai_embed([text])
        if vecs and isinstance(vecs[0], list):
            v = vecs[0]
            # If OpenAI embedding dimension differs from expected dim, truncate/pad
            if len(v) >= dim:
                return v[:dim]
            else:
                # pad with zeros
                return v + [0.0] * (dim - len(v))
    except Exception:
        # fallback to deterministic hash-based embedding
        return _hash_embed(text, dim=dim)
    return _hash_embed(text, dim=dim)


class InMemoryVectorStore:
    """A tiny vector store that supports add/search and disk persistence.

    This is intentionally small for prototyping. For production use a real
    vector DB (FAISS, Pinecone, Milvus, etc.) and proper OpenAI embeddings.
    """

    def __init__(self, dim: int = 128):
        self.dim = dim
        self._docs: List[Dict[str, Any]] = []

    def add_document(self, doc_id: str, text: str, meta: Dict[str, Any] | None = None):
        emb = get_embedding(text, dim=self.dim)
        self._docs.append({"id": doc_id, "text": text, "meta": meta or {}, "emb": emb})

    def similarity_search(self, query: str, top_k: int = 5) -> List[Tuple[float, Dict[str, Any]]]:
        qv = _hash_embed(query, dim=self.dim)
        results: List[Tuple[float, Dict[str, Any]]] = []
        for d in self._docs:
            score = sum(qv[i] * d["emb"][i] for i in range(self.dim))
            results.append((score, d))
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]

    def persist(self, path: str = INDEX_PATH) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._docs, f, ensure_ascii=False, indent=2)

    def load(self, path: str = INDEX_PATH) -> None:
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            self._docs = json.load(f)


def build_index_from_texts(texts: List[Tuple[str, str]], chunk_size=1000, overlap=200) -> InMemoryVectorStore:
    """Build an index from a list of (doc_id, text) tuples."""
    store = InMemoryVectorStore()
    for doc_id, text in texts:
        chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        for i, c in enumerate(chunks):
            cid = f"{doc_id}::chunk::{i}"
            store.add_document(cid, c, meta={"source": doc_id, "chunk_index": i})
    return store


if __name__ == "__main__":
    # simple demo: index sample files in data/sample_docs
    import glob

    files = glob.glob(os.path.join("data", "sample_docs", "*"))
    texts = []
    for p in files:
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            texts.append((os.path.basename(p), f.read()))

    store = build_index_from_texts(texts)
    store.persist()
    print(f"Indexed {len(store._docs)} chunks; persisted to {INDEX_PATH}")
