from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine
from routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時: テーブルを作成
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="FastAPI Auth", lifespan=lifespan)

app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
