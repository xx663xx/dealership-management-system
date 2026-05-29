# Матрица соответствия требований

## Назначение

Этот документ связывает требования учебного проекта с конкретными файлами, тестами, командами проверки и Pull Request. Он нужен, чтобы проверяющий мог быстро увидеть, какие требования уже закрыты, чем они подтверждаются и что еще остается в работе.

Статусы:

- `Done` - требование уже отражено в `main`.
- `In review` - изменение готово отдельной веткой/PR, но еще не смержено в `main`.
- `Planned` - требование еще не реализовано или не оформлено в Git.

## Ключевые требования

| Требование | Где реализовано | Чем проверяется | PR / история | Статус |
| --- | --- | --- | --- | --- |
| Честный baseline существующего Tkinter-прототипа | `main.py`, `app/`, `sql/`, `templates/`, `screenshots/` | Ручной запуск, последующие smoke-тесты | Initial import `a3d16c6`; PR #1 | Done |
| Нормальная Git-история через ветки и PR | GitHub Pull Requests, merge commits в `main` | История `main`, review/approve/request changes | PR #1-#7 | Done |
| Локальная память и служебные файлы не попадают в Git | `.gitignore` | `git status --short --ignored` | PR #1 / baseline fixes | Done |
| Smoke-тесты фиксируют текущее поведение до рефакторинга | `tests/smoke/test_database_smoke.py` | `make check` | PR #1 | Done |
| Entry point можно безопасно импортировать | `main.py`, `tests/smoke/test_main_entrypoint.py` | `make check` | PR #5 | Done |
| `main.py` является тонкой точкой входа | `main.py`, `app/main_window.py` | `make check`, review архитектуры | PR #5 | Done |
| Запускаемый Tkinter-слой отделен от reusable core | `app/main_window.py`, `app/ui_tables.py`, `packages/dealership_core/` | `make check`, unit/smoke tests | PR #2, PR #3, PR #5 | Done |
| Reusable core содержит чистые helper-функции | `packages/dealership_core/helpers.py` | `tests/unit/test_core_helpers.py`, `make check` | PR #2 | Done |
| Reusable core содержит доменные валидаторы | `packages/dealership_core/validators.py` | `tests/unit/test_core_validators.py`, `make check` | PR #3 | Done |
| Продажа использует core-валидацию доступности автомобиля | `app/ui_tables.py`, `packages/dealership_core/validators.py` | `tests/unit/test_core_validators.py`, manual GUI flow | PR #3 | Done |
| SQLite-сценарии продаж и броней покрыты integration tests | `tests/integration/test_sqlite_sales_reservations.py`, `sql/schema.sql` | `make check` | PR #4 | Done |
| База создается из SQL-схемы и seed-данных | `app/database.py`, `sql/schema.sql`, `sql/seed_data.sql` | `tests/smoke/test_database_smoke.py`, `make check` | PR #1 | Done |
| SQL constraints и triggers защищают целостность данных | `sql/schema.sql` | smoke/integration tests | PR #1, PR #4 | Done |
| Договор продажи формируется по шаблону | `app/contracts.py`, `templates/contract_template.txt` | `tests/smoke/test_database_smoke.py`, `make check` | PR #1, PR #2 | Done |
| Безопасное имя файла договора вынесено в reusable core | `packages/dealership_core/helpers.py`, `app/contracts.py` | `tests/unit/test_core_helpers.py`, `make check` | PR #2 | Done |
| Единая команда проверки проекта | `Makefile` | `make check` | PR #1, PR #6 | Done |
| Reusable core можно собрать отдельно от GUI | `pyproject.toml`, `scripts/build_core_wheel.py`, `Makefile` | `make build-lib` | PR #6 | Done |
| Сборка reusable core не зависит от reviewer-specific venv tooling | `scripts/build_core_wheel.py`, `Makefile` | `make build-lib` на macOS/Windows review | PR #6 fix `cef85cb` | Done |
| Спецификация предметной области оформлена отдельно | `docs/specification.md` | Documentation review, `make check` | PR #7 | Done |
| Архитектурное описание проекта оформлено отдельно | `docs/architecture.md` | Documentation review, `make check` | PR #8 | Done |
| Диаграммы хранятся в редактируемом виде | `docs/diagrams/` | Проверка наличия исходников `.mmd`/`.drawio` и совпадения с кодом | Not merged yet | Planned |
| README является полной точкой входа | `README.md` | Fresh-clone/manual verification | Partial updates in PR #1 and PR #6 | Planned |
| Документация для разработчика | Planned: `docs/developer-guide.md` | Review, fresh-clone workflow | Not started | Planned |
| Docker/Compose для воспроизводимых проверок | Planned: `Dockerfile`, `.dockerignore`, `infra/compose.yaml` | `docker build`, `docker compose` / `make compose-check` | Not started | Planned |
| Команда сборки документации | Planned: `make docs` or equivalent | `make docs` | Not started | Planned |
| Отчет о покрытии тестами | Planned: coverage tooling / `make coverage` | `make coverage` | Not started | Planned |

## Проверки по областям

| Область | Основные файлы | Основная команда |
| --- | --- | --- |
| Smoke tests | `tests/smoke/` | `make check` |
| Unit and negative tests | `tests/unit/` | `make check` |
| SQLite integration tests | `tests/integration/` | `make check` |
| Reusable core build | `packages/dealership_core/`, `scripts/build_core_wheel.py` | `make build-lib` |
| Tkinter runtime | `main.py`, `app/main_window.py`, `app/ui_tables.py`, `app/ui_reports.py` | `make run` |
| Documentation | `README.md`, `docs/specification.md`, `docs/architecture.md` | Review + `make check` |

## Открытые gaps

На текущем этапе проект уже имеет тесты, reusable core, thin entrypoint, packaging-команду и спецификацию. До финальной сдачи еще нужно закрыть:

- оформить editable diagrams как tracked artifacts;
- добавить `docs/developer-guide.md`;
- довести README до полного fresh-clone сценария;
- добавить Docker/Compose для воспроизводимых проверок;
- добавить `make docs` и, при необходимости, `make coverage`;
- подключить `validate_reservation()` и `validate_test_drive()` к GUI-формам или явно оставить это как documented future work.