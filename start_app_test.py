import uvicorn
import os
import asyncio
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="CRUDCreator start app test",
        description="CRUDCreator script to start a test app in current environment"
    )
    parser.add_argument("CRUDCREATOR_TEST_ENV", type=str)
    args = parser.parse_args()
    os.environ["CRUDCREATOR_TEST_ENV"] = args.CRUDCREATOR_TEST_ENV
    print(f"app starting with CRUDCREATOR_TEST_ENV={os.environ['CRUDCREATOR_TEST_ENV']}")
    from test.utils import reinit_db
    from test.settings import settings
    from test.loop import loop
    from test.app import app
    print("The settings are :")
    print(settings)
    loop.run_until_complete(reinit_db())
    loop.run_until_complete(
        uvicorn.Server(
            uvicorn.Config(app=app, loop=loop, port=8081)
        ).serve()
    )