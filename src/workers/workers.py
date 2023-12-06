from src.utils.celery import get_celery_app
from src.models.order_model import create_order

from src.utils.celery import ChannelEnum, TaskNameEnum

# entry point into the whole process
def send_to_create_order(user_id: int, item_id: int, quantity: int):
    # create order in db
    order = create_order(user_id=user_id)
    
    payload = {
        "main_id": order.id,
        "user_id": user_id,
        "item_id": item_id,
        "quantity": quantity,
    }

    # send message to create order service
    celery = get_celery_app(ChannelEnum.CREATE_ORDER.value)
    celery.send_task(
        TaskNameEnum.CREATE_ORDER.value,
        kwargs=payload,
        task_id=str(order.id),
    )
    return "sent task"
