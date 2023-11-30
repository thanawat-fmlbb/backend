from src.utils.celery import get_celery_app, ChannelEnum, TaskNameEnum
from src.models.order_model import StatusEnum, update_order_status


def handle_delivery(main_id: int, success: bool, result_payload: dict):
    if success:
        # update order status
        update_order_status(main_id=main_id, status=StatusEnum.SUCCESS)

    else:
        # check error type
        # error type should not be empty since this is the last service
        e = result_payload.get("error")
        if e == "timeout":
            update_order_status(main_id=main_id, status=StatusEnum.TIMEOUT)
        else:
            update_order_status(main_id=main_id, status=StatusEnum.UNKNOWN)
        
        # rollback to inventory
        service = get_celery_app(ChannelEnum.INVENTORY.value)
        service.send_task(
            TaskNameEnum.RB_INVENTORY.value,
            kwargs={ "main_id": main_id },
            task_id=str(main_id)
        )
