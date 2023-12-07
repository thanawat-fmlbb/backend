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

def thing_setup():
    with Session(get_engine()) as session:
        try:
            
            item1 = session.get(Thing, 1)
            if item1 is None:
                item1 = Thing(id=1, name="thing", price=10)
                session.add(item1)
                session.commit()

            item2 = session.get(Thing, 2)
            if item2 is None:
                item2 = Thing(id=2, name="empty_thing", price=20)
                session.add(item2)
                session.commit()

            item3 = session.get(Thing, 3)
            if item3 is None:
                item3 = Thing(id=3, name="another_thing", price=10)
                session.add(item3)
                session.commit()
            return True
        except Exception as e:
            print(str(e))
            return False