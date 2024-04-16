FROM python:3.12.3-alpine3.19

WORKDIR /app

COPY test/docker/sqlalchemy1.4/requirements.txt /app/test/docker/sqlalchemy1.4/requirements.txt

RUN pip install -r test/docker/sqlalchemy1.4/requirements.txt

RUN pip install pytest pytest-asyncio httpx asyncpg pg8000

COPY . /app

CMD python -u run_test.py $CRUDCREATOR_TEST_ENV