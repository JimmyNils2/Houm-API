from fastapi import FastAPI
from routes import employees, properties, visits
from sqlalchemy.ext.asyncio import AsyncEngine

from db.db_setup import async_engine
from db.models import employee, property, visit


app = FastAPI(
    title="HOUM API",
    description="Real Estate API",
    version="0.0.1",
    contact={
        "name": "Jimmy Gonzalez",
        "url": "https://github.com/JimmyNils2",
        "email": "jimmynils2@gmail.com",
    },
    license_info={"name": "MIT"},
)

async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(employee.Base.metadata.create_all)
        await conn.run_sync(property.Base.metadata.create_all)
        await conn.run_sync(visit.Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await create_tables(async_engine)

app.include_router(employees.router)
app.include_router(properties.router)
app.include_router(visits.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
