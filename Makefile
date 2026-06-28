.PHONY: install dev dev-with-logs tests watch-logs

install:
	uv sync

dev:
	PYTHONPATH=src uv run fastapi dev --reload-dir src/

dev-with-logs:
	@mkdir -p logs
	PYTHONPATH=src uv run fastapi dev --reload-dir src/ 2>&1 | tee logs/app.log

tests:
	uv run pytest

watch-logs:
	@mkdir -p logs
	lnav logs/app.log
