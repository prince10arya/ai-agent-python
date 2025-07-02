import os

from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.db import init_db
from api.chat.routing import router as chat_router
#? check this fuction if any error
@asynccontextmanager
async def lifespan(app: FastAPI):
    #* before start up
     #* Run synchronous init_db in a separate thread to avoid blocking the event loop
    print("Application startup: Initializing database...")
    init_db()
    print("Application startup: Database initialized.")
    yield
    #* after shutdown
    print("Application shutdown: Cleaning up resources (if any)...")

app = FastAPI(lifespan=lifespan)
app.include_router(chat_router, prefix='/api/chats')
@app.get('/')
def read_index():
    return {"hello": "world"}
