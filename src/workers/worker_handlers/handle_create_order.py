from src.utils.celery import get_celery_app, ChannelEnum, TaskNameEnum
from src.models.order_model import StatusEnum, update_order_status
from src.models.thing_model import get_price


def handle_create_order(main_id: int, success: bool, item_id: int, quantity: int):
    
    if success:
        # update order status
        order = update_order_status(main_id=main_id, status=StatusEnum.CREATE_ORDER)

        payload = {
            "main_id": main_id,
            "user_id": order.user_id,
            "item_price": get_price(item_id=item_id),
            "quantity": quantity,
        }

        # send message to payment service
        service = get_celery_app(ChannelEnum.PAYMENT.value)
        service.send_task(
            TaskNameEnum.PAYMENT.value,
            kwargs=payload,
            task_id=str(order.id),
        )

    else:
        # should not rollback to create order again
        # create_order should deal with status when create entity in db
        update_order_status(main_id=main_id, status=StatusEnum.FAILED)
