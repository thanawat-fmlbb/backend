from fastapi import APIRouter, Request

from src.models.db import create_db_and_tables
from src.models.thing_model import thing_setup
from src.models.user_model import user_setup
from src.utils.celery import get_celery_app, ChannelEnum

router = APIRouter()

@router.post("/")
async def control_panel(request: Request):
    return { "WIP": "WIP"}


@router.get("/setup")
async def service_setup():
    create_db_and_tables()
    user_setup()
    thing_setup()

    # send message to create order service
    celery = get_celery_app(ChannelEnum.PAYMENT.value)
    celery.send_task(
        "wk-payment.tasks.setup",
        task_id="setup_payment",
    )

    celery = get_celery_app(ChannelEnum.INVENTORY.value)
    celery.send_task(
        "wk-inventory.tasks.setup",
        task_id="setup_inventory",
    )

    return { "msg": "setup sent" }
