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


def create_user():
    pass