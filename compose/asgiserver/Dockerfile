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
    pip install wheel pipenv && \
    pip install daphne

RUN mkdir -p /asgi/files

WORKDIR /asgi/files

COPY Pipfile Pipfile.lock ./
RUN set -ex && pipenv install --deploy --system --dev

WORKDIR /project/CoursesManager

ADD ./compose/asgiserver/startdaphne /usr/local/bin/

RUN chmod +x /usr/local/bin/startdaphne

ENV PYTHONPATH=$PYTHONPATH

CMD ["startdaphne"]