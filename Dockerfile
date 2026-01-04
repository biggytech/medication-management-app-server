# Shared folder with venv built packages
ARG VIRTUAL_ENV=/opt/venv

# Build stage:
FROM python:3.13.11-alpine AS build
ARG VIRTUAL_ENV
ENV VIRTUAL_ENV=$VIRTUAL_ENV

WORKDIR /app

# Required for psycopg2 Python Library
RUN apk add postgresql17-dev

# Enable venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

RUN apk del postgresql17-dev

# Run stage:
FROM python:3.13.11-alpine
ARG VIRTUAL_ENV
ENV VIRTUAL_ENV=$VIRTUAL_ENV

WORKDIR /app

RUN apk add postgresql17-dev

# Copy generated packages from the build stage:
COPY --from=build $VIRTUAL_ENV $VIRTUAL_ENV
# Enabled venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./.env.docker ./.env
COPY ./db ./db
COPY ./models ./models
COPY ./routers ./routers
COPY ./services ./services
COPY ./templates ./templates
COPY ./app.py ./app.py
COPY ./DejaVuSerif-Bold.ttf ./DejaVuSerif-Bold.ttf
COPY ./DejaVuSerif-Bold.ttf ./DejaVuSerif-Bold.ttf

EXPOSE 5001

# host param binds the app to localhost (instead of 127.0.0.1),
# which allows to expose it as Docker port (DEV ONLY!)
CMD ["flask", "run", "--port=5001", "--host=0.0.0.0"]
