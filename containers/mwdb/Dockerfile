FROM python:3.8

RUN apt update && apt install -y build-essential libffi-dev libfuzzy-dev postgresql-client libmagic1

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./uwsgi.ini ./
COPY ./start.sh ./
COPY ./init_minio.py ./

CMD ["/app/start.sh"]
