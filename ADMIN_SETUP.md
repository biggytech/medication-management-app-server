# Admin Panel Setup

This document explains how to set up and use the admin panel for the Medication Management App.

## Environment Setup

1. Create a `.env` file in the root directory with the following content:

```env
# Admin credentials for admin panel access
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Secret key for Flask sessions (change this in production)
SECRET_KEY=your-secret-key-change-this-in-production

# Database configuration (if needed)
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=medication_management
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
```

2. Install required dependencies:

```bash
pip install python-dotenv
```

## Accessing the Admin Panel

1. Start the Flask application:
```bash
python app.py
```

2. Navigate to `http://localhost:5000/admin/login`

3. Login with the credentials specified in your `.env` file:
   - Username: `admin` (or your custom ADMIN_USERNAME)
   - Password: `admin123` (or your custom ADMIN_PASSWORD)

## Admin Panel Features

### Dashboard
- Overview of system statistics
- Quick access to user and doctor management
- Real-time counts of users, doctors, and guest users

### User Management
- View all users in the system
- Add new users with full name, email, and password
- Edit existing user information
- Change user passwords
- Delete users
- Distinguish between registered users and guest users

### Doctor Management
- View all doctors with their associated user information
- Create new doctor profiles by linking to existing users
- Edit doctor specialisation, place of work, and photo URL
- Delete doctor profiles

## Security Notes

- The admin panel uses session-based authentication
- Admin credentials are stored in environment variables
- All admin routes are protected with the `@admin_required` decorator
- Change the default admin credentials in production
- Use a strong secret key for Flask sessions in production

## API Endpoints

The admin panel provides the following API endpoints:

### Users
- `GET /admin/api/users` - Get all users
- `POST /admin/api/users` - Create new user
- `PUT /admin/api/users/<id>` - Update user
- `DELETE /admin/api/users/<id>` - Delete user

### Doctors
- `GET /admin/api/doctors` - Get all doctors
- `POST /admin/api/doctors` - Create new doctor
- `PUT /admin/api/doctors/<id>` - Update doctor
- `DELETE /admin/api/doctors/<id>` - Delete doctor

All API endpoints require admin authentication.
