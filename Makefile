.PHONY: install test lint typecheck serve demo
install:
	python -m pip install -e ".[dev]"
test:
	pytest
lint:
	ruff check .
	ruff format --check .
typecheck:
	mypy
serve:
	uvicorn tsnt.api.app:create_app --factory --reload
demo:
	tsnt demo
