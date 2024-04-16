from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from test.settings import settings, DatabaseType
from sqlalchemy.ext.asyncio import AsyncEngine
from src.crudcreator.adaptator.sql.engine_wrapper.SQLEngineWrapper import SQLEngineSyncWrapper, SQLEngineAsyncWrapper
from sqlalchemy.pool import NullPool

if settings.database_type == DatabaseType.sqlite:
    engine = create_engine("sqlite+pysqlite:///test/data/1.sqlite", echo=False)
    engine_sync = engine
    engine_wrapper = SQLEngineSyncWrapper(engine=engine)
elif settings.database_type == DatabaseType.postgres:
    engine = create_engine(
        f"postgresql+pg8000://{settings.postgres_username}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}", echo=False)
    engine_sync = engine
    engine_wrapper = SQLEngineSyncWrapper(engine=engine)
elif settings.database_type == DatabaseType.async_postgres:
    engine = create_async_engine(
        f"postgresql+asyncpg://{settings.postgres_username}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}", 
        echo=False,
        poolclass=NullPool#TODO : remove (can't at the moment, otherwise the unit test TestClient crashes)
    )
    engine_sync = create_engine(
        f"postgresql+pg8000://{settings.postgres_username}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}",
        echo=False
    )
    engine_wrapper = SQLEngineAsyncWrapper(engine=engine)
else:
    raise not NotImplementedError()
