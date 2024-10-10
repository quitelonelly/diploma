from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from database.config import settings

# Создание движка
sync_engine = create_engine(
    url = settings.DATABASE_URL_psycopg,
    echo = True,
    # pool_size = 5,
    # max_overflow = 10
)

async_engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    echo = True,
    # pool_size = 5,
    # max_overflow = 10
)
new_session = async_sessionmaker(async_engine, expire_on_commit=False)

with sync_engine.connect() as conn:
    res = conn.execute(text("SELECT VERSION()"))
    print(f"{res.first()=} ")
