import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    openrouter_api_key: str
    openrouter_base_url: str
    openrouter_model: str
    openrouter_app_url: str
    openrouter_app_title: str

    notes_dir: str
    chroma_dir: str
    embeddings_model: str
    top_k_default: int


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _resolve_path(p: str, *, base: Path) -> str:
    pp = Path(p)
    if pp.is_absolute():
        return str(pp)
    return str((base / pp).resolve())


def _get_env(name: str, default: str | None = None) -> str:
    v = os.getenv(name, default)
    if v is None or v == "":
        raise ValueError(f"Missing required env var: {name}")
    return v


def load_settings() -> Settings:
    base = _repo_root()
    return Settings(
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
        openrouter_base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        openrouter_model=os.getenv("OPENROUTER_MODEL", ""),
        openrouter_app_url=os.getenv("OPENROUTER_APP_URL", "http://localhost"),
        openrouter_app_title=os.getenv("OPENROUTER_APP_TITLE", "tech-notes-rag-bot"),
        notes_dir=_resolve_path(os.getenv("NOTES_DIR", "notes"), base=base),
        chroma_dir=_resolve_path(os.getenv("CHROMA_DIR", ".chroma"), base=base),
        embeddings_model=os.getenv("EMBEDDINGS_MODEL", "paraphrase-multilingual-MiniLM-L12-v2"),
        top_k_default=int(os.getenv("TOP_K_DEFAULT", "4")),
    )


