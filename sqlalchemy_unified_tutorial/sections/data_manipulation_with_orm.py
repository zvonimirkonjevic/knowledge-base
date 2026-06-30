from sqlalchemy.orm import Session

from models import User, Address, engine


# ========================================
# Insert in ORM using Unit of Work pattern
# ========================================

# defining potential row in ORM way
squidward = User(name="Squidward", fullname="Squidward Tentacles")
krabs = User(name="EHKrabs", fullname="Eugene H. Krabs")

# adding potential rows to session -> pending state
session = Session(engine)
session.add(squidward)
session.add(krabs)

print(session.new)

# to create new transaction where we push current set of changes
# we use .flush(), not needed, .commit() already calls that for us
session.flush() # after this executes transaction is still open, so we need to commit changes, roll them back or close it

# objects are now in new state: persistent and are associated with session object in which they are loaded or added
# after being flushed ORM has retrieved primary key for each object
print(squidward.id)
print(krabs.id)


# ========================================
# Update in ORM using Unit of Work pattern
# ========================================

# these new items are stored by primary key in identity map
# if we fetch newly added object it searches identity map 
# else it emmits select statement
some_squidward = session.get(User, 4)
print(some_squidward)

# identity map unique instance of particular python object per a particular database identity
print(some_squidward is squidward)

# commit changes to the database
session.commit()

from sqlalchemy import select
sandy = session.execute(select(User).filter_by(name="Sandy")).scalar_one()
print(sandy)

# session keeps track of changes made to objects
sandy.fullname = "Sandy Squirrel"
print(sandy in session.dirty)

# use select statement to fetch changed full name, as this select will autoflush any changes made
sandy_fullname = session.execute(select(User.fullname).where(User.id == 2)).scalar_one()
print(sandy_fullname) # these changes are still in transaction so they are not persisted on db
print(sandy in session.dirty)


# ========================================
# Delete in ORM using Unit of Work pattern
# ========================================

patrick = session.get(User, 3)

# same as insert and update nothing happens until flush
session.delete(patrick)

session.execute(select(User).where(User.name == "Patrick")).first()
print(patrick in session)


# ========================================
# Bulk/Multi row insert, update, delete in ORM using Unit of Work pattern
# ========================================

# simple multi row insert
from sqlalchemy import insert
session.execute(
    insert(User),
    [
        {"name": "spongebob", "fullname": "Spongebob Squarepants"},
        {"name": "sandy", "fullname": "Sandy Cheeks"},
        {"name": "patrick", "fullname": "Patrick Star"},
        {"name": "squidward", "fullname": "Squidward Tentacles"},
        {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
    ],
)


# ==========================
# Rollback
# ==========================

session.rollback()

# lets inspect sandy object after rollback -> it should be expired
print(sandy.__dict__)

# accessing attributes will lazy load them
print(sandy.fullname)
print(sandy.__dict__)

print(patrick in session)

print(session.execute(select(User).where(User.name == "Patrick")).scalar_one() is patrick)


# ========================
# Closing session
# ========================

session.close()

# lets try to access session related object
# print(squidward.name) # we cannot access this variable as it was expunged

# to access squidward we can re-attach it to same session
session.add(squidward)
print(squidward.name)
