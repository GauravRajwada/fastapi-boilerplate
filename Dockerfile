FROM python:3.12 as python-base

WORKDIR /src

COPY . .

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN poetry install 

RUN pip3 install pymongo

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "src.app.main:app", "--bind", "0.0.0.0:8000"]
