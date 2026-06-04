# Руководство разработчика

## Назначение

Этот документ описывает, как работать с проектом автосалона локально - как запустить приложение, выполнить проверки, собрать переиспользуемое ядро и подготовить изменения через ветки и Pull Request.

Проект является desktop-приложением на Tkinter, поэтому GUI запускается локально на машине разработчика. Автоматические проверки выполняются без открытия графического интерфейса.

## Требования

- Python 3.11 или новее
- Git
- Make или совместимая команда `make`

Дополнительные runtime-библиотеки для приложения не нужны. Проект использует стандартные модули Python, такие как `tkinter` и `sqlite3`.

На Windows Python обычно доступен как `python`. На macOS и Linux - как `python3`. `Makefile` выбирает команду по платформе, но при необходимости ее можно переопределить.

## Проверка после clone

```bash
git clone <repo-url>
cd <repo-folder>
make help
make setup
make check
```

Если Python доступен под другим именем

```bash
make check PYTHON=python
make check PYTHON=python3
```

## Запуск приложения

```bash
make run
```

Приложение открывает Tkinter-интерфейс и использует локальную SQLite-базу `data/dealership.db`.

Если базы еще нет, проект инициализирует ее из файлов

- `sql/schema.sql`
- `sql/seed_data.sql`

## Автоматические проверки

Основная команда проверки

```bash
make check
```

Она запускает текущий набор `unittest`

- smoke-тесты для инициализации SQLite, seed-данных, отчетов и договора;
- unit и negative tests для `packages/dealership_core`;
- integration tests для SQLite-сценариев продаж и бронирований.

Тесты можно запустить отдельно

```bash
make test
```

Для проверки документации и редактируемых диаграмм:

```bash
make docs
```

Команда проверяет наличие основных Markdown-документов и парсит Draw.io XML-исходники диаграмм стандартными средствами Python.

Для отчета покрытия:

```bash
make coverage
```

Команда запускает полный набор `unittest` через `coverage.py`, печатает отчет в терминал и создает `coverage.xml`. Если tooling еще не установлен, сначала выполните `make setup`.

## Сборка переиспользуемого ядра

Переиспользуемая логика автосалона находится в

```text
packages/dealership_core/
```

Собрать ее как wheel-пакет можно командой

```bash
make install-build-tool
make build-lib
```

`make install-build-tool` явно устанавливает стандартные инструменты сборки `build` и `setuptools`. `make build-lib` не устанавливает зависимости молча: он проверяет, что build tooling уже доступен, и собирает wheel через `python -m build --wheel --no-isolation`.

## Docker/Compose проверки

Tkinter GUI запускается локально через `make run`. Контейнерные проверки используются для non-GUI сценария: тестов и сборки reusable core wheel.

```bash
make compose-check
make compose-down
```

`make compose-check` запускает сервис `checks` из `infra/compose.yaml`. `make compose-down` удаляет compose-сеть после проверки.

## Структура проекта

```text
main.py                         тонкая точка входа приложения
app/                            Tkinter UI, база данных, отчеты, договоры
packages/dealership_core/       переиспользуемые helper-функции и правила валидации
sql/                            SQLite-схема, seed-данные, SQL-запросы отчетов
templates/                      шаблон договора продажи
tests/smoke/                    smoke-тесты без GUI
tests/unit/                     тесты reusable core
tests/integration/              SQLite integration tests
docs/                           спецификация, архитектура, traceability
Dockerfile                      контейнерная non-GUI проверка
infra/                          Compose и описание контейнерной проверки
```

## Рабочий цикл

Начать с актуального `main`

```bash
git switch main
git pull --ff-only
```

Создать ветку под одну ограниченную задачу

```bash
git switch -c docs/example-change
```

После изменения запустить проверки

```bash
make check
```

Если изменение затрагивает сборку или reusable core, дополнительно запустить

```bash
make build-lib
```

Если изменение затрагивает документацию, диаграммы или инфраструктуру, полезны дополнительные проверки:

```bash
make docs
make compose-check
make compose-down
```

Перед коммитом проверить рабочее дерево:

```bash
git status --short --ignored
```

Не нужно добавлять в Git локальную память, generated files, runtime data и кэши:

- `Obsidian/`
- `AGENTS.md`
- `data/`
- `contracts/`
- `dist/`
- `build/`
- `__pycache__/`

Сгенерированные артефакты можно убрать командой:

```bash
make clean
```

Коммитить нужно только файлы, относящиеся к конкретной задаче:

```bash
git add <changed-files>
git commit -m "docs: describe local developer workflow"
git push -u origin docs/example-change
```

## Pull Request

В каждом Pull Request нужно кратко указать:

- что изменено;
- зачем это важно для требований курса;
- как изменение проверялось;
- какие связанные задачи остаются planned.

Для documentation-only PR обычно достаточно проверки:

```bash
make check
```

Если PR меняет build-команды, packaging или reusable core, также нужно запустить:

```bash
make build-lib
```

Если PR меняет документацию, диаграммы или контейнерные проверки, также нужно запустить:

```bash
make docs
make compose-check
make compose-down
```
