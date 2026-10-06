FROM docker.io/library/python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /ingestion

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src ./src
CMD ["uv", "run", "--no-dev", "ingestion"]
