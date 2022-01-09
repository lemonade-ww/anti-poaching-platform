import asyncio
from typing import Optional

from fastapi import FastAPI

from api.analytics.taxon import router
from api.db.engine import init_engine
from api.db.session import SessionLocal

app = FastAPI()
app.include_router(router)
engine = init_engine()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id + 12, "q": q}
