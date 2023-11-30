"""
-- Note to self (and others) --
Channel List:
0 - backend to create_order
1 - backend to payment
2 - backend to inventory
3 - backend to delivery
4 - workers to result collector 
"""

import os
from celery import Celery
from dotenv import load_dotenv
from enum import Enum

class ChannelEnum(Enum):
    CREATE_ORDER = 0
    PAYMENT = 1
    INVENTORY = 2
    DELIVERY = 3
    RESULT = 4

class TaskNameEnum(Enum):
    CREATE_ORDER = "wk-create-order.tasks.create_order"
    PAYMENT = "wk-payment.tasks.create_payment"
    INVENTORY = "wk-inventory.tasks.check_inventory"
    DELIVERY = "wk-delivery.tasks.deliver"

    RB_CREATE_ORDER = "wk-create-order.tasks.rollback"
    RB_PAYMENT = "wk-payment.tasks.rollback"
    RB_INVENTORY = "wk-inventory.tasks.rollback"
    RB_DELIVERY = "wk-delivery.tasks.rollback"


load_dotenv()
REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

def get_celery_app(channel_number: int):
    redis_url = f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/{channel_number}"
    return Celery(  "backend",
                    broker=redis_url,
                    backend=redis_url,
                    broker_connection_retry_on_startup=True)