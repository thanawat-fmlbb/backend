from fastapi import Request

from src.utils.celery import get_celery_app
from src.models.order_model import StatusEnum, create_order, update_order_status
from src.models.thing_model import get_price
from src.models.user_model import create_user


# entry point into the whole process
async def send_to_create_order(request: Request):
    request_body = await request.json()

    # might create user here, if not already created
    create_user() # not implemented

    user_id = request_body.get("user_id")
    item_id = request_body.get("item_id")
    quantity = request_body.get("quantity")

    # create order in db
    order = create_order(user_id=user_id)
    
    payload = {
        "main_id": order.id,
        "user_id": user_id,
        "item_id": item_id,
        "quantity": quantity,
    }

    # send message to create order service
    celery = get_celery_app(0)
    # TODO: change task name to match
    celery.send_task(
        "wk-create-order.tasks.create_order",       # task name
        kwargs=payload,
        task_id=str(order.id),
        link="backend.tasks.handle_create_order"    # callback task
    )
    return "sent task"


async def send_to_payment(main_id: int, item_id: int, quantity: int):
    # update order status
    order = update_order_status(main_id=main_id, status= StatusEnum.CREATE_ORDER)
    
    payload = {
        "main_id": main_id,
        "user_id": order.user_id,
        "item_price": get_price(item_id=item_id),
        "quantity": quantity,
    }

    # send message to create order service
    celery = get_celery_app(2)
    # TODO: change task name to match
    celery.send_task("wk-payment.tasks.payment", args=(payload,), task_id=str(order.id))

