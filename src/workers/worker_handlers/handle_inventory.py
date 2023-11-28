from src.utils.celery import get_celery_app, ChannelEnum, TaskNameEnum
from src.models.order_model import StatusEnum, update_order_status


def handle_inventory(main_id: int, success: bool):
    if success:
        # update order status
        order = update_order_status(main_id=main_id, status=StatusEnum.INVENTORY)

        payload = {
            "main_id": main_id,
            "user_id": order.user_id,
            "user_address": order.user.address,
        }

        # send message to delivery service
        service = get_celery_app(ChannelEnum.DELIVERY.value)
        service.send_task(
            TaskNameEnum.DELIVERY.value,
            kwargs=payload,
            task_id=str(order.id),
        )

    else:
        # rollback to payment
        service = get_celery_app(ChannelEnum.PAYMENT.value)
        service.send_task(
            TaskNameEnum.RB_PAYMENT.value,
            kwargs={ "main_id": main_id },
            task_id=str(main_id)
        )
