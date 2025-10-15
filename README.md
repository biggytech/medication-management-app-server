# Medication Management App - Server

## Requirements
- Python 3.13.3 or higher

## Getting Started
1. Install dependencies from `requirements.txt`
2. Create DB with `python db/create_db.py`
3. Start with `make dev`

## Development
1. Create a migration `make create-migration`
2. Run migrations `make migrate`

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
