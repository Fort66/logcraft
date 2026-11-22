[Project Structure]

logcraft/
├── src/
│   └── logcraft/
│       ├── __init__.py              # Публичный API (импорты)
│       ├── _version.py              # Версия пакета
│       ├── logger.py                # SmartLogger (обертка над loguru)
│       ├── config.py                # Глобальная конфигурация
│       │
│       ├── sinks/                   # Кастомные sinks
│       │   ├── __init__.py
│       │   ├── html_sink.py         # HTML-вывод с цветами
│       │   ├── archive_sink.py      # Архивация в отдельную папку
│       │   ├── safe_queue.py        # JSON-очередь вместо pickle
│       │   └── colored_file.py      # Цветной файл (через ANSI)
│       │
│       ├── formatters/              # Кастомные форматтеры
│       │   ├── __init__.py
│       │   ├── abbreviator.py       # Сокращение путей модулей
│       │   └── custom_tokens.py     # Расширение токенов
|       |
|       ├── rich_integration/
│       |   ├── __init__.py
│       |   ├── console.py          # Глобальный Rich Console
│       |   ├── tags.py             # Конвертер loguru-тегов → Rich-теги
│       |   └── themes.py           # Цветовые темы
│       │
│       ├── profiler/                # Модуль профилирования
│       │   ├── __init__.py
│       │   ├── core.py              # Основной класс Profiler
│       │   ├── tree.py              # Дерево вызовов (ProfileNode)
│       │   └── renderer.py          # Рендер: ASCII + JSON
│       │
│       └── utils/                   # Утилиты
│           ├── __init__.py
│           └── ansi.py              # Работа с ANSI-кодами
│
├── tests/                           # Тесты
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_logger.py
│   ├── test_sinks/
│   │   ├── __init__.py
│   │   ├── test_html_sink.py
│   │   └── test_archive_sink.py
│   └── test_profiler/
│       ├── __init__.py
│       └── test_core.py
│
├── docs/                            # Документация
│   ├── index.md
│   ├── getting-started.md
│   ├── api-reference.md
│   └── profiling.md
│
├── examples/                        # Примеры использования
│   ├── basic_usage.py
│   ├── profiling_demo.py
│   └── custom_sinks_demo.py
│
├── benchmarks/                      # Бенчмарки (для сравнения с loguru)
│   ├── bench_logger.py
│   └── bench_profiler.py
│
├── .github/
│   ├── workflows/
│   │   ├── tests.yml                # CI: тесты на разных Python
│   │   ├── lint.yml                 # CI: линтинг
│   │   └── release.yml              # CI: публикация в PyPI
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .gitignore
├── .pre-commit-config.yaml          # Pre-commit хуки
├── pyproject.toml                   # Конфигурация проекта
├── README.md
├── CHANGELOG.md
├── LICENSE                          # MIT
├── CONTRIBUTING.md
└── Makefile                         # Команды для разработки


[Git Branches]

main                          ← стабильные релизы (v0.1.0, v0.2.0...)
│
├── develop                   ← основная ветка разработки (интеграция фич)
│   │
│   ├── feature/smart-logger-wrapper    ← обертка над Loguru
│   ├── feature/html-sink               ← HTML-вывод
│   ├── feature/archive-sink            ← архивация логов
│   ├── feature/safe-queue              ← безопасная очередь
│   ├── feature/abbreviator             ← сокращение путей
│   ├── feature/profiler-python         ← прототип профайлера на Python
│   │
│   └── feature/rust-core               ← 🦀 ОТДЕЛЬНАЯ ВЕТКА: Rust реализация
│       ├── feature/rust-profiler       ← профайлер на Rust
│       └── feature/rust-formatter      ← форматтер на Rust
│
├── hotfix/*                  ← срочные исправления в main
└── release/*                 ← подготовка релиза



[Test Running]

# Запуск тестов
uv run pytest

# Запуск линтера
uv run ruff check src tests

# Запуск форматтера
uv run ruff format src tests

# Запуск типизации
uv run mypy src

# Запуск примеров
uv run python examples/basic_usage.py
