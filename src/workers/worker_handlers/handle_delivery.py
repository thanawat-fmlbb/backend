from src.utils.celery import get_celery_app, ChannelEnum, TaskNameEnum
from src.models.order_model import StatusEnum, update_order_status


def handle_delivery(main_id: int, success: bool):
    if success:
        # update order status
        update_order_status(main_id=main_id, status=StatusEnum.COMPLETE)

    else:
        # rollback to inventory
        service = get_celery_app(ChannelEnum.INVENTORY.value)
        service.send_task(
            TaskNameEnum.RB_INVENTORY.value,
            kwargs={ "main_id": main_id },
            task_id=str(main_id)
        )
