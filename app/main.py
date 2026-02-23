from app.api.routes import router
from fastapi import FastAPI

from app.db.database import database, engine
from app.models.message import Base

app = FastAPI(title="AI Project API")

app.include_router(router)


@app.on_event("startup")
async def startup():
    await database.connect()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("🚀 Database is connected!")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()