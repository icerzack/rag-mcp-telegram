from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx


@dataclass(frozen=True)
class ReindexResult:
    indexed_files: int
    indexed_chunks: int


def _parse_timeout_s(timeout_raw: str) -> float:
    v = timeout_raw.strip().lower()
    if v.endswith("s"):
        v = v[:-1]
    return float(v)


class RagApiClient:
    def __init__(self, *, base_url: str, timeout: str = "60s") -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout_s = _parse_timeout_s(timeout)

    async def reindex(self) -> ReindexResult:
        async with httpx.AsyncClient(timeout=self._timeout_s) as client:
            r = await client.post(f"{self._base_url}/reindex", json={})
            r.raise_for_status()
            data: dict[str, Any] = r.json()
            return ReindexResult(
                indexed_files=int(data.get("indexed_files", 0)),
                indexed_chunks=int(data.get("indexed_chunks", 0)),
            )

    async def chat(
        self,
        *,
        question: str,
        top_k: int | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"question": question}
        if top_k is not None:
            payload["top_k"] = top_k

        async with httpx.AsyncClient(timeout=self._timeout_s) as client:
            r = await client.post(f"{self._base_url}/chat", json=payload)
            r.raise_for_status()
            return r.json()


