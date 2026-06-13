.PHONY: install dev tests

install:
	uv sync

dev:
	PYTHONPATH=src uv run fastapi dev
tests:
	uv run pytest
