from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.database import create_db_and_tables
from routers.courses import router as courses_router
from routers.students import router as students_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="API Académica", lifespan=lifespan)
app.include_router(courses_router)
app.include_router(students_router)
