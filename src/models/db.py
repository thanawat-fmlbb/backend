import os
from dotenv import load_dotenv

from sqlmodel import SQLModel, Session, create_engine


load_dotenv()
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_HOSTNAME = os.environ.get('DB_HOSTNAME', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'backend')

db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url)

# import models so that the tables will be created
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# def get_engine():
#     return engine

def get_session():
    with Session(engine) as session:
        yield session