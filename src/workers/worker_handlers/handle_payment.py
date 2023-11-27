from src.utils.celery import get_celery_app
from src.models.order_model import StatusEnum, update_order_status

celery = get_celery_app(2) # get result from channel 2

@celery.task
def handle_payment(result):
    # should send back: 
    # - main_id: int
    # - success: bool
    print("result: ", result)
