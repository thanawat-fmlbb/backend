from typing import Optional, List

from sqlmodel import SQLModel, Field, Column, VARCHAR, Relationship

class User(SQLModel, table=True):
    # user_id
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True))
    address: str

    # Relationship
    orders: List["Order"] = Relationship(back_populates="user")

def create_user():
    pass