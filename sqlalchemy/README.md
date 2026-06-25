# SQLAlchemy Tutorial

Working through the [SQLAlchemy 2.0 Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

## Setup

Requires Docker and [uv](https://docs.astral.sh/uv/).

Start PostgreSQL and seed the schema + tutorial data:

```bash
docker compose up --build -d
```

This starts the `db` service and runs the `seed` service once the database is
healthy. The `seed` service ([seed.py](seed.py)) creates the tables and loads
the canonical tutorial rows, so the data scripts have something to work against.
Re-running `docker compose up` re-seeds a clean schema.

Install dependencies (for running the scripts on the host):

```bash
uv sync
```

## Files

| File | Tutorial Section |
|------|-----------------|
| [models.py](models.py) | Shared engine + table/ORM definitions (DB setup) |
| [seed.py](seed.py) | Builds the schema and loads tutorial data (runs in docker compose) |
| [working_with_transactions_and_dbapi.py](working_with_transactions_and_dbapi.py) | [Working with Transactions and the DBAPI](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html) |

## Database

PostgreSQL running via Docker:

- **Host:** `localhost:5432`
- **User/Password:** `test` / `test`
- **Database:** `test_db`
