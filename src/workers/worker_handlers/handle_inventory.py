from src.utils.celery import get_celery_app, ChannelEnum, TaskNameEnum
from src.models.order_model import StatusEnum, update_order_status
from src.models.user_model import get_user_by_id

def handle_inventory(main_id: int, success: bool, result_payload: dict):
    if success:
        # update order status
        order = update_order_status(main_id=main_id, status=StatusEnum.INVENTORY)
        user = get_user_by_id(order.user_id)
        
        payload = {
            "main_id": main_id,
            "user_id": order.user_id,
            "user_address": user.address,
        }

        # send message to delivery service
        service = get_celery_app(ChannelEnum.DELIVERY.value)
        service.send_task(
            TaskNameEnum.DELIVERY.value,
            kwargs=payload,
            task_id=str(order.id),
        )

    else:
        e = result_payload.get("error", "skip")
        if e == "timeout":
            update_order_status(main_id=main_id, status=StatusEnum.TIMEOUT)
        elif e == "out_of_stock":
            update_order_status(main_id=main_id, status=StatusEnum.OUT_OF_STOCK)
        elif e != "skip":
            update_order_status(main_id=main_id, status=StatusEnum.UNKNOWN)

        # rollback to payment
        service = get_celery_app(ChannelEnum.PAYMENT.value)
        service.send_task(
            TaskNameEnum.RB_PAYMENT.value,
            kwargs={ "main_id": main_id },
            task_id=str(main_id)
        )
