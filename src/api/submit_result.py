from fastapi import APIRouter, Request

from src.workers.worker_handlers.handle_create_order import handle_create_order
from src.workers.worker_handlers.handle_payment import handle_payment
from src.workers.worker_handlers.handle_inventory import handle_inventory
from src.workers.worker_handlers.handle_delivery import handle_delivery

router = APIRouter()

@router.post("/submit_result")
async def get_result(request: Request):
    request_body = await request.json()
    main_id = request_body.get("main_id")
    success = request_body.get("success")
    service_name = request_body.get("service_name")
    
    payload = request_body.get("payload")
    
    if service_name == "create_order":
        item_id = payload.get("item_id")
        quantity = payload.get("quantity")
        handle_create_order(main_id=main_id, success=success, item_id=item_id, quantity=quantity)
    elif service_name == "payment":
        item_id = payload.get("item_id")
        quantity = payload.get("quantity")
        handle_payment(main_id=main_id, success=success, item_id=item_id, quantity=quantity)
    elif service_name == "inventory":
        handle_inventory(main_id=main_id, success=success)
    elif service_name == "delivery":
        handle_delivery(main_id=main_id, success=success)
    else:
        raise ValueError("Invalid service_name!!!!")
    
    return {"msg": "result submitted"}