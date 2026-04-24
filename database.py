"""
AutoFlow AI - Database Connection
Configuración de SQLAlchemy + asyncpg para PostgreSQL
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine                          # ← nuevo
from sqlalchemy.orm import declarative_base, sessionmaker     # ← nuevo
from config import settings

# Engine asincrónico (para Uvicorn/FastAPI)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Session factory asíncrona
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base para modelos
Base = declarative_base()


# ─── Engine síncrono (exclusivo para threads del JobExecutor) ──────────────────
SYNC_DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql+asyncpg://", "postgresql+psycopg2://"
)

sync_engine = create_engine(
    SYNC_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)
# ──────────────────────────────────────────────────────────────────────────────


async def get_db():
    """Dependency para inyectar sesión de BD en endpoints"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Inicializar tablas en la BD"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Cerrar conexión con la BD"""
    await engine.dispose()