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
# Select Statement
# ========================

stmt = select(User).where(User.name == "Spongebob")
with Session(engine) as session:
    for row in session.execute(stmt):
        print(row)

# three ways of creating select from statement (Core)
print(select(user_table))

print(select(user_table.c.name, user_table.c.fullname))

print(select(user_table.c["name", "fullname"]))

# select from statement (ORM)
print(select(User))

with Session(engine) as session:
    row = session.execute(select(User)).first()
    print(row[0])

    user = session.scalars(select(User)).first()
    print(user)

print(select(User.name, User.fullname))

with Session(engine) as session:
    row = session.execute(select(User.name, User.fullname)).first()
    print(row)

    session.execute(
        select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
    ).all()

# selecting from labeled sql expressions
stmt = select(
    ("Username: " + user_table.c.name).label("username"),
).order_by(user_table.c.name)
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row.username)

# selecting with text() column expression
from sqlalchemy import text
stmt = select(
    text("'some_phrase'"), user_table.c.name 
).order_by(user_table.c.name)
with engine.connect() as conn:
    print(conn.execute(stmt).all())

# literal_column() instead of text()
from sqlalchemy import literal_column
stmt = select(
    literal_column("'some phrase'").label("p"), user_table.c.name
).order_by(user_table.c.name)
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(f"{row.p}, {row.name}")

print(user_table.c.name == "Patrick")
print(address_table.c.user_id > 10)

# simple where clause
print(select(user_table).where(user_table.c.name == "Spongebob"))

# chaining multiple where clauses
print(
    select(address_table.c.email_address)
    .where(user_table.c.name == "Patrick")
    .where(address_table.c.user_id == user_table.c.id)
)

# chaining multiple rules inside single where clause
print(
    select(address_table.c.email_address)
    .where(
        user_table.c.name == "Patrick",
        address_table.c.user_id == user_table.c.id
    )
)

# we can also directly use and_() and or_()
from sqlalchemy import and_, or_
print(
    select(address_table).where(
        and_(
            or_(user_table.c.name == "Spongebob", user_table.c.name == "Sandy"),
            address_table.c.user_id == user_table.c.id
        )
    )
)

# we can use .filter_by as shortcut instead of writing long .where for simple equality comparisons
print(select(User).filter_by(name="Spongebob", fullname="Spongebob Squarepants"))
