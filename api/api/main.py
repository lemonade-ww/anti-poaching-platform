from fastapi import FastAPI

from api.analytics import judgment, species
from api.db.engine import bind_session
from api.db.session import SessionLocal
from api.lib.errors import ResponseError, response_error_handler

app = FastAPI()
app.include_router(species.router)
app.include_router(judgment.router)
bind_session(SessionLocal)

app.add_exception_handler(ResponseError, response_error_handler)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
