from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship, Session, select

from src.models.user_model import User
from src.models.db import get_engine

class StatusEnum(str, Enum):
    # neutral
    IN_PROGRESS = "in_progress"

    # success
    CREATE_ORDER = "create_order"
    PAYMENT = "payment"
    INVENTORY = "inventory"
    DELIVERY = "delivery"
    SUCCESS = "success"

    # failure
    INSUFFICIENT_FUNDS = "insufficient_funds"
    OUT_OF_STOCK = "out_of_stock"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # main_id
    status: StatusEnum = Field(default=StatusEnum.IN_PROGRESS.value)
    user_id: int = Field(foreign_key="user.id") # in case we needed it

    # Relationship
    user: Optional[User] = Relationship(back_populates="orders")


def create_order(
    user_id: int,
    ):
    with Session(get_engine()) as session:
        order = Order(user_id=user_id)
        session.add(order)
        session.commit()
        session.refresh(order)
        return order

def update_order_status(
    main_id: int,
    status: StatusEnum,
    ):
    with Session(get_engine()) as session:
        statement = select(Order).where(Order.id == main_id)
        order = session.exec(statement).one()
        order.status = status.value
        session.add(order)
        session.commit()
        session.refresh(order)
    return order
