from fastapi import FastAPI

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("Запуск...")

app = FastAPI(
    lifespan=lifespan
)


