.PHONY: format lint test bench-start build help

help:
	@echo "Available commands:"
	@echo "  format      - Format code with black"
	@echo "  lint        - Run linting with ruff"
	@echo "  test        - Run tests"
	@echo "  bench-start - Start development server"
	@echo "  build       - Build assets"

format:
	black .
	ruff --fix .

lint:
	black --check .
	ruff check .

test:
	bench --site test_site run-tests --app easygo_education

bench-start:
	bench start

build:
	bench build --app easygo_education
