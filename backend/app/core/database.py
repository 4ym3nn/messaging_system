from psycopg_pool import AsyncConnectionPool
from app.core.config import settings

pool: AsyncConnectionPool = None

async def init_db_pool():
    global pool
    pool = AsyncConnectionPool(settings.DATABASE_URL, min_size=5, max_size=20)
    await pool.open()

async def close_db_pool():
    global pool
    if pool:
        await pool.close()

def get_pool() -> AsyncConnectionPool:
    return pool
