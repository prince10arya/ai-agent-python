import os
import sqlmodel
from sqlmodel import Session, SQLModel
DB_URL = os.environ.get('DATABASE_URL')

if DB_URL == "":
    raise NotImplementedError("`DB_URL` needs to be set")

engine = sqlmodel.create_engine(DB_URL)

# database models
def init_db():
    print("creating database tables...")
    SQLModel.metadata.create_all(engine)

# api routes
def get_session():
    with Session(engine) as session:
        yield session

