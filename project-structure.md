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



uv run python examples/rich_html_demo.py


Что мы вылечилено на данный момент

    Дублирование в терминале — SmartLogger.add() автоматически убирает дефолтный stderr-sink
    ANSI-мусор в файлах — HTMLSink конвертирует ANSI → чистый HTML через Rich
    Терминальный рендеринг — RichSink даёт TrueColor, жирный, курсив

Что не тронуто пока ❌
Из того, что сообщество просит в Issues Loguru:
Критичные боли (высокий спрос):

    Сокращение путей модулей ({name:abbrev}) — Issue #1400
        Сейчас: my.company.project.core.services.auth.utils
        Должно быть: m.c.p.c.s.a.utils или просто utils
    Отдельная папка для архивов — Issue #1473
        Сейчас: ротированные логи сваливаются в ту же папку
        Должно быть: logs/archive/2026-11-22_14-30-00.log
    Безопасная очередь — Issue #563
        Сейчас: enqueue=True использует pickle (уязвимость)
        Должно быть: JSON-сериализация или безопасный бинарный протокол
    Профилирование как логирование — твоя главная идея
        Встроенный профайлер с флеймграфом, цветовыми маркерами, JSON-экспортом

Средние боли:

    Права доступа на файлы (permissions) — Issue #401
    Поддержка %s форматирования — Issue #1367
    Ограничение длины трейсбека — Issue #77
    Интеграция с OpenTelemetry — Issue #674

Что делать?
Следующий спринт (текущая ветка):

    Сокращение путей (легко, полезно сразу)
    Архивная папка (легко, полезно сразу)
    Профайлер (главная фича, ради которой всё затевалось)

Параллельно в Rust-ветке:

    Безопасная очередь (JSON вместо pickle)
    Оптимизация форматирования на C/Rust
    OpenTelemetry sink


    
Дорожная карта лечения болей Loguru
№,  Боль,                           Issue       Loguru,     Ветка,                      Сложность
0,  Дубли в терминале,              "#208,      #112",      smart-logger-wrapper,       ✅ вылечено
0,  ANSI-мусор в файлах,            "#26,       #153",      smart-logger-wrapper,       ✅ вылечено
1,  Длинные пути модулей,           #1400,                  feature/abbreviator,        ✅ низкая
2,  Архивные логи в общей папке,    #1473,                  feature/archive-sink,       ✅ низкая
3,  Нет chmod на лог-файлы,         #401,                   feature/file-permissions,   ✅ низкая
4,  Нет %s-форматирования,          #1367,                  feature/percent-format,     ✅ низкая
5,  Трейсбек на 200 строк,          #77,                    feature/traceback-limit,    средняя
6,  pickle в enqueue=True,          #563,                   feature/safe-queue,         высокая
7,  Нет OpenTelemetry,              #674,                   feature/otel-sink,          средняя
8,  Профайлер (финал),              —,                      feature/profiler,           высокая
