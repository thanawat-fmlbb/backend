from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, VARCHAR, Relationship, select, Session

from src.models.db import get_engine
class User(SQLModel, table=True):
    # user_id
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True))
    address: str

    # Relationship
    orders: List["Order"] = Relationship(back_populates="user")

def get_user_by_id(id: int):
    with Session(get_engine()) as session:
        statement = select(User).where(User.id == id)
        return session.exec(statement).one()


def create_user(username: str, address: str) -> int:
    with Session(get_engine()) as session:
        user = User(username=username, address=address)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user.id

def user_setup():
    with Session(get_engine()) as session:
        try:
            user1 = session.get(User, 1)
            if user1 is None:
                user1 = User(id=1, username="urmom", address="address_1")
                session.add(user1)
                session.commit()

            user2 = session.get(User, 2)
            if user2 is None:
                user2 = User(id=2, username="mr.broke", address="address_2")
                session.add(user2)
                session.commit()

            user3 = session.get(User, 3)
            if user3 is None:
                user3 = User(id=3, username="johndoe", address="timeout")
                session.add(user3)
                session.commit()
            return True
        except Exception as e:
            print(str(e))
            return False