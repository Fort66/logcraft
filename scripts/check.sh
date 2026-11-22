#!/usr/bin/env bash
# Собирает вывод всех проверок в один файл
mkdir -p reports
{
  echo "=== PYTEST ==="
  uv run pytest tests/ -v --tb=long
  echo
  echo "=== RUFF ==="
  uv run ruff check src tests
  echo
  echo "=== MYPY ==="
  uv run mypy src
} > reports/check.log 2>&1

echo "Лог записан: reports/check.log ($(wc -l < reports/check.log) строк)"
tail -n 15 reports/check.log