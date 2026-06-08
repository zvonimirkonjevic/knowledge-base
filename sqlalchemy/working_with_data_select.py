# ========================
# Setup DB
# ========================

from sqlalchemy import create_engine

DB_URL = "postgresql://test:test@localhost/test_db"
engine = create_engine(DB_URL, echo=True)


from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String

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


from sqlalchemy import select
stmt = select(user_table).where(user_table.c.name == "Spongebob")
print(stmt)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)

from sqlalchemy.orm import DeclarativeBase, Session
class Base(DeclarativeBase):
    pass

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

Base.metadata.create_all(engine)

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
from sqlalchemy import func, cast
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
