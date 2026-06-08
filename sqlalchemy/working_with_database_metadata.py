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
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_adress", String, nullable=False)
)

# to create these tables on db we need to emit ddl
metadata_obj.create_all(engine)

#  
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

print(Base.metadata)
print(Base.registry)

# creating db tables using Declarative in ORM
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

# creating db tables on db by emitting ddl
Base.metadata.create_all(engine)
