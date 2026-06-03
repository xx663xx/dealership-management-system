# Система управления автосалоном

Проект представляет собой desktop-приложение на Tkinter для работы с базой данных автосалона. Через интерфейс можно просматривать справочники, добавлять записи, оформлять продажи, бронировать автомобили, записывать тест-драйвы, вести сервисные заявки, формировать договор продажи и открывать SQL-отчеты.

Текущее поведение защищено тестами, часть доменной логики вынесена в переиспользуемый пакет, основные действия запускаются через `Makefile`, а архитектура и диаграммы описаны в `docs/`.

## Возможности

- учет автомобилей, клиентов, сотрудников и поставщиков;
- оформление продаж и сохранение договора по шаблону;
- бронирование автомобилей;
- запись и фиксация результатов тест-драйвов;
- учет сервисных заявок;
- просмотр отчетов на основе SQL-запросов;
- автоматическая инициализация SQLite-базы из SQL-файлов;
- отдельные smoke, unit, negative и integration tests.

## Требования

- Python 3.11 или новее;
- Git;
- Make или совместимая команда `make`.

Дополнительные runtime-библиотеки не требуются, так как приложение использует стандартные модули Python - `tkinter` и `sqlite3`.

`Makefile` выбирает команду Python по платформе: `python` на Windows и `python3` на macOS/Linux. Если Python доступен под другим именем, команду можно переопределить через `PYTHON`.

## Быстрая проверка после clone

```bash
git clone <repo-url>
cd <repo-folder>
make help
make check
make install-build-tool
make build-lib
```

Если Python нужно указать явно:

```bash
make check PYTHON=python
make install-build-tool PYTHON=python
make build-lib PYTHON=python
```

## Запуск приложения

```bash
make run
```

Эта команда запускает `main.py`, который является тонкой точкой входа и делегирует запуск Tkinter-приложения в `app/main_window.py`.

При запуске используется локальная SQLite-база:

```text
data/dealership.db
```

Если базы еще нет, приложение создает структуру и демонстрационные данные из:

```text
sql/schema.sql
sql/seed_data.sql
```

## Проверки

Основная команда проверки:

```bash
make check
```

Она запускает:

- smoke-тесты инициализации SQLite, seed-данных, SQL-отчетов и договора;
- unit и negative tests для `packages/dealership_core`;
- integration tests для сценариев продаж и бронирований в SQLite.

Тесты можно запустить отдельно:

```bash
make test
```

## Сборка переиспользуемого ядра

Переиспользуемая логика находится в:

```text
packages/dealership_core/
```

Собрать ее как wheel-артефакт можно без запуска GUI:

```bash
make install-build-tool
make build-lib
```

`make install-build-tool` явно устанавливает стандартные инструменты сборки `build` и `setuptools`. `make build-lib` не устанавливает зависимости молча: он проверяет, что build tooling доступен, и собирает wheel через стандартный `python -m build`.

## Docker/Compose проверки

Tkinter GUI запускается локально через `make run`. Docker/Compose используется для воспроизводимых non-GUI проверок:

```bash
docker build -t car-dealership-checks:local .
docker run --rm car-dealership-checks:local
docker compose -f infra/compose.yaml run --rm checks
docker compose -f infra/compose.yaml down
```

Контейнер запускает автоматические тесты и собирает reusable core wheel без открытия GUI.

## Структура проекта

```text
main.py                         тонкая точка входа приложения
app/                            Tkinter UI, база данных, отчеты, договоры
packages/dealership_core/       переиспользуемые helper-функции и validators
sql/                            SQLite-схема, seed-данные, запросы отчетов
templates/                      шаблон договора продажи
tests/smoke/                    smoke-тесты без GUI
tests/unit/                     unit и negative tests reusable core
tests/integration/              SQLite integration tests
docs/                           документация, спецификация, архитектура
docs/diagrams/                  редактируемые исходники диаграмм Draw.io
Dockerfile                      контейнерная non-GUI проверка
infra/                          Compose и описание контейнерной проверки
screenshots/                    изображения интерфейса и диаграмм
```

## Документация

Основные документы:

- `docs/specification.md` - назначение проекта, роли, сущности, сценарии и ограничения;
- `docs/architecture.md` - слои приложения, reusable core, SQLite, договоры и тестовая стратегия;
- `docs/developer-guide.md` - локальный workflow разработчика, ветки, проверки и Pull Request;
- `docs/traceability.md` - матрица соответствия требований файлам, тестам и PR;
- `docs/diagrams/` - редактируемые исходники диаграмм в формате diagrams.net / Draw.io XML.

PNG-версии диаграмм используются в отчете и скриншотах, но исходниками считаются файлы в `docs/diagrams/`.

## Команды проекта

```bash
make help       # показать доступные команды
make run        # запустить Tkinter-приложение
make test       # запустить unittest-набор
make check      # основная локальная проверка
make install-build-tool  # установить стандартные инструменты сборки
make build-lib  # собрать reusable core как wheel
```

## Что пока запланировано

На текущем этапе еще не реализованы:

- отдельная команда `make docs`;
- команда отчета покрытия тестами;
- полноценная команда `make setup`.