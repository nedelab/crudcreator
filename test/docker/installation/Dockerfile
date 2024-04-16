FROM python:3.12.3-alpine3.19

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

RUN ./scripts/build.ps1

FROM python:3.12.3-alpine3.19

COPY --from=0 /app/dist /dist

RUN pip install $(find /dist/*.whl -type f)

WORKDIR /app

RUN crudcreator init simple

RUN pip install -r requirements.txt

RUN pip install pytest pytest-asyncio httpx

RUN pytest test

RUN python -u reinit_db.py

CMD python -u main.py