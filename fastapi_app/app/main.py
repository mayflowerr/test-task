from fastapi import FastAPI
from .db import SessionLocal, Base, engine
import os
from contextlib import asynccontextmanager
from app.routers import questions


SKIP_DB_INIT = os.getenv("SKIP_DB_INIT", "0") == "1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not SKIP_DB_INIT:
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Q&A API (FastAPI)", lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(questions.router)