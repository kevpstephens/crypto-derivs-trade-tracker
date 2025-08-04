.PHONY: install test format lint docker-build docker-up docker-down clean run help

# Default target
help:
	@echo "Crypto Derivatives Trade Tracker - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install     Install dependencies"
	@echo ""
	@echo "Development:"
	@echo "  run         Start development server"
	@echo "  test        Run test suite"
	@echo "  format      Format code with black and isort"
	@echo "  lint        Lint code with flake8"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build    Build Docker image"
	@echo "  docker-up       Start all services (API, DB, Redis)"
	@echo "  docker-down     Stop all services"
	@echo "  docker-logs     Show service logs"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean       Clean up cache files and artifacts"

# Development setup
install:
	pip install -r requirements.txt

# Testing
test:
	pytest -v

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term

# Code quality
format:
	black app/ tests/
	isort app/ tests/

lint:
	flake8 app/ tests/

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Development server
run:
	uvicorn app.main:app --reload

# Cleanup
clean:
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/