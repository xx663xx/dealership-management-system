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
make setup
make build-lib
make docs
make coverage
```

Если Python нужно указать явно:

```bash
make check PYTHON=python
make setup PYTHON=python
make build-lib PYTHON=python
make docs PYTHON=python
make coverage PYTHON=python
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

Документацию и редактируемые диаграммы можно проверить командой:

```bash
make docs
```

Отчет покрытия тестами формируется через `coverage.py`:

```bash
make setup
make coverage
```

`make coverage` запускает весь `unittest`-набор, печатает отчет в терминал и создает `coverage.xml`. Общий процент покрытия включает Tkinter GUI-слой, поэтому он ниже покрытия reusable core; GUI-сценарии дополнительно проверяются smoke/manual проверками.

## Сборка переиспользуемого ядра

Переиспользуемая логика находится в:

```text
packages/dealership_core/
```

Собрать ее как wheel-артефакт можно без запуска GUI:

```bash
make setup
make build-lib
```

`make setup` явно устанавливает инструменты разработки `build`, `setuptools` и `coverage`. `make build-lib` не устанавливает зависимости молча: он проверяет, что build tooling доступен, и собирает wheel через стандартный `python -m build`.

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
docs/diagrams/                  редактируемые исходники диаграмм и PNG-экспорты
Dockerfile                      контейнерная non-GUI проверка
infra/                          Compose и описание контейнерной проверки
screenshots/                    скриншоты Tkinter-интерфейса
```

## Документация

Основные документы:

- `docs/specification.md` - назначение проекта, роли, сущности, сценарии и ограничения;
- `docs/architecture.md` - слои приложения, reusable core, SQLite, договоры и тестовая стратегия;
- `docs/developer-guide.md` - локальный workflow разработчика, ветки, проверки и Pull Request;
- `docs/traceability.md` - матрица соответствия требований файлам, тестам и PR;
- `docs/diagrams/` - редактируемые исходники диаграмм и PNG-экспорты для отчетов.

Индекс диаграмм находится в `docs/diagrams/README.md`: там перечислены Draw.io-исходники, PNG-превью и документы, где каждая диаграмма используется.

`screenshots/` хранит только скриншоты Tkinter-интерфейса. Диаграммы и их PNG-превью лежат в `docs/diagrams/`.

## Команды проекта

```bash
make help       # показать доступные команды
make run        # запустить Tkinter-приложение
make test       # запустить unittest-набор
make check      # основная локальная проверка
make setup      # установить инструменты разработки
make build-lib  # собрать reusable core как wheel
make docs       # проверить документацию и Draw.io XML-диаграммы
make coverage   # сформировать отчет покрытия тестами
make compose-check  # запустить Docker/Compose non-GUI проверку
make compose-down   # остановить compose-окружение проверки
make clean      # удалить локальные generated artifacts
```
