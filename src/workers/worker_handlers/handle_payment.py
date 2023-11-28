from src.utils.celery import get_celery_app, ChannelEnum, TaskNameEnum
from src.models.order_model import StatusEnum, update_order_status


def handle_payment(main_id: int, success: bool, item_id: int, quantity: int):

    if success:
        # update order status
        order = update_order_status(main_id=main_id, status=StatusEnum.PAYMENT)

        payload = {
            "main_id": main_id,
            "item_id": item_id,
            "quantity": quantity,
        }

        # send message to inventory service
        service = get_celery_app(ChannelEnum.INVENTORY.value)
        service.send_task(
            TaskNameEnum.INVENTORY.value,
            kwargs=payload,
            task_id=str(order.id),
        )

    else:
        # rollback to create_order
        service = get_celery_app(ChannelEnum.CREATE_ORDER.value)
        service.send_task(
            TaskNameEnum.RB_CREATE_ORDER.value,
            kwargs={ "main_id": main_id },
            task_id=str(main_id)
        )
