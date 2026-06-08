# ========================
# Setup DB
# ========================

from sqlalchemy import create_engine

DB_URL = "postgresql://test:test@localhost/test_db"
engine = create_engine(DB_URL, echo=True)



DB_URL = "postgresql://test:test@localhost/test_db"
engine = create_engine(DB_URL, echo=True)

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String

# create all tables used in third section
metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String)
)

from sqlalchemy import ForeignKey

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False)
)

metadata_obj.create_all(engine)

# ========================
# Insert Statement
# ========================

from sqlalchemy import insert

stmt = insert(user_table).values(name="Spongebob", fullname="Spongebob Squarepants")
print(stmt)

compiled = stmt.compile()
print(compiled.params)

# executing statement
with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()

print(result.inserted_primary_key)
print(insert(user_table))

# insert without specific .values clause
with engine.connect() as conn:
    result = conn.execute(
        insert(user_table),
        [
            {"name":"Sandy", "fullname": "Sandy Cheecks"},
            {"name": "Patrick", "fullname": "Patrick Star"}
        ],
    )
    conn.commit()

# deep alchemy trick of inserting data, using subquery and bindparam
# simpler than fetching all user_ids, storing them and then doing another call to write into table based on fetched user_ids
from sqlalchemy import select, bindparam

scalar_subq = (
    select(user_table.c.id)
    .where(user_table.c.name == bindparam("username"))
    .scalar_subquery()
)

with engine.connect() as conn:
    result = conn.execute(
        insert(address_table).values(user_id=scalar_subq),
        [
            {"username": "Spongebob", "email_address": "spongebob@sqlalchemy.org"},
            {"username": "Sandy", "email_address": "sandy@sqlalchemy.org"},
            {"username": "Patrick", "email_address": "patrick@sqlalchemy.org"}
        ],
    )
    conn.commit()

# insert default values
print(insert(user_table).values().compile(engine))

# insert with returning
stmt = insert(address_table).returning(
    address_table.c.id, address_table.c.email_address
)
print(stmt)

# insert with returning combined with from select
select_stmt = select(
    user_table.c.id, user_table.c.name + "@aol.com"
)
insert_stmt = insert(address_table).from_select(
    ["user_id", "email_address"], select_stmt
)
print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))
