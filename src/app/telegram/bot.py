from __future__ import annotations

import logging
import os

from telegram import Update
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from app.api.client import RagApiClient


logger = logging.getLogger(__name__)

async def _reply_html(update: Update, text: str) -> None:
    if update.message is None:
        return
    try:
        await update.message.reply_text(
            text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except BadRequest:
        await update.message.reply_text(text)


async def _cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await _reply_html(
        update,
        "Привет! Отправь мне вопрос, и я отвечу используя твои локальные заметки.\n\nКоманды:\n/start\n/reindex"
    )


async def _cmd_reindex(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    base_url = os.getenv("PY_RAG_BASE_URL", "http://127.0.0.1:8000")
    timeout = os.getenv("REQUEST_TIMEOUT", "60s")
    client = RagApiClient(base_url=base_url, timeout=timeout)

    try:
        res = await client.reindex()
        await _reply_html(
            update,
            f"Заметки успешно индексированы.\nФайлов: {res.indexed_files}\nЧанков: {res.indexed_chunks}"
        )
    except Exception:
        logger.exception("reindex failed")
        await _reply_html(update, "RAG сервис недоступен, проверь что он запущен")


async def _on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.message.text is None:
        return

    base_url = os.getenv("PY_RAG_BASE_URL", "http://127.0.0.1:8000")
    timeout = os.getenv("REQUEST_TIMEOUT", "60s")
    client = RagApiClient(base_url=base_url, timeout=timeout)

    try:
        res = await client.chat(question=update.message.text)
        answer = str(res.get("answer", "")) or "(empty answer)"
        await _reply_html(update, answer)
    except Exception:
        logger.exception("chat failed")
        await _reply_html(update, "RAG сервис недоступен, проверь что он запущен")


def run_bot() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if token.strip() == "":
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

    logging.basicConfig(level=logging.INFO)

    app: Application = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", _cmd_start))
    app.add_handler(CommandHandler("reindex", _cmd_reindex))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, _on_text))

    logger.info("Bot started")
    app.run_polling(close_loop=False)


