from src.utils.celery import get_celery_app, ChannelEnum, TaskNameEnum
from src.models.order_model import StatusEnum, update_order_status


def handle_payment(main_id: int, success: bool, result_payload: dict, header: dict):
    if success:
        item_id = result_payload.get("item_id")
        quantity = result_payload.get("quantity")
        
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
            headers=header
        )

    else:
        e = result_payload.get("error", "skip")
        if e == "timeout":
            update_order_status(main_id=main_id, status=StatusEnum.TIMEOUT)
        elif e == "insufficient_funds":
            update_order_status(main_id=main_id, status=StatusEnum.INSUFFICIENT_FUNDS)
        elif e != "skip":
            update_order_status(main_id=main_id, status=StatusEnum.UNKNOWN)

        # rollback to create_order
        service = get_celery_app(ChannelEnum.CREATE_ORDER.value)
        service.send_task(
            TaskNameEnum.RB_CREATE_ORDER.value,
            kwargs={ "main_id": main_id }, # removes error field so it skips the error check next time
            task_id=str(main_id),
            headers=header
        )

        
def handle_payment_confirm(main_id: int, success: bool, result_payload: dict, header: dict):
    if success:
        # update order status
        update_order_status(main_id=main_id, status=StatusEnum.SUCCESS)
        # done
    else:
        e = result_payload.get("error", "skip")
        if e == "timeout":
            update_order_status(main_id=main_id, status=StatusEnum.TIMEOUT)
        elif e == "insufficient_funds":
            update_order_status(main_id=main_id, status=StatusEnum.INSUFFICIENT_FUNDS)
        elif e != "skip":
            update_order_status(main_id=main_id, status=StatusEnum.UNKNOWN)

        # rollback to delivery
        service = get_celery_app(ChannelEnum.DELIVERY.value)
        service.send_task(
            TaskNameEnum.RB_DELIVERY.value,
            kwargs={ "main_id": main_id },
            task_id=str(main_id),
            headers=header
        )