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
from fastapi import APIRouter, Depends, Request
from dotenv import load_dotenv
from sqlmodel import Session

from src.models.db import get_session
from src.models.order_model import StatusEnum, create_order, update_order_status
from src.models.thing_model import get_price
from src.models.user_model import create_user

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
@router.post("/0")
async def send_to_create_order(request: Request, session: Session = Depends(get_session)):
    request_body = await request.json()

    # might create user here, if not already created
    create_user() # not implemented

    user_id = request_body.get("user_id")
    item_id = request_body.get("item_id")
    quantity = request_body.get("quantity")

    # create order in db
    order = create_order(
        user_id=user_id,
        session=session
    )
    
    payload = {
        "main_id": order.id,
        "user_id": user_id,
        "item_id": item_id,
        "quantity": quantity,
    }

    # send message to create order service
    celery = get_celery_app(0)
    # TODO: change task name to match
    celery.send_task("wk-create-order.tasks.create_order", kwargs=payload, task_id=str(order.id))
    return "sent task"

@router.get("/2")
async def send_to_payment(request: Request, session: Session = Depends(get_session)):
    request_body = await request.json()

    main_id = request_body.get("main_id")
    item_id = request_body.get("item_id")
    quantity = request_body.get("quantity")

    # update order status
    order = update_order_status(main_id=main_id, status= StatusEnum.CREATE_ORDER, session=session)
    
    payload = {
        "main_id": main_id,
        "user_id": order.user_id,
        "item_price": get_price(item_id=item_id, session=session),
        "quantity": quantity,
    }

    # send message to create order service
    celery = get_celery_app(2)
    # TODO: change task name to match
    celery.send_task("wk-payment.tasks.payment", args=(payload,), task_id=str(order.id))

