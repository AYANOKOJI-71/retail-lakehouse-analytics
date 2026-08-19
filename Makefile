.PHONY: install test demo compose-up compose-down

install:
	python3 -m venv .venv && .venv/bin/pip install -e ".[dev,spark]"

test:
	.venv/bin/ruff check src tests && .venv/bin/pytest -q

demo:
	.venv/bin/python -m lakehouse.pipeline --source-file data/fixtures/montgomery_retail_sales.csv

compose-up:
	docker compose up --build

compose-down:
	docker compose down --volumes
