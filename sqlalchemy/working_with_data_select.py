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

# simple subquery
subq = (
    select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
    .group_by(address_table.c.user_id)
    .subquery()
)
print(subq)
print(select(subq.c.user_id, subq.c.count))

# using subquery in statement
stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(
    user_table, subq
)
print(stmt)

# simple cte
subq = (
    select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
    .group_by(address_table.c.user_id)
    .cte()
)

stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(
    user_table, subq
)
print(stmt)

# subquery in ORM
subq = select(Address).where(~Address.email_address.like("%@aol.com")).subquery()
address_subq = aliased(Address, subq)
stmt = (
    select(User, address_subq)
    .join_from(User, address_subq)
    .order_by(User.id, address_subq.id)
)
with Session(engine) as session:
    for user, address in session.execute(stmt):
        print(f"{user} {address}")

# cte in ORM
cte_obj = select(Address).where(~Address.email_address.like("%@aol.com")).cte()
address_cte = aliased(Address, cte_obj)
stmt = (
    select(User, address_cte)
    .join_from(User, address_cte)
    .order_by(User.id, address_cte.id)
)
with Session(engine) as session:
    for user, address in session.execute(stmt):
        print(f"{user} {address}")

# simple scalar subquery
subq = (
    select(func.count(address_table.c.id))
    .where(user_table.c.id == address_table.c.user_id)
    .scalar_subquery()
)
print(subq)

# even though subquery contains both tables in from clause, when used in enclosing select statement it is correlated and not inside from clause
stmt = select(user_table.c.name, subq.label("address_count"))
print(stmt)

# in the case where the correlation is ambiguous, sqlalchemy will let us know that more clarity is needed
#stmt = (
#    select(
#        user_table.c.name,
#        address_table.c.email_address,
#        subq.label("address_count"),
#    )
#    .join_from(user_table, address_table)
#    .order_by(user_table.c.id, address_table.c.id)
#)
#print(stmt)

# to specify by what we want to correlate we use .correlate()
subq = (
    select(func.count(address_table.c.id))
    .where(user_table.c.id == address_table.c.user_id)
    .scalar_subquery()
    .correlate(user_table)
)

# this query counts how many emails does user have, 
# then we select user name, their email address and number of emails
# we join them as we take data from two different tables
with engine.connect() as conn:
    result = conn.execute(
        select(
            user_table.c.name,
            address_table.c.email_address,
            subq.label("address_count"),
        )
        .join_from(user_table, address_table)
        .order_by(user_table.c.id, address_table.c.id)
    )
    print(result.all())

# defining lateral correlation
subq = (
    select(
        func.count(address_table.c.id).label("address_count"),
        address_table.c.email_address,
        address_table.c.user_id,
    )
    .where(user_table.c.id == address_table.c.user_id)
    .lateral()
)

# here we can see that our lateral correlation above
# allows us to get user_table.c.id inside subquery that is on the right side of join clause
stmt = (
    select(user_table.c.name, subq.c.address_count, subq.c.email_address)
    .join_from(user_table, subq)
    .order_by(user_table.c.id, subq.c.email_address)
)
print(stmt)

# simple union all statement
from sqlalchemy import union_all
stmt1 = select(user_table).where(user_table.c.name == "Sandy")
stmt2 = select(user_table).where(user_table.c.name == "Spongebob")
u = union_all(stmt1, stmt2)
with engine.connect() as conn:
    result = conn.execute(u)
    print(result.all())

# subquery from union
u_subq = u.subquery()
stmt = (
    select(u_subq.c.name, address_table.c.email_address)
    .join_from(address_table, u_subq)
    .order_by(u_subq.c.name, address_table.c.email_address)
)

with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.all())

# simple union on ORM objects
stmt1 = select(User).where(User.name == "Sandy")
stmt2 = select(User).where(User.name == "Spongebob")
u = union_all(stmt1, stmt2)

orm_stmt = select(User).from_statement(u)
with Session(engine) as session:
    for obj in session.execute(orm_stmt).scalars():
        print(obj)

# subquery from union in ORM
user_alias = aliased(User, u.subquery())
orm_stmt = select(user_alias).order_by(user_alias.id) # by creating subquery we can now use order_by
with Session(engine) as session:
    for obj in session.execute(orm_stmt).scalars():
        print(obj)

# simple exists keyword 
subq = (
    select(func.count(address_table.c.id))
    .where(user_table.c.id == address_table.c.user_id)
    .group_by(address_table.c.user_id)
    .having(func.count(address_table.c.id) > 1)
).exists()

with engine.connect() as conn:
    result = conn.execute(select(user_table.c.name).where(subq))
    print(result.all())

# simple not exists keyword
subq = (
    select(address_table.c.id).where(user_table.c.id == address_table.c.user_id)
).exists()

with engine.connect() as conn:
    result = conn.execute(select(user_table.c.name).where(~subq)) # ~ is binary negation operator
    print(result.all())

# simple count function that returns number of rows returned
print(select(func.count()).select_from(user_table))

# simple lower function that converts string to lowercase
print(select(func.lower("A String With Much UPPERCASE")))

# simple now function that returns current time, sqlalchemy knows how to handle different dbs
stmt = select(func.now())
with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.all())

# custom function using func namespace will still be rendered as SQL function
print(select(func.some_crazy_function(user_table.c.name, 17)))

# common sql function such as count, now, max, concat include different SQL statements for different backends
# postgres and oracle backends have different sql statements for now function which are included in func namespace
from sqlalchemy.dialects import postgresql
print(select(func.now()).compile(dialect=postgresql.dialect()))

from sqlalchemy.dialects import oracle
print(select(func.now()).compile(dialect=oracle.dialect()))

# pre-configured SQL function (only a few dozen of these)
print(func.now().type)

# arbitrary SQL function (all other SQL functions)
print(func.run_some_calculation().type)

# to add return type to sql function we specify type_
from sqlalchemy import JSON
function_expr = func.json_object('{a, 1, b, "def", c, 3.5}', type_=JSON)

stmt = select(function_expr["def"])
print(stmt)

# built in functions have already specified return type that sometimes depends on how we use them as seen below
from sqlalchemy import Column, Integer, String
m1 = func.max(Column("some_int", Integer))
print(m1.type)

m2 = func.max(Column("some_str", String))
print(m2.type)

print(func.now().type)
print(func.current_date().type)

print(func.concat("x", "y").type)

# built in function that doesnt have specified return type
print(func.upper("lowercase").type)

# some python's operators like + will be based on content around it
# be correctly interpreted by sqlalchemy as concatenation
print(select(func.upper("lowercase") + " suffix"))

# advanced sql function techniques - partition by
stmt = (
    select(
        # count rows, partition (group) by user name, and sort them by email id
        func.row_number().over(partition_by=user_table.c.name),
        user_table.c.name,
        address_table.c.email_address,
    )
    .select_from(user_table)
    .join(address_table)
)
with engine.connect() as conn:  
    # result is list of rows not single row like it would be with max or sum
    # results are grouped by user's name  meaning first all entries for Patrick will be shown then for other users
    result = conn.execute(stmt)
    print(result.all())

# using order_by instead of partition by
stmt = (
    select(
        func.count().over(order_by=user_table.c.name),
        user_table.c.name,
        address_table.c.email_address,
    )
    .select_from(user_table)
    .join(address_table)
)
with engine.connect() as conn:
    # instead of returning 1,2,3... for patrick it sees patrick name first, sets counter
    # and tracks number of instances for name patrick until tie is broken when sandy comes
    # thats why we get 21 returned next to each entry related to patrick name 
    result = conn.execute(stmt)
    print(result.all())

# simple within clause
print(
    func.unnest(
        func.percentile_disc([0.25, 0.5, 0.75, 1]).within_group(user_table.c.name)
    )
)

# simple filter within function
stmt = (
    select(
        func.count(address_table.c.email_address).filter(user_table.c.name == "Sandy"),
        func.count(address_table.c.email_address).filter(
            user_table.c.name == "Spongebob"
        ),
    )
    .select_from(user_table)
    .join(address_table)
)
with engine.connect() as conn:  
    result = conn.execute(stmt)
    print(result.all())

# simple table-valued function
# due to us using postgres we had to adopt this function to it
# changed func.json_each to json_array_elements_text instead

# this function unpacks json valid array into three rows with single column value
# we then filter and take rows where values are "two" and "three"
onetwothree = func.json_array_elements_text('["one", "two", "three"]').table_valued("value")
stmt = select(onetwothree).where(onetwothree.c.value.in_(["two", "three"]))
with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.all())

# simple column valued function
from sqlalchemy import select, func
stmt = select(func.json_array_elements('["one", "two"]').column_valued("x"))
print(stmt)
with engine.connect() as conn:
    result = conn.execute(stmt)
    print(results.all())

from sqlalchemy.dialects import oracle
stmt = select(func.scalar_strings(5).column_valued("s"))
print(stmt.compile(dialect=oracle.dialect()))
