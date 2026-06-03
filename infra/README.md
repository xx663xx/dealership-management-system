# Контейнерная проверка

Проект является desktop-приложением на Tkinter, поэтому графический интерфейс запускается локально командой `make run`.

Docker и Compose используются для воспроизводимой проверки без открытия GUI:

```bash
docker build -t car-dealership-checks:local .
docker run --rm car-dealership-checks:local
docker compose -f infra/compose.yaml run --rm checks
docker compose -f infra/compose.yaml down
```

Контейнер запускает автоматические тесты и собирает reusable core wheel без открытия Tkinter-окна.

Образ использует полный `python:3.11`, а не `python:3.11-slim`. Проверки не открывают GUI, но тесты импортируют модули приложения, которые импортируют `tkinter`. В slim-образе нет Tk-библиотек, необходимых для такого импорта.

Compose использует команду по умолчанию из `Dockerfile`, поэтому команда non-GUI проверки описана в одном месте.
