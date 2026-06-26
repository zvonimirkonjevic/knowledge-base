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

# simple from clause
print(select(user_table.c.name))

# comma-separated from clause
print(select(user_table.c.name, address_table.c.email_address))

# join statement where we specify left and right side
print(
    select(user_table.c.name, address_table.c.email_address).join_from(
        user_table, address_table
    )
)

# join statement where we only specify right side
print(select(user_table.c.name, address_table.c.email_address).join(address_table))

# we can use select_from to modify clause if inffered one is not what we want
print(select(user_table.c.name, address_table.c.email_address).select_from(user_table).join(address_table))

# another use case for select_from is when our selected columns do not provide enough info for from clause
from sqlalchemy import func
print(select(func.count("*")).select_from(user_table))

# when we have multiple or no foreign keys between tables we need to specify on clause
print(
    select(address_table.c.email_address)
    .select_from(user_table)
    .join(address_table, user_table.c.id == address_table.c.user_id)
)

print(select(user_table).join(address_table, isouter=True))
print(select(user_table).join(address_table, full=True))

# simple order by clause
print(select(user_table).order_by(user_table.c.name))

# in ORM this way we choose asc or desc order
print(select(User).order_by(User.fullname.desc()))

# aggregate functions using group by/having
count_fn = func.count(user_table.c.id)
print(count_fn)

# simple example of group by and having clauses
with engine.connect() as conn:
    results = conn.execute(
        select(User.name, func.count(Address.id).label("count"))
        .join(Address)
        .group_by(User.name)
        .having(func.count(Address.id) > 1)
    )
    print(results.all())

from sqlalchemy import insert
with engine.connect() as conn:
    # add duplicated value for address
    conn.execute(insert(address_table).values(email_address="notspongebob@sqlalchemy.org", user_id=1))

    results = conn.execute(
        select(User.name, func.count(Address.id).label("count"))
        .join(Address)
        .group_by(User.name)
        .having(func.count(Address.id) > 1)
    )
    print(results.all())

from sqlalchemy import func, desc
stmt = (
    select(Address.user_id, func.count(Address.id).label("num_addresses")) # this selects user_id and number of addresses
    .group_by("user_id") # we group number of addresses by user_id, to get number of addresses per user
    .order_by("user_id", desc("num_addresses")) # this orders them by user_id and in descending order number of addresses
)
print(stmt)

# simple use of aliases
user_alias_1 = user_table.alias()
user_alias_2 = user_table.alias()
print(
    select(user_alias_1.c.name, user_alias_2.c.name).join_from(
        user_alias_1, user_alias_2, user_alias_1.c.id > user_alias_2.c.id
    )
)

# simple use of aliases in ORM
from sqlalchemy.orm import aliased
address_alias_1 = aliased(Address)
address_alias_2 = aliased(Address)

# we do not have these entires as each script is indepenedent on other scripts from tutorial
from sqlalchemy.orm import Session
with Session(engine) as session:
    patrick_aol = Address(email_address="patrick@aol.com", user_id=3)
    patrick_gmail = Address(email_address="patric@gmail.com", user_id=3)
    session.add(patrick_aol)
    session.add(patrick_gmail)
    session.commit()

print(
    select(User) # select whole user object
    .join_from(User, address_alias_1) # join user and address table on foreign key
    .where(address_alias_1.email_address == "patrick@aol.com") # add clause to join users whos email is this value
    .join_from(User, address_alias_2) # do another join on foreign key
    .where(address_alias_2.email_address == "patrick@gmail.com") # add clause to join users whos email is this value
    # this is single query with and between two where clauses
)
