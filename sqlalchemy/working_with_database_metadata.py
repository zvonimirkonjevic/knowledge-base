from sqlalchemy import create_engine, text

DB_URL = "postgresql://test:test@localhost/test_db"
engine = create_engine(DB_URL, echo=True)

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String

# to be able to create tables first we need metadata object which will contain all tables created with table names as keys
metadata_obj = MetaData()

# create simple user_account table
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String)
)

# accessing table parameters
print(user_table.c.name)
print(user_table.c.keys())
print(user_table.primary_key)

from sqlalchemy import ForeignKey

# defining table with foreign key and not nullable constraints
adress_table = Table(
    "adress",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_adress", String, nullable=False)
)

# to create these tables on db we need to emit ddl
metadata_obj.create_all(engine)
