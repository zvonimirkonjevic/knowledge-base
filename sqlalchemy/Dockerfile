FROM python:3.12-slim

# psycopg2 builds from source, so it needs a full C toolchain (build-essential
# pulls in gcc + libc headers) plus the libpq headers.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY models.py seed.py ./

CMD ["uv", "run", "python", "seed.py"]
