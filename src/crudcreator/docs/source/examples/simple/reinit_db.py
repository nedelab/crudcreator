"""
This code is used to create the correct tables in the SQLite database.
Normally, you'll never have to write such code: crudcreator connects to an existing SQL database.
"""

from sqlalchemy import text
import os
import asyncio
from main import create_sql_engine

async def reinit_db():
    list_filename = [
        "book.sql", 
    ]
    async with create_sql_engine().begin() as conn:
        for filename in list_filename:
            with open(os.path.join("sql", filename)) as f:
                for sql_req in f.read().split(";"):
                    if len(sql_req.strip()) > 0:
                        await conn.execute(text(sql_req))
                await conn.execute(text("COMMIT;"))

if __name__ == "__main__":
    asyncio.run(reinit_db())