.PHONY: install test lint format clean build sync add-dev

# Установка всех зависимостей
install:
	uv sync --all-extras

# Установка только dev-зависимостей
install-dev:
	uv sync --extra dev

# Добавление новой зависимости
add:
	@read -p "Package name: " pkg; uv add $$pkg

# Добавление dev-зависимости
add-dev:
	@read -p "Package name: " pkg; uv add --dev $$pkg

# Запуск тестов
test:
	uv run pytest

# Запуск тестов с coverage
test-cov:
	uv run pytest --cov=logcraft --cov-report=html

# Линтинг
lint:
	uv run ruff check src tests
	uv run mypy src

# Форматирование
format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

# Очистка
clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +

# Сборка пакета
build:
	uv build

# Публикация в PyPI
release:
	uv build
	uv publish

# Pre-commit хуки
pre-commit-install:
	uv run pre-commit install

# Запуск всех проверок перед коммитом
check: format lint test