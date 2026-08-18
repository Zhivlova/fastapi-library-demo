from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Model

from routers.books import router as books_router
from models.books import BooksModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    print("База данных готова к работе")

    yield

    print("Выключение сервера")


app = FastAPI(
    lifespan=lifespan,
    title="Book Manager API",
    description="Учебное приложение для курса по FastAPI",
    version="1.0.0",
)
app.include_router(books_router)
