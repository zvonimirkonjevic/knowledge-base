from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from models import engine


class Base(DeclarativeBase):
    pass

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
    
    user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

Base.metadata.create_all(engine)

u1 = User(name="pkrabs", fullname="Pearl Krabs")
print(u1.addresses)

a1 = Address(email_address="pearl.krabs@gmail.com")
u1.addresses.append(a1)
print(u1.addresses)

# also user field in adresses table has synchronized
print(a1.user) # synchronization is result of using back_populates parameter

a2 = Address(email_address="pearl@aol.com", user=u1)
print(u1.addresses)

a2.user = u1

session = Session(engine)

session.add(u1)

print(u1 in session)
print(a1 in session)
print(a2 in session)

print(u1.id)
print(a1.user_id)

session.commit()

print(u1.id)
print(u1.addresses)
print(u1.addresses) # now we wont see sql as we have lazy loaded this attribute already

# since we have lazy loaded user object already that contains a1, a2 addresses as they are same objects as a1 and a2
# we wont see fetch from db using sql 
print(a1)
print(a2)

# using relationship() to indicate right side of join and on clause at once in ORM
from sqlalchemy import select
print(select(Address.email_address).select_from(User).join(User.addresses))

# following works because of foreign key constraint not because of relationship() objects on User and Address classes
print(select(Address.email_address).join_from(User, Address))

from sqlalchemy.orm import selectinload
for user_obj in session.execute(
    select(User).options(selectinload(User.addresses))
).scalars():
    user_obj.addresses  # access addresses collection already loaded

# or we can add it as parameter in relationship
#class User(Base):
#    __tablename__ = "user_account"
#
#    addresses: Mapped[List["Address"]] = relationship(
#        back_populates="user", lazy="selectin"
#    )

# selectin load
from sqlalchemy.orm import selectinload
stmt = select(User).options(selectinload(User.addresses)).order_by(User.id)
for row in session.execute(stmt):
    print(
        f"{row.User.name}  ({', '.join(a.email_address for a in row.User.addresses)})"
    )

# joined load
from sqlalchemy.orm import joinedload
stmt = (
    select(Address)
    .options(joinedload(Address.user, innerjoin=True))
    .order_by(Address.id)
)
for row in session.execute(stmt):
    print(f"{row.Address.email_address} {row.Address.user.name}")

# explicit join + eager load
# similar to joined load except we have to define join ourself
from sqlalchemy.orm import contains_eager
stmt = (
    select(Address)
    .join(Address.user)
    .where(User.name == "pkrabs")
    .options(contains_eager(Address.user))
    .order_by(Address.id)
)
for row in session.execute(stmt):
    print(f"{row.Address.email_address} {row.Address.user.name}")

stmt = (
    select(Address)
    .join(Address.user)
    .where(User.name == "pkrabs")
    .options(joinedload(Address.user))
    .order_by(Address.id)
)
print(stmt)  # select has a join and left outer join unnecessarily

# raise load
# one way to set it up is to configure it on relationship itself
#class User(Base):
#    __tablename__ = "user_account"
#    id: Mapped[int] = mapped_column(primary_key=True)
#    addresses: Mapped[List["Address"]] = relationship(
#        back_populates="user", lazy="raise_on_sql"
#    )
#class Address(Base):
#    __tablename__ = "address"
#    id: Mapped[int] = mapped_column(primary_key=True)
#    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
#    user: Mapped["User"] = relationship(back_populates="addresses", lazy="raise_on_sql")
