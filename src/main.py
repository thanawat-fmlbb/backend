from fastapi import FastAPI, Request
from src.workers import workers
from src.models import db
from src.api import submit_result

app = FastAPI()
app.include_router(submit_result.router, prefix="/internal")


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
    item_id = request_body.get("item_id")
    quantity = request_body.get("quantity")

    # send task to create order
    workers.send_to_create_order(user_id=user_id, item_id=item_id, quantity=quantity)
    return {"msg": "task sent"}
