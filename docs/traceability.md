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
| Reusable core можно собрать отдельно от GUI | `pyproject.toml`, `Makefile` | `make install-build-tool`, `make build-lib` | PR #6; standard build update | Done |
| Сборка reusable core использует стандартный Python build workflow | `pyproject.toml`, `Makefile` | `make install-build-tool`, `make build-lib` | PR #18 | Done |
| Спецификация предметной области оформлена отдельно | `docs/specification.md` | Documentation review, `make check` | PR #7 | Done |
| Архитектурное описание проекта оформлено отдельно | `docs/architecture.md` | Documentation review, `make check` | PR #8 | Done |
| Диаграммы хранятся в редактируемом виде | `docs/diagrams/*.drawio.xml`, `docs/diagrams/README.md` | `xmllint --noout docs/diagrams/*.drawio.xml`, экспорт через draw.io CLI | PR #11 | Done |
| README является полной точкой входа | `README.md` | Fresh-clone/manual verification, `make check`, `make install-build-tool`, `make build-lib` | Current README PR | In review |
| Документация для разработчика | `docs/developer-guide.md` | Review, fresh-clone workflow, `make check`, `make build-lib` | PR #10 | Done |
| Docker/Compose для воспроизводимых проверок | `Dockerfile`, `.dockerignore`, `.env.example`, `infra/compose.yaml`, `infra/README.md` | `docker build`, `docker run`, `docker compose -f infra/compose.yaml run --rm checks` | PR #18 | Done |
| Команда сборки документации | Planned: `make docs` or equivalent | `make docs` | Not started | Planned |
| Отчет о покрытии тестами | Planned: coverage tooling / `make coverage` | `make coverage` | Not started | Planned |

## Проверки по областям

| Область | Основные файлы | Основная команда |
| --- | --- | --- |
| Smoke tests | `tests/smoke/` | `make check` |
| Unit and negative tests | `tests/unit/` | `make check` |
| SQLite integration tests | `tests/integration/` | `make check` |
| Reusable core build | `packages/dealership_core/`, `pyproject.toml` | `make build-lib` |
| Container non-GUI checks | `Dockerfile`, `infra/compose.yaml`, `infra/README.md` | `docker compose -f infra/compose.yaml run --rm checks` |
| Tkinter runtime | `main.py`, `app/main_window.py`, `app/ui_tables.py`, `app/ui_reports.py` | `make run` |
| Documentation | `README.md`, `docs/specification.md`, `docs/architecture.md` | Review + `make check` |

## Что осталось сделать

На текущем этапе проект уже имеет тесты, reusable core, thin entrypoint, packaging-команду, Docker/Compose, спецификацию, архитектурное описание, traceability и редактируемые диаграммы. Перед защитой остаются дополнительные улучшения автоматизации:

- добавить `make docs`;
- добавить `make coverage`.