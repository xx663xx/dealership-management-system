# syntax=docker/dockerfile:1

FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/workspace

WORKDIR /workspace

COPY app/ app/
COPY packages/ packages/
COPY scripts/ scripts/
COPY sql/ sql/
COPY templates/ templates/
COPY tests/ tests/
COPY main.py pyproject.toml README.md ./

CMD ["sh", "-c", "python -m unittest discover -s tests && python scripts/build_core_wheel.py"]
