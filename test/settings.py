from pydantic import BaseModel
import os
from enum import Enum

class DatabaseType(Enum):
    sqlite: str = "sqlite"
    postgres: str = "postgres"
    async_postgres: str = "async_postgres"

class Settings(BaseModel):
    database_type: DatabaseType
    postgres_username: str
    postgres_password: str
    postgres_database: str
    postgres_port: int
    postgres_host: str

CRUDCREATOR_TEST_ENV = os.getenv("CRUDCREATOR_TEST_ENV")

with open(os.path.join("test", "settings", CRUDCREATOR_TEST_ENV+".json"), "r") as f:
    settings = Settings.parse_raw(f.read())