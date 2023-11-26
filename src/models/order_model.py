from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship, Session, select
from fastapi import Depends

from src.models.db import engine, get_session
from src.models.user_model import User
from src.models.thing_model import Thing

class StatusEnum(str, Enum):
    IN_PROGRESS = "in_progress"
    CREATE_ORDER = "create_order"
    PAYMENT = "payment"
    INVENTORY = "inventory"
    DELIVERY = "delivery"
    FAILED = "failed"
    COMPLETE = "complete"

class Order(SQLModel, table=True):
    # main_id
    id: Optional[int] = Field(default=None, primary_key=True)
    status: StatusEnum = Field(default=StatusEnum.IN_PROGRESS)
    user_id: int = Field(foreign_key="user.id")

    item_id: int = Field(foreign_key="thing.id")
    quantity: int

    total_price: float # might be removed

    # Relationship
    user: Optional[User] = Relationship(back_populates="orders")
    item: Optional[Thing] = Relationship(back_populates="orders")



def create_order(
    user_id: int,
    item_id: int,
    quantity: int,
    total_price: float,
    session: Session,
    ):
    order = Order(user_id=user_id, item_id=item_id, quantity=quantity, total_price=total_price)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def update_order_status(
    main_id: int,
    session: Session,
    ):
    statement = select(Order).where(Order.id == main_id)
    order = session.exec(statement).one()
    order.status = StatusEnum.CREATE_ORDER
    session.add(order)
    session.commit()
    session.refresh(order)
    return order
