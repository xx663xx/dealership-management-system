# syntax=docker/dockerfile:1

FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/workspace

WORKDIR /workspace

COPY app/ app/
COPY packages/ packages/
COPY sql/ sql/
COPY templates/ templates/
COPY tests/ tests/
COPY main.py pyproject.toml README.md ./

RUN python -m pip install "build>=1.2" "setuptools>=68"

CMD ["sh", "-c", "python -m unittest discover -s tests && python -m build --wheel --no-isolation"]
