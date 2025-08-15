from fastapi import FastAPI
from database import engine, Base
from tasks import router as tasks_router

app = FastAPI(title="Task Manager API")

app.include_router(tasks_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)