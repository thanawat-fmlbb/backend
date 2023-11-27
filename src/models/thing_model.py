from typing import Optional
from sqlmodel import SQLModel, Field, Session, select

from src.models.db import get_engine

class Thing(SQLModel, table=True):
    # item_id
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float

def get_price(item_id: int):
    with Session(get_engine()) as session:
        statement = select(Thing).where(Thing.id == item_id)
        thing = session.exec(statement).one()
        return thing.price
