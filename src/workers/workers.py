from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from src.utils.celery import get_celery_app
from src.models.order_model import create_order

from src.utils.celery import ChannelEnum, TaskNameEnum
from opentelemetry import trace


# entry point into the whole process
def send_to_create_order(user_id: int, item_id: int, quantity: int):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("send_to_create_order"):
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        header = {"traceparent": carrier["traceparent"]}

        # create order in db
        order = create_order(user_id=user_id)

        payload = {
            "main_id": order.id,
            "user_id": user_id,
            "item_id": item_id,
            "quantity": quantity,
        }

        # send message to create order service
        celery = get_celery_app(ChannelEnum.CREATE_ORDER.value)
        celery.send_task(
            TaskNameEnum.CREATE_ORDER.value,
            kwargs=payload,
            task_id=str(order.id),
            headers=header,
        )
    return "sent task"
