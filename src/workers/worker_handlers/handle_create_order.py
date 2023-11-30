from src.utils.celery import get_celery_app, ChannelEnum, TaskNameEnum
from src.models.order_model import StatusEnum, update_order_status
from src.models.thing_model import get_price


def handle_create_order(main_id: int, success: bool, result_payload: dict):
    if success:
        item_id = result_payload.get("item_id")
        quantity = result_payload.get("quantity")
        
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

        # check error type
        # if error is defined but does not match any of the cases, then UNKNOWN
        # if error is not defined (most likely already dealt with), then SKIP
        e = result_payload.get("error", "skip")
        if e == StatusEnum.TIMEOUT.value:
            update_order_status(main_id=main_id, status=StatusEnum.TIMEOUT)
        elif e != "skip":
            update_order_status(main_id=main_id, status=StatusEnum.UNKNOWN)
        
