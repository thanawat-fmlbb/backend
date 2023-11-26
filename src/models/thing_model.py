from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

class Thing(SQLModel, table=True):
    # item_id
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float

    # Relationship
    orders: List["Order"] = Relationship(back_populates="item")