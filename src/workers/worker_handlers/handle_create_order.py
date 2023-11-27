from src.utils.celery import get_celery_app
from src.models.order_model import StatusEnum, update_order_status
from src.models.thing_model import get_price

celery = get_celery_app(0) # get result from channel 0

@celery.task
def handle_create_order(result):
    print("hello from handle_create_order")
    # should send back: 
    # - main_id: int
    # - success: bool
    # - item_id: int    --> can be stored in db instead of sending back
    # - quantity: int   --> can be stored in db instead of sending back

    print("result: ", result)
    main_id = result.get("main_id")
    success = result.get("success", False)
    item_id = result.get("item_id")
    quantity = result.get("quantity")

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
        service = get_celery_app(0)
        # TODO: change task name to match + add kwargs
        service.send_task("wk-payment.tasks.make_payment", kwargs=payload, task_id=str(main_id))

    else:
        # rollback
        service = get_celery_app(0)
        service.send_task("wk-create-order.tasks.rollback", kwargs={ "main_id": main_id }, task_id=str(main_id))
