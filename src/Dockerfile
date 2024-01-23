FROM python:3.10

ENV TZ=Europe/Moscow

WORKDIR /src

RUN apt-get update && apt-get install -y netcat-traditional

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY . /src
CMD ["alembic", "upgrade", "head"]