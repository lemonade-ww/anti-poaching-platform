from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import analytics
from api.config import Environment, get_settings
from api.db.engine import bind_session
from api.db.session import SessionLocal

app = FastAPI(servers=[{"url": "http://localhost:8000"}])
app.include_router(analytics.router)
bind_session(SessionLocal)

if get_settings().environment is Environment.Development:
    # Allow all origins for development only
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_headers=["*"],
        allow_methods=["*"],
        allow_credentials=True,
    )


@app.get("/")
async def read_root():
    return {"Hello": "World"}
