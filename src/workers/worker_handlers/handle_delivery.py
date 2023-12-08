from src.utils.celery import get_celery_app, ChannelEnum, TaskNameEnum
from src.models.order_model import StatusEnum, update_order_status


def handle_delivery(main_id: int, success: bool, result_payload: dict, header: dict):
    if success:
        # update order status
        update_order_status(main_id=main_id, status=StatusEnum.DELIVERY)
        
        service = get_celery_app(ChannelEnum.PAYMENT.value)
        service.send_task(
            TaskNameEnum.PAYMENT_SUCCESS.value,
            kwargs={ "main_id": main_id },
            task_id=str(main_id),
            headers=header
        )
    else:
        # check error type
        e = result_payload.get("error", "skip")
        if e == "timeout":
            update_order_status(main_id=main_id, status=StatusEnum.TIMEOUT)
        elif e != "skip":
            update_order_status(main_id=main_id, status=StatusEnum.UNKNOWN)
        
        # rollback to inventory
        service = get_celery_app(ChannelEnum.INVENTORY.value)
        service.send_task(
            TaskNameEnum.RB_INVENTORY.value,
            kwargs={ "main_id": main_id },
            task_id=str(main_id),
            headers=header
        )
