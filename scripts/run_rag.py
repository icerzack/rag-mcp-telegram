import logging
import os

import uvicorn
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    host = os.getenv("RAG_HOST", "127.0.0.1")
    port = int(os.getenv("RAG_PORT", "8000"))
    uvicorn.run("app.main:app", host=host, port=port, reload=True, log_level="info")


if __name__ == "__main__":
    main()


