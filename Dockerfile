FROM python:3.13-alpine3.21 AS builder

ARG HGRPGPASSFILE
ARG HGRPGSERVICEFILE
ENV PGPASSFILE="/app/.hgr_pgpass"
ENV PGSERVICEFILE="/app/.pg_service.conf"

EXPOSE 8000
WORKDIR /app 
COPY requirements.txt /app
RUN apk update && apk add --no-cache build-base libpq-dev
RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY ./hgr-django /app
RUN printf $HGRPGPASSFILE > $PGPASSFILE && printf $HGRPGSERVICEFILE > $PGSERVICEFILE && chmod 600 $PGPASSFILE $PGSERVICEFILE
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
