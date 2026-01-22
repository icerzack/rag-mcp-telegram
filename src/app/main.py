from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.config import load_settings
from app.llm.openrouter_client import OpenRouterClient, OpenRouterConfig
from app.rag.rag import RAG


app = FastAPI(title="tech-notes-rag")
logger = logging.getLogger("uvicorn.error")


class ReindexRequest(BaseModel):
    notes_dir: str | None = None


class ReindexResponse(BaseModel):
    indexed_files: int
    indexed_chunks: int


class ChatRequest(BaseModel):
    question: str
    top_k: int | None = None


class ChatResponse(BaseModel):
    answer: str


@app.post("/reindex", response_model=ReindexResponse)
def reindex(req: ReindexRequest | None = None) -> ReindexResponse:
    settings = load_settings()
    notes_dir = req.notes_dir if req and req.notes_dir else settings.notes_dir

    try:
        logger.info(
            "reindex: notes_dir=%s chroma_dir=%s embeddings_model=%s",
            notes_dir,
            settings.chroma_dir,
            settings.embeddings_model,
        )
        rag = RAG(chroma_dir=settings.chroma_dir, embeddings_model=settings.embeddings_model)
        indexed_files, indexed_chunks = rag.reindex_notes(notes_dir=notes_dir)
        return ReindexResponse(indexed_files=indexed_files, indexed_chunks=indexed_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    settings = load_settings()

    top_k = req.top_k if req.top_k is not None else settings.top_k_default
    if top_k <= 0 or top_k > 20:
        raise HTTPException(status_code=400, detail="top_k must be in [1, 20]")

    rag = RAG(chroma_dir=settings.chroma_dir, embeddings_model=settings.embeddings_model)
    if rag.count() == 0:
        return ChatResponse(
            answer=(
                "Похоже, индекс пуст. Запусти /reindex (или вызови POST /reindex) и повтори вопрос.\n\n"
                "Также проверь, что NOTES_DIR указывает на папку с заметками."
            ),
        )
    retrieved = rag.query(question=req.question, top_k=top_k)
    if retrieved:
        top = max(retrieved, key=lambda x: x.score)
        logger.info("chat: q=%r top_k=%s top_file=%s top_score=%.4f", req.question, top_k, top.file, top.score)
    else:
        logger.info("chat: q=%r top_k=%s retrieved=0", req.question, top_k)

    if len(retrieved) == 0:
        return ChatResponse(
            answer=(
                "В заметках не нашлось релевантной информации по этому вопросу. Попробуй переформулировать.\n\n"
                "Если ты только что добавил/изменил заметки — запусти /reindex."
            ),
        )

    context = "\n\n".join([f"SOURCE: {c.file}\n{c.text}" for c in retrieved])
    system = (
        "Ты отвечаешь только на основе CONTEXT. "
        "Если в контексте нет ответа — скажи, что в заметках нет информации и предложи уточнить.\n\n"
        "Требования к строгости:\n"
        "- Не добавляй факты, команды, флаги или шаги, которых явно нет в CONTEXT\n"
        "- Если пользователь просит команду/пример, а этого нет в CONTEXT — прямо скажи, что этого нет в заметках\n\n"
        "Требования к формату:\n"
        "- Верни только Telegram HTML (без Markdown)\n"
        "- Используй <b> для заголовков, <code> для inline-кода, <pre> для блоков кода\n"
        "- Не добавляй список источников в ответ\n"
    )

    try:
        llm = OpenRouterClient(
            OpenRouterConfig(
                api_key=settings.openrouter_api_key,
                base_url=settings.openrouter_base_url,
                model=settings.openrouter_model,
                app_url=settings.openrouter_app_url,
                app_title=settings.openrouter_app_title,
            )
        )
        answer = llm.chat(system=system, user=req.question, context=context)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e)) from e

    return ChatResponse(answer=answer)

