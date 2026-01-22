from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


@dataclass(frozen=True)
class RetrievedChunk:
    file: str
    chunk_id: str
    score: float
    text: str


def _iter_note_files(notes_dir: str) -> list[Path]:
    root = Path(notes_dir)
    files: list[Path] = []
    for pat in ("**/*.md", "**/*.txt"):
        files.extend(root.glob(pat))
    return sorted([p for p in files if p.is_file()])


def _chunk_text(text: str, *, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    out: list[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + chunk_size)
        part = text[start:end].strip()
        if part:
            out.append(part)
        if end == n:
            break
        start = end - overlap
    return out


class RAG:
    def __init__(
        self,
        *,
        chroma_dir: str,
        collection_name: str = "notes",
        embeddings_model: str = "paraphrase-multilingual-MiniLM-L12-v2",
    ) -> None:
        self._client = chromadb.PersistentClient(path=chroma_dir)
        self._collection_name = collection_name
        self._emb_fn = SentenceTransformerEmbeddingFunction(model_name=embeddings_model)
        self._collection = None

    def _get_collection(self):
        if self._collection is None:
            self._collection = self._client.get_or_create_collection(
                self._collection_name,
                embedding_function=self._emb_fn,  # type: ignore[arg-type]
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    def reset(self) -> None:
        try:
            self._client.delete_collection(self._collection_name)
        except Exception:
            pass
        self._collection = self._client.create_collection(
            self._collection_name,
            embedding_function=self._emb_fn,  # type: ignore[arg-type]
            metadata={"hnsw:space": "cosine"},
        )

    def count(self) -> int:
        return int(self._get_collection().count())

    def reindex_notes(self, *, notes_dir: str) -> tuple[int, int]:
        root = Path(notes_dir)
        docs = []
        for p in _iter_note_files(notes_dir):
            rel = str(p.relative_to(root))
            text = p.read_text(encoding="utf-8", errors="ignore")
            if text.strip():
                docs.append((rel, text))

        chunks: list[tuple[str, str, str]] = []
        for rel, text in docs:
            for idx, part in enumerate(_chunk_text(text)):
                chunk_id = f"{rel}#{idx}"
                chunks.append((chunk_id, rel, part))

        self.reset()
        col = self._get_collection()
        if chunks:
            col.add(
                ids=[c_id for c_id, _, _ in chunks],
                documents=[t for _, _, t in chunks],
                metadatas=[{"file": rel, "chunk_id": c_id} for c_id, rel, _ in chunks],
            )
        return (len(docs), len(chunks))

    def query(self, *, question: str, top_k: int) -> list[RetrievedChunk]:
        col = self._get_collection()
        res: dict[str, Any] = col.query(
            query_texts=[question],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        docs = (res.get("documents") or [[]])[0]
        metas = (res.get("metadatas") or [[]])[0]
        dists = (res.get("distances") or [[]])[0]

        out: list[RetrievedChunk] = []
        for doc, meta, dist in zip(docs, metas, dists):
            distance = float(dist)
            score = 1.0 / (1.0 + distance)
            out.append(
                RetrievedChunk(
                    file=str(meta.get("file", "")),
                    chunk_id=str(meta.get("chunk_id", "")),
                    score=float(score),
                    text=str(doc),
                )
            )
        return out


