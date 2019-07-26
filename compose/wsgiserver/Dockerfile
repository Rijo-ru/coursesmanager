FROM python:3.7-alpine

RUN apk update && \
    apk upgrade && \
    apk add --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    openssl-dev \
    libffi-dev \
    libsodium-dev \
    build-base && \
    pip install --upgrade pip && \
    pip install psycopg2 && \
    pip install pynacl && \
    pip install cryptography --no-binary cryptography && \
    pip install wheel pipenv

RUN mkdir -p /project/CoursesManager/apps && \
    mkdir -p /project/CoursesManager/static && \
    mkdir -p /project/CoursesManager/core && \
    mkdir -p /project/CoursesManager/templates

WORKDIR /project/CoursesManager

COPY Pipfile Pipfile.lock ./
RUN set -ex && pipenv install --deploy --system

COPY ./compose/wsgiserver/startgunicorn /usr/local/bin/

RUN chmod +x /usr/local/bin/startgunicorn

ADD ./apps ./apps
ADD ./core ./core
ADD ./manage.py ./
ADD ./gunicorn.conf.py ./
ADD ./static ./static
ADD ./templates ./templates

ADD ./generate_students.py ./

ADD ./.env ./

ENV PYTHONPATH=$PYTHONPATH

CMD ["startgunicorn"]