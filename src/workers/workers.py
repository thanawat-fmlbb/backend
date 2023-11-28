from celery import signature
from src.utils.celery import get_celery_app
from src.models.order_model import create_order
from src.models.user_model import create_user

from src.utils.celery import ChannelEnum, TaskNameEnum

# entry point into the whole process
def send_to_create_order(user_id: int, item_id: int, quantity: int):
    print("hello from send_to_create_order")
    # might create user here, if not already created
    create_user() # not implemented

    # create order in db
    order = create_order(user_id=user_id)
    
    payload = {
        "main_id": order.id,
        "user_id": user_id,
        "item_id": item_id,
        "quantity": quantity,
    }

    # send message to create order service
    # celery = get_celery_app(ChannelEnum.CREATE_ORDER.value)
    celery = get_celery_app(ChannelEnum.INVENTORY.value)
    print(TaskNameEnum.TEST.value)
    celery.send_task(
        # TaskNameEnum.CREATE_ORDER.value,
        TaskNameEnum.TEST.value,
        kwargs=payload,
        task_id=str(order.id),
    )
    return "sent task"
