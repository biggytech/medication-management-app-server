# Medication Management App - Server

This is server (API) for the mobile application.

Mobile application repo: https://github.com/biggytech/medication-management-mobile-app

## Requirements

- Python 3.13.3 or higher

## Run the App

### Run locally

1. Prepare `.env` file by using env file example
2. Install dependencies from `requirements.txt`
    - create virtual environment: `python3 -m venv .venv`
    - activate the virtual environment: `source .venv/bin/activate`
    - install dependencies: `pip install -r requirements.txt`
3. Start with `flask run --port=8000`

### Run from Docker

1. Prepare `.env` file by using env file example
2. `docker compose up -d`
    - Rebuild: `docker builder prune && docker compose up --build -d`

## ENV FILE example

See [.env.example](./.env.example)
