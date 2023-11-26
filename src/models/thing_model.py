from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship, Session, select

class Thing(SQLModel, table=True):
    # item_id
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float

def get_price(item_id: int, session: Session):
    statement = select(Thing).where(Thing.id == item_id)
    thing = session.exec(statement).one()
    return thing.price
