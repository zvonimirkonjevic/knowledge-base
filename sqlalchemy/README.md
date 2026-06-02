# SQLAlchemy Tutorial

Working through the [SQLAlchemy 2.0 Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

## Setup

Requires Docker and [uv](https://docs.astral.sh/uv/).

Start the PostgreSQL database:

```bash
docker compose up -d
```

Install dependencies:

```bash
uv sync
```

## Files

| File | Tutorial Section |
|------|-----------------|
| [working_with_transactions_and_dbapi.py](working_with_transactions_and_dbapi.py) | [Working with Transactions and the DBAPI](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html) |

## Database

PostgreSQL running via Docker:

- **Host:** `localhost:5432`
- **User/Password:** `test` / `test`
- **Database:** `test_db`
