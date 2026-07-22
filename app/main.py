import os

import evidentrace_sdk
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

    # Evidentrace: post every finished trace to the local compute engine
    # (dev mode — see EVIDENTRACE_DEV_ENGINE_URL to point elsewhere).
    evidentrace_sdk.init(
        dev_engine_url=os.environ.get(
            "EVIDENTRACE_DEV_ENGINE_URL", "http://localhost:8100"
        ),
        framework="langchain",
    )

    print("🚀 Database is connected!")


@app.on_event("shutdown")
async def shutdown():
    evidentrace_sdk.shutdown()
    await database.disconnect()