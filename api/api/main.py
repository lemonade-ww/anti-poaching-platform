from fastapi import FastAPI

from api import analytics
from api.db.engine import bind_session
from api.db.session import SessionLocal

app = FastAPI()
app.include_router(analytics.router)
bind_session(SessionLocal)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
