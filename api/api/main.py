import asyncio
from typing import Optional

from fastapi import FastAPI

from api.db.engine import init_engine
from api.db.models import Base

app = FastAPI()
engine = init_engine()


@app.get("/init")
def init_db():
    return Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id + 12, "q": q}
