.PHONY: install test lint clean build distribute docker-build docker-run

install:
	pip install -r requirements.txt
	pip install -e .

test:
	python -m pytest tests/ --cov=excel_ai_addin --cov-report=term-missing

lint:
	flake8 excel_ai_addin tests
	black --check excel_ai_addin tests
	isort --check-only excel_ai_addin tests

format:
	black excel_ai_addin tests
	isort excel_ai_addin tests

clean:
	rm -rf build/ dist/ *.egg-info/ .coverage htmlcov/ .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	python setup.py sdist bdist_wheel

distribute: clean test build
	twine check dist/*
	twine upload dist/*

docker-build:
	docker-compose build

docker-run:
	docker-compose up app

docker-test:
	docker-compose up test

docker-lint:
	docker-compose up lint

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run linting checks"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make build        - Build package"
	@echo "  make distribute   - Build and upload to PyPI"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run application in Docker"
	@echo "  make docker-test  - Run tests in Docker"
	@echo "  make docker-lint  - Run linting in Docker" 