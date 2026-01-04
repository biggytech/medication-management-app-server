# Medication Management App - Server

## Requirements

- Python 3.13.3 or higher

## Getting Started

1. Install dependencies from `requirements.txt`
    - create virtual environment: `python3 -m venv .venv`
    - activate the virtual environment: `source .venv/bin/activate`
    - install dependencies: `pip install -r requirements.txt`
2. Create DB with `python db/create_db.py`
3. Create cascade statements by running `db/migrations/add_delete_cascade_statements.sql`
4. Start with `make dev`

### Build from Docker

1. Build Docker image: `docker build . -t medication-management-app-server`
2. Run: `docker run -p 5001:5001 -it medication-management-app-server`

#### Production Mode

TODO: think of using this approach https://flask.palletsprojects.com/en/stable/tutorial/deploy/

## ENV FILE example

```
# Database
DB_DRIVER_NAME=postgresql+psycopg2
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=medication

# Secrets
JWT_SECRET_KEY=my-jwt-secret-key
SECRET_KEY=your-secret-key-change-this-in-production

# Admin login
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
```
