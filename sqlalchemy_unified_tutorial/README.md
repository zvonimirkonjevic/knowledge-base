# SQLAlchemy Tutorial

Working through the [SQLAlchemy 2.0 Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html).

## Setup

Requires Docker and [uv](https://docs.astral.sh/uv/).

Start PostgreSQL and seed the schema + tutorial data:

```bash
docker compose up --build -d
```

This starts the `db` service and runs the `seed` service once the database is
healthy. The `seed` service ([scripts/seed.py](scripts/seed.py)) creates the
tables and loads the canonical tutorial rows, so the section scripts have
something to work against. Re-running `docker compose up` re-seeds a clean
schema.

Install dependencies (for running the scripts on the host):

```bash
uv sync
```

Run a section script as a module from the project root, so `from models import
...` resolves:

```bash
uv run python -m sections.working_with_data_insert
```

## Layout

- [models/](models/) — shared engine + table/ORM definitions (DB setup).
- [scripts/](scripts/) — utility scripts (schema build + data seeding).
- [sections/](sections/) — one script per tutorial section.

## Files

| File | Tutorial Section |
|------|-----------------|
| [models/models.py](models/models.py) | Shared engine + table/ORM definitions (DB setup) |
| [scripts/seed.py](scripts/seed.py) | Builds the schema and loads tutorial data (runs in docker compose) |
| [sections/working_with_transactions_and_dbapi.py](sections/working_with_transactions_and_dbapi.py) | [Working with Transactions and the DBAPI](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html) |
| [sections/working_with_database_metadata.py](sections/working_with_database_metadata.py) | [Working with Database Metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html) |
| [sections/working_with_data_insert.py](sections/working_with_data_insert.py) | [Working with Data — Using INSERT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_insert.html) |
| [sections/working_with_data_select.py](sections/working_with_data_select.py) | [Working with Data — Using SELECT Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html) |
| [sections/working_with_data_update_delete.py](sections/working_with_data_update_delete.py) | [Working with Data — Using UPDATE and DELETE Statements](https://docs.sqlalchemy.org/en/20/tutorial/data_update.html) |
| [sections/data_manipulation_with_orm.py](sections/data_manipulation_with_orm.py) | [Data Manipulation with the ORM](https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html) |
| [sections/working_with_orm_related_objects.py](sections/working_with_orm_related_objects.py) | [Working with ORM Related Objects](https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html) |

## Database

PostgreSQL running via Docker:

- **Host:** `localhost:5432`
- **User/Password:** `test` / `test`
- **Database:** `test_db`
