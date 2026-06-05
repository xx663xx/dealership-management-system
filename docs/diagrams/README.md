# Диаграммы проекта

Папка хранит редактируемые исходники диаграмм и PNG-экспорты для отчетов и просмотра. Исходниками считаются `.drawio.xml` файлы и DBML-файл ERD; PNG лежат отдельно в `exports/` и не редактируются вручную.

## Индекс

| Диаграмма | Исходник | PNG-превью | Используется в документах |
| --- | --- | --- | --- |
| IDEF0 context A-0 | `idefA-0_context.drawio.xml` | `exports/idefA-0_context.png` | `docs/architecture.md` |
| IDEF0 decomposition A0 | `idefA0_decomposition.drawio.xml` | `exports/idefA0_decomposition.png` | `docs/architecture.md` |
| IDEF0 sale decomposition A4 | `idefA4_decomposition.drawio.xml` | `exports/idefA4_decomposition.png` | `docs/architecture.md` |
| Use-case overview | `use-cases.drawio.xml` | `exports/use-cases.png` | `docs/specification.md`, `docs/architecture.md` |
| App startup sequence | `app-startup-sequence.drawio.xml` | `exports/app-startup-sequence.png` | `docs/architecture.md`, `docs/developer-guide.md` |
| Sales sequence | `sales-sequence.drawio.xml` | `exports/sales-sequence.png` | `docs/specification.md`, `docs/architecture.md` |
| SQLite ERD | `schema.dbml` | `exports/schema.png` | `docs/architecture.md` |

`schema.dbml` хранит редактируемый исходник ERD для dbdiagram.io, а `schema.png` сохранен как PNG-превью этой схемы. Исполняемым source of truth для SQLite-ограничений, триггеров и создания таблиц остается `sql/schema.sql`.

## PNG-экспорты

| Файл | Назначение |
| --- | --- |
| `exports/idefA-0_context.png` | PNG-превью контекстной IDEF0-диаграммы. |
| `exports/idefA0_decomposition.png` | PNG-превью декомпозиции A0. |
| `exports/idefA4_decomposition.png` | PNG-превью декомпозиции A4. |
| `exports/use-cases.png` | PNG-превью use-case диаграммы. |
| `exports/app-startup-sequence.png` | PNG-превью sequence diagram запуска приложения. |
| `exports/sales-sequence.png` | PNG-превью sequence diagram продажи автомобиля. |
| `exports/schema.png` | PNG-превью ERD SQLite-схемы. |

## Проверка

Проверить документацию и наличие diagram sources/exports:

```bash
make docs
```

Проверить XML-файлы напрямую:

```bash
xmllint --noout docs/diagrams/*.drawio.xml
```

DBML-исходник ERD можно открыть или импортировать в dbdiagram.io:

```bash
docs/diagrams/schema.dbml
```

Если установлен draw.io CLI, можно пересобрать PNG-превью:

```bash
drawio --export --format png --output docs/diagrams/exports/idefA-0_context.png docs/diagrams/idefA-0_context.drawio.xml
drawio --export --format png --output docs/diagrams/exports/idefA0_decomposition.png docs/diagrams/idefA0_decomposition.drawio.xml
drawio --export --format png --output docs/diagrams/exports/idefA4_decomposition.png docs/diagrams/idefA4_decomposition.drawio.xml
drawio --export --format png --output docs/diagrams/exports/use-cases.png docs/diagrams/use-cases.drawio.xml
drawio --export --format png --output docs/diagrams/exports/app-startup-sequence.png docs/diagrams/app-startup-sequence.drawio.xml
drawio --export --format png --output docs/diagrams/exports/sales-sequence.png docs/diagrams/sales-sequence.drawio.xml
```
