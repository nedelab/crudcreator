import pytest
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="CRUDCreator run test",
        description="CRUDCreator script to run the unit tests in current environment"
    )
    parser.add_argument("CRUDCREATOR_TEST_ENV", type=str)
    args = parser.parse_args()
    os.environ["CRUDCREATOR_TEST_ENV"] = args.CRUDCREATOR_TEST_ENV
    print(f"tests starting with CRUDCREATOR_TEST_ENV={os.environ['CRUDCREATOR_TEST_ENV']}")
    from test.utils import reinit_db
    from test.settings import settings
    from test.loop import loop
    print("The settings are :")
    print(settings)
    loop.run_until_complete(reinit_db())
    pytest.main(["test"])