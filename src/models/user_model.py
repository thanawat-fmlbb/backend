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
            user = session.get(User, 1)
            if user is None:
                user = User(id=1, username="urmom", address="address_1")
                session.add(user)
                session.commit()

            user = session.get(User, 2)
            if user is None:
                user = User(id=2, username="urmom", address="address_2")
                session.add(user)
                session.commit()

            user = session.get(User, 3)
            if user is None:
                user = User(id=3, username="urmom", address="timeout")
                session.add(user)
                session.commit()
            return True
        except Exception as e:
            print(str(e))
            return False