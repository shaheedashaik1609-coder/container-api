from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db import init_pool, close_pool
from app.routers import containers, predict  

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_pool()
    yield
    close_pool()


app = FastAPI(title="Container API",version="1.0.0",lifespan=lifespan)

app.include_router(containers.router)
app.include_router(predict.router)

@app.get("/health")
def health():
    return {"status": "ok"}