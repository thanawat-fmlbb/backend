from fastapi import FastAPI, Request

from src.workers import workers
from src.models import db
from src.models.user_model import create_user
from src.api import submit_result, control_panel

app = FastAPI()
app.include_router(submit_result.router, prefix="/internal")
app.include_router(control_panel.router, prefix="/backdoor")


# init database
db.create_db_and_tables()


@app.get("/")
def test():
    print("hello")
    return {"hello": "world"}


@app.post("/order")
async def receive_order(request: Request):
    # gets http request body
    request_body = await request.json()
    user_id = request_body.get("user_id")
    username = request_body.get("username")
    address = request_body.get("address")
    item_id = request_body.get("item_id")
    quantity = request_body.get("quantity")

    response = {}
    if not user_id:
        # might create user here, if not already created
        user_id = create_user(username, address) # not implemented
        response["user_created"] = f"User created with id: {user_id}"

    # send task to create order
    workers.send_to_create_order(user_id=user_id, item_id=item_id, quantity=quantity)
    response["msg"] = "task sent"
    return response
