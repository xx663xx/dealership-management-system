# Диаграммы проекта

Папка хранит редактируемые исходники диаграмм и PNG-экспорты для отчетов и просмотра. Исходниками считаются `.drawio.xml` файлы; PNG лежат отдельно в `exports/` и не редактируются вручную.

## Исходники

| Файл | Назначение |
| --- | --- |
| `idefA-0_context.drawio.xml` | Контекстная IDEF0-диаграмма A-0: границы работы автосалона, входы, выходы, управление и механизмы. |
| `idefA0_decomposition.drawio.xml` | Декомпозиция A0: основные процессы автосалона от учета автомобилей до сервиса и отчетов. |
| `idefA4_decomposition.drawio.xml` | Декомпозиция A4: сценарий продажи автомобиля, включая подбор, бронирование, договор и обновление статуса. |
| `use-cases.drawio.xml` | Use-case overview: роли пользователей, клиентские сценарии, сервисные сценарии и проверки проекта. |
| `app-startup-sequence.drawio.xml` | Sequence diagram запуска приложения: `main.py`, `app.main_window`, `app.database`, Tkinter UI. |
| `sales-sequence.drawio.xml` | Sequence diagram продажи автомобиля: core-валидация, `INSERT INTO sales`, SQLite-триггеры, договор. |

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

Если установлен draw.io CLI, можно пересобрать PNG-превью:

```bash
drawio --export --format png --output docs/diagrams/exports/idefA-0_context.png docs/diagrams/idefA-0_context.drawio.xml
drawio --export --format png --output docs/diagrams/exports/idefA0_decomposition.png docs/diagrams/idefA0_decomposition.drawio.xml
drawio --export --format png --output docs/diagrams/exports/idefA4_decomposition.png docs/diagrams/idefA4_decomposition.drawio.xml
drawio --export --format png --output docs/diagrams/exports/use-cases.png docs/diagrams/use-cases.drawio.xml
drawio --export --format png --output docs/diagrams/exports/app-startup-sequence.png docs/diagrams/app-startup-sequence.drawio.xml
drawio --export --format png --output docs/diagrams/exports/sales-sequence.png docs/diagrams/sales-sequence.drawio.xml
```
