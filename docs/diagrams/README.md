# Диаграммы проекта

Папка хранит редактируемые исходники диаграмм в формате diagrams.net / Draw.io XML. Эти файлы можно открыть в draw.io desktop или на app.diagrams.net и изменить без перерисовки схем с нуля.

## Состав

| Файл | Назначение |
| --- | --- |
| `idefA-0_context.drawio.xml` | Контекстная IDEF0-диаграмма A-0: границы работы автосалона, входы, выходы, управление и механизмы. |
| `idefA0_decomposition.drawio.xml` | Декомпозиция A0: основные процессы автосалона от учета автомобилей до сервиса и отчетов. |
| `idefA4_decomposition.drawio.xml` | Декомпозиция A4: сценарий продажи автомобиля, включая подбор, бронирование, договор и обновление статуса. |

PNG-версии этих схем используются в отчете и хранятся отдельно в `screenshots/`. Исходниками считаются именно файлы из `docs/diagrams/`.

## Проверка

Проверить, что XML-файлы корректно разбираются:

```bash
xmllint --noout docs/diagrams/*.drawio.xml
```

Если установлен draw.io CLI, можно экспортировать превью:

```bash
drawio --export --format png --output /tmp/idefA-0_context.png docs/diagrams/idefA-0_context.drawio.xml
drawio --export --format png --output /tmp/idefA0_decomposition.png docs/diagrams/idefA0_decomposition.drawio.xml
drawio --export --format png --output /tmp/idefA4_decomposition.png docs/diagrams/idefA4_decomposition.drawio.xml
```

Эти команды не обязательны для запуска приложения, но помогают проверить, что диаграммы остаются воспроизводимыми.
