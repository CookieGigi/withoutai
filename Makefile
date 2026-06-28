.PHONY: install dev tests

install:
	uv sync

dev:
	PYTHONPATH=src uv run fastapi dev --reload-dir src/
tests:
	uv run pytest
