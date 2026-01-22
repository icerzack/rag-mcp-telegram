run-rag:
	python3 scripts/run_rag.py

run-bot:
	python3 scripts/run_bot.py

reindex:
	curl -sS -X POST http://127.0.0.1:8000/reindex -H 'Content-Type: application/json' -d '{}' | python3 -m json.tool


