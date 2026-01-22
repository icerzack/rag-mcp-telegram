from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI


@dataclass(frozen=True)
class OpenRouterConfig:
    api_key: str
    base_url: str
    model: str
    app_url: str
    app_title: str


class OpenRouterClient:
    def __init__(self, cfg: OpenRouterConfig) -> None:
        if cfg.api_key.strip() == "":
            raise ValueError("Missing OPENROUTER_API_KEY")
        if cfg.model.strip() == "":
            raise ValueError("Missing OPENROUTER_MODEL")

        self._model = cfg.model
        self._client = OpenAI(
            api_key=cfg.api_key,
            base_url=cfg.base_url,
            default_headers={
                "HTTP-Referer": cfg.app_url,
                "X-Title": cfg.app_title,
            },
        )

    def chat(self, *, system: str, user: str, context: str) -> str:
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{user}"},
            ],
            temperature=0.0,
        )
        content = resp.choices[0].message.content
        return content or ""


