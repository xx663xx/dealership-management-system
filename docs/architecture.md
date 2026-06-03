# Архитектура проекта автосалона

## Назначение документа

Этот документ объясняет, как устроен проект после первых этапов инженерного оформления. Где находится запускаемое приложение, где переиспользуемая логика, как приложение работает с SQLite, где формируются договоры и какими проверками защищено текущее поведение.

Документ дополняет `docs/specification.md`. Спецификация описывает предметную область и сценарии, а архитектура показывает границы ответственности между файлами и слоями.

## Общий вид

Проект построен как локальное desktop-приложение на Tkinter с SQLite-базой и отдельным reusable core package для чистых helper-функций и доменных правил.

```mermaid
flowchart TB
    User["Пользователь"]
    Main["main.py<br/>тонкая точка входа"]
    Window["app/main_window.py<br/>создание Tkinter окна"]
    UI["Application / GUI<br/>app/ui_tables.py<br/>app/ui_reports.py<br/>app/contracts.py"]
    Config["app/config.py<br/>таблицы, отчеты, пути"]
    Core["packages/dealership_core<br/>formatting, validators"]
    DB["app/database.py<br/>SQLite connection/init"]
    SQL["sql/schema.sql<br/>sql/seed_data.sql"]
    RuntimeDb["data/dealership.db"]
    Files["templates/contract_template.txt<br/>contracts/*.txt"]
    Tests["tests/<br/>smoke, unit, integration"]
    Build["Makefile<br/>check / build-lib"]

    User --> Main --> Window --> UI
    UI --> Config
    UI --> Core
    UI --> DB
    UI --> RuntimeDb
    UI --> Files
    DB --> SQL
    DB --> RuntimeDb
    Build -.-> Tests
    Build -.-> Core
    Tests -.-> Core
    Tests -.-> DB
    Tests -.-> RuntimeDb
```

## Слои и ответственность

| Слой | Файлы | Ответственность |
| --- | --- | --- |
| Entry point | `main.py` | Минимальная точка запуска. Импортирует `run_app()` и вызывает его только при запуске файла. |
| Application/UI | `app/main_window.py`, `app/ui_tables.py`, `app/ui_reports.py` | Tkinter-окна, меню, таблицы, формы, кнопки, сообщения об ошибках. |
| Application services | `app/contracts.py`, `app/database.py`, `app/config.py` | Работа с договорами, подключение и инициализация SQLite, конфигурация таблиц и отчетов. |
| Reusable core | `packages/dealership_core/` | Чистые функции форматирования, безопасное имя файла договора, доменная валидация продаж, броней и тест-драйвов. |
| Data/schema | `sql/schema.sql`, `sql/seed_data.sql`, `data/dealership.db` | SQLite-схема, демонстрационные данные, локальная runtime-база. |
| Documents/templates | `templates/`, `contracts/` | Шаблон договора и сгенерированные текстовые договоры. |
| Tests | `tests/smoke/`, `tests/unit/`, `tests/integration/` | Фиксация поведения, проверки reusable core и SQLite-сценариев. |
| Automation/build | `Makefile`, `pyproject.toml` | Единые команды запуска, тестов и сборки reusable core wheel. |
| Documentation | `README.md`, `docs/` | Инструкции запуска, спецификация, архитектура и будущие диаграммы/traceability. |

## Запускаемый слой

`main.py` намеренно оставлен маленьким

- импортирует `run_app` из `app.main_window`;
- объявляет `main()`;
- вызывает `main()` только в блоке `if __name__ == "__main__"`.

Такой entry point можно безопасно импортировать в тестах и вспомогательных инструментах - импорт `main` больше не создает Tkinter-окно и не открывает SQLite-базу.

`app/main_window.py` отвечает за создание корневого окна Tkinter, подключение к базе, инициализацию схемы и главное меню приложения. Он не хранит доменные правила сам, а передает действия в UI-модули таблиц и отчетов.

## GUI и прикладная логика

`app/ui_tables.py` отвечает за табличные окна и формы добавления, изменения и удаления записей. Через него пользователь работает с автомобилями, клиентами, сотрудниками, поставщиками, продажами, бронями, тест-драйвами и сервисом.

Ключевой сценарий продажи уже использует reusable core

- пользователь выбирает автомобиль;
- приложение проверяет, что автомобиль доступен для продажи;
- core-валидатор `validate_sale()` проверяет статус, цену и дату;
- после сохранения продажи SQLite-триггеры переводят автомобиль в статус `продана` и завершают активную бронь.

`app/ui_reports.py` отвечает за выбор отчета, ввод параметров и отображение результатов SQL-запроса. Сами SQL-запросы описаны в `app/config.py`, чтобы окно отчетов оставалось универсальным.

## Reusable core

Пакет `packages/dealership_core` содержит код, который не зависит от Tkinter, SQLite connection, путей проекта и файловой системы.

Сейчас в core находятся

- `format_money()` и `format_integer()` для пользовательского отображения чисел;
- `safe_contract_filename()` для безопасного имени файла договора;
- `ValidationError`;
- `validate_sale()`;
- `validate_reservation()`;
- `validate_test_drive()`.

Core проверяется unit-тестами и собирается отдельно от GUI

```bash
make build-lib
```

Команда создает wheel-артефакт в `dist/` стандартным Python-инструментом `build` по метаданным из `pyproject.toml`. Сборка не запускает Tkinter и не требует подключения к SQLite.

## Работа с SQLite

`app/database.py` отвечает за создание подключения и инициализацию базы

- `connect_db()` открывает SQLite-базу по пути из `app/config.py`;
- включает `PRAGMA foreign_keys = ON`;
- `init_db(conn)` применяет `sql/schema.sql`;
- при необходимости добавляет поля, которые появились после исходного прототипа;
- загружает seed-данные из `sql/seed_data.sql`, если таблица автомобилей пустая;
- добавляет демонстрационные брони, если база уже содержит автомобили.

SQLite-схема хранит не только таблицы, но и часть инвариантов

- `CHECK`-ограничения для статусов и неотрицательных чисел;
- `FOREIGN KEY`-связи между автомобилями, клиентами, сотрудниками и операциями;
- `UNIQUE` для продажи одного автомобиля только один раз;
- триггеры для смены статуса автомобиля после брони или продажи.

Такое разделение означает, что часть правил защищается на уровне reusable core, а часть остается на уровне базы данных как последний рубеж целостности.

## Договоры

`app/contracts.py` отвечает за сценарий договора продажи

1. Получает данные продажи, автомобиля, клиента и сотрудника через SQL-запрос.
2. Форматирует денежные значения и пробег через reusable core.
3. Читает шаблон `templates/contract_template.txt`.
4. Подставляет данные в шаблон.
5. Создает безопасное имя файла через `safe_contract_filename()`.
6. Сохраняет договор в `contracts/`.
7. Записывает относительный путь к файлу в `sales.contract_file`.

Текущий рендер договора еще находится в application layer, потому что он читает шаблон с диска и показывает preview через Tkinter. Возможное дальнейшее улучшение - вынести чистую функцию рендера в core.

## Автоматизация

Основные команды собраны в `Makefile`.

| Команда | Назначение |
| --- | --- |
| `make run` | Запускает Tkinter-приложение. |
| `make test` | Запускает automated tests через `unittest discover`. |
| `make check` | Основная локальная проверка проекта. Сейчас зависит от `test`. |
| `make install-build-tool` | Явно устанавливает стандартные инструменты сборки `build` и `setuptools`. |
| `make build-lib` | Собирает reusable core wheel без запуска GUI. |

`Makefile` выбирает `python` на Windows и `python3` на macOS/Linux. Это сделано после review, чтобы команды проверки были воспроизводимее для разных участников.

## Проверки

Текущая тестовая стратегия разделена по уровню

| Уровень | Папка | Что защищает |
| --- | --- | --- |
| Smoke | `tests/smoke/` | Инициализация SQLite, seed-данные, SQL-отчеты, рендер договора, безопасный импорт `main`. |
| Unit/negative | `tests/unit/` | Helper-функции и доменные валидаторы reusable core, включая ошибочные данные. |
| Integration | `tests/integration/` | SQLite-сценарии продаж и броней: статусы автомобилей, завершение броней, ограничения внешних ключей и уникальности. |

Тесты используют временную SQLite-базу в памяти и не зависят от локального `data/dealership.db`.

## Потоки выполнения

### Запуск приложения

```mermaid
sequenceDiagram
    participant User as Пользователь
    participant Main as main.py
    participant Window as app.main_window
    participant DB as app.database
    participant UI as Tkinter UI

    User->>Main: python main.py / make run
    Main->>Window: run_app()
    Window->>DB: connect_db()
    Window->>DB: init_db(conn)
    Window->>UI: создать главное окно и меню
    UI-->>User: показать приложение
```

### Продажа автомобиля

```mermaid
sequenceDiagram
    participant User as Пользователь
    participant Tables as app.ui_tables
    participant Core as dealership_core
    participant DB as SQLite
    participant Contracts as app.contracts

    User->>Tables: выбрать автомобиль и открыть форму продажи
    Tables->>Core: validate_sale(status, price, date)
    Core-->>Tables: ok или ValidationError
    Tables-->>User: показать форму с заполненными полями
    User->>Tables: сохранить форму продажи
    Tables->>DB: INSERT INTO sales
    DB-->>DB: set_car_sold_after_sale
    DB-->>DB: complete_reservation_after_sale
    Tables->>Contracts: save_contract_for_sale()
    Contracts->>DB: получить данные продажи
    Contracts->>DB: записать sales.contract_file
    Contracts-->>Tables: путь к файлу договора
    Tables-->>User: показать preview и сообщение
```

## Дальнейшее развитие

Текущая архитектура уже разделяет entry point, GUI, reusable core, SQLite и тесты. Следующие улучшения запланированы как отдельные небольшие PR, чтобы не смешивать архитектурные изменения, документацию и инфраструктуру.

Планируемые улучшения

- подключить `validate_reservation()` и `validate_test_drive()` к GUI-формам;
- вынести чистый рендер договора в reusable core;
- разделить в `app/database.py` подключение, инициализацию схемы, миграции и seed-логику;
- добавить Docker/Compose для воспроизводимых проверок;
- добавить traceability matrix и оформить editable diagrams.
