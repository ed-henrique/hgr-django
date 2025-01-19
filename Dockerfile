FROM python:3.13-alpine3.21 AS builder

ENV PGSERVICEFILE="/app/.pg_service.conf"

EXPOSE 8000
WORKDIR /app 
COPY requirements.txt /app
RUN apk update && apk add --no-cache build-base libpq-dev
RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY ./hgr-django /app
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
