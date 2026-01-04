FROM python:3.13.11-alpine

WORKDIR /app

EXPOSE 5001

COPY requirements.txt ./

# Required for psycopg2 Python Library
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc
RUN apk add --no-cache --virtual .build-deps musl-dev
RUN apk add --no-cache --virtual .build-deps postgresql-dev

RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r requirements.txt --no-cache-dir
RUN apk --purge del .build-deps

COPY . .

# Binds the app to localhost (instead of 127.0.0.1),
# which allows to expose it as Docker port (DEV ONLY!)
CMD ["flask", "run", "--port=5001", "--host=0.0.0.0"]
