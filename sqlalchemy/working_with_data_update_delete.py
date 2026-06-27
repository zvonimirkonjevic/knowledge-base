# DB setup (engine + tables + ORM models) lives in models.py and is created
# and populated by seed.py, which runs via `docker compose up`.
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import engine, user_table, address_table, User, Address

stmt = select(user_table).where(user_table.c.name == "Spongebob")
print(stmt)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)

# ========================
# Update Statement
# ========================

# simple update statement
from sqlalchemy import update
stmt = (
    update(user_table)
    .where(user_table.c.name == "patrick")
    .values(fullname="Patrick the Star")
)
print(stmt)

# simple update against expression
stmt = update(user_table).values(fullname="Username: " + user_table.c.name)
print(stmt)

# simple update of many values in single statement
from sqlalchemy import bindparam
stmt = (
    update(user_table)
    .where(user_table.c.name == bindparam("oldname"))
    .values(name=bindparam("newname"))
)
with engine.begin() as conn:
    conn.execute(
        stmt,
        [
            {"oldname": "jack", "newname": "ed"},
            {"oldname": "wendy", "newname": "mary"},
            {"oldname": "jim", "newname": "jake"},
        ],
    )

# simple correlated update
scalar_subq = (
    select(address_table.c.email_address)
    .where(address_table.c.user_id == user_table.c.id)
    .order_by(address_table.c.id)
    .limit(1)
    .scalar_subquery()
)
update_stmt = update(user_table).values(fullname=scalar_subq)
print(update_stmt)

# simple update from statement
update_stmt = (
    update(user_table)
    .where(user_table.c.id == address_table.c.user_id)
    .where(address_table.c.email_address == "patrick@aol.com")
    .values(fullname="Pat")
)
print(update_stmt)

# mysql specific syntax for updating values in multiple tables
update_stmt = (
    update(user_table)
    .where(user_table.c.id == address_table.c.user_id)
    .where(address_table.c.email_address == "patrick@aol.com")
    .values(
        {
            user_table.c.fullname: "Pat",
            address_table.c.email_address: "pat@aol.com",
        }
    )
)
from sqlalchemy.dialects import mysql
print(update_stmt.compile(dialect=mysql.dialect()))

# updating multiple rows in db using single update statement and values construct
from sqlalchemy import Values
values = Values(
    user_table.c.id,
    user_table.c.name,
    name="my_values"
).data([(1, "new_name"), (2, "another_name"), ("3", "name_name")])

update_stmt = (
    user_table.update().values(name=values.c.name).where(user_table.c.id == values.c.id)
)

from sqlalchemy.dialects import postgresql
print(update_stmt.compile(dialect=postgresql.dialect()))

# simple delete statement
from sqlalchemy import delete
stmt = delete(user_table).where(user_table.c.name == "Patrick")
print(stmt)

# mutlitple table deletes in mysql
delete_stmt = (
    delete(user_table)
    .where(user_table.c.id == address_table.c.user_id)
    .where(address_table.c.email_address == "patrick@aol.com")
)
from sqlalchemy.dialects import mysql
print(delete_stmt.compile(dialect=mysql.dialect()))

# getting affected row count from update and delete
with engine.begin() as conn:
    result = conn.execute(
        update(user_table)
        .values(fullname="Patrick McStar")
        .where(user_table.c.name == "Patrick")
    )
    print(result.rowcount)

# simple use of returning clause
update_stmt = (
    update(user_table)
    .where(user_table.c.name == "Patrick")
    .values(fullname="Patrick the Star")
    .returning(user_table.c.id, user_table.c.name)
)
print(update_stmt)

delete_stmt = (
    delete(user_table)
    .where(user_table.c.name == "Patrick")
    .returning(user_table.c.id, user_table.c.name)
)
print(delete_stmt)
