FROM python:3.9.19-alpine3.19

WORKDIR /app

COPY test/docker/python3.9/requirements.txt /app/test/docker/python3.9/requirements.txt

RUN pip install -r test/docker/python3.9/requirements.txt

RUN pip install pytest pytest-asyncio httpx asyncpg pg8000

COPY . /app

CMD python -u run_test.py $CRUDCREATOR_TEST_ENV