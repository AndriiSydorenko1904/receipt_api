from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import users, receipts, public
from app.core.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Receipt API", lifespan=lifespan)

# Роутери
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(receipts.router, prefix="/receipts", tags=["Receipts"])
app.include_router(public.router, prefix="/receipts/public", tags=["Public Receipts"])
