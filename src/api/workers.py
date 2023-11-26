"""
-- Note to self (and others) --
Channel List:
0 From Backend to CreateOrder
1 From CreateOrder to Backend

2 From Backend to Payment
3 From Payment to Backend

4 From Backend to Inventory
5 From Inventory to Backend

6 From Backend to Delivery
7 From Delivery to Backend
"""

import os
from celery import Celery
from fastapi import APIRouter, Depends
from dotenv import load_dotenv
from sqlmodel import Session

from src.models.order_model import create_order, update_order_status
from src.models.db import get_session

router = APIRouter()

load_dotenv()
REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

def get_celery_app(channel_number: int):
    redis_url = f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/{channel_number}"
    return Celery(  "backend",
                    broker=redis_url,
                    backend=redis_url,
                    broker_connection_retry_on_startup=True)
    


# will name the route later
@router.get("/0")
def send_to_create_order(session: Session = Depends(get_session)):
    # create order in db
    order = create_order(
        user_id=1,
        item_id=1,
        quantity=1,
        total_price=1.0,
        session=session
    )
    
    payload = {
        "main_id": order.id,
        "user_id": order.user_id,
        "item_id": order.item_id,
        "quantity": order.quantity,
        "total_price": order.total_price,
    }

    # send message to create order service
    celery = get_celery_app(0)
    # TODO: change task name to match the task name in create_order service
    celery.send_task("wk-create-order.tasks.create_order", kwargs=payload, task_id=str(order.id))
    return "sent task"

@router.get("/2")
def send_to_payment(session: Session = Depends(get_session)):
    # create order in db
    order = update_order_status(main_id=1, session=session)
    
    payload = {
        "main_id": order.id,
        "user_id": order.user_id,
        "item_id": order.item_id,
        "quantity": order.quantity,
        "total_price": order.total_price,
    }

    # send message to create order service
    celery = get_celery_app(2)
    # TODO: change task name to match the task name in payment service
    celery.send_task("wk-payment.tasks.payment", args=(payload,), task_id=str(order.id))

