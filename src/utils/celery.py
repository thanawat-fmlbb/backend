"""
-- Note to self (and others) --
Channel List:
0 From Backend to CreateOrder
1 From CreateOrder to Backend

2 From Backend to Payment
3 From Payment to Backend

4 From Backend to Inventory
5 From Inventory to Backend

6 From Backend to Delivery
7 From Delivery to Backend
"""

import os
from utils.celery import Celery
from dotenv import load_dotenv


load_dotenv()
REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

def get_celery_app(channel_number: int):
    redis_url = f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/{channel_number}"
    return Celery(  "backend",
                    broker=redis_url,
                    backend=redis_url,
                    broker_connection_retry_on_startup=True)