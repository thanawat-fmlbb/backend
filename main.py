from fastapi import FastAPI
from src.api import workers
from src.models import db

app = FastAPI()
# get routers from different files
app.include_router(workers.router, prefix="/workers")

# init database
db.create_db_and_tables()


@app.get("/")
def test():
    print("hello")
    return {"hello": "world"}