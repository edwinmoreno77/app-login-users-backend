# Authentication Backend

This is an authentication backend developed with Flask that provides endpoints for user registration, login, and user management.

## Prerequisites

- Python 3.8 or higher
- Pipenv (dependency manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backendLogin
```

2. Install dependencies using Pipenv:
```bash
pipenv install
```

3. Configure environment variables:
   - Copy `example.env` to `.env`
   - Adjust variables as needed

## Running the Project

1. Activate the virtual environment:
```bash
pipenv shell
```

2. Start the application:
```bash
python app.py
```

The application will run on `http://localhost:5004`

## Available Endpoints

### User Registration
- **URL**: `/api/register`
- **Method**: POST
- **Body**:
  ```json
  {
    "name": "User Name",
    "email": "user@example.com",
    "password": "password",
    "avatar": "avatar_url",
    "phone": "123456789",
    "address": "Address"
  }
  ```

### Login
- **URL**: `/api/login`
- **Method**: POST
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password"
  }
  ```

### Get Current User
- **URL**: `/api/users/me`
- **Method**: GET
- **Headers**: 
  - Authorization: Bearer {token}

### List Users
- **URL**: `/api/users`
- **Method**: GET
- **Headers**: 
  - Authorization: Bearer {token}

## CORS Configuration

The backend is configured to accept requests from:
- Origin: `http://localhost:5173`
- Methods: GET, POST, PUT, DELETE, OPTIONS
- Allowed Headers: Content-Type, Authorization

## Project Structure

```
backendLogin/
├── app.py              # Main application
├── config.py           # Configurations
├── models.py           # Data models
├── routes.py           # API routes
├── init_db.py          # Database initialization script
├── Pipfile            # Project dependencies
├── Pipfile.lock       # Exact dependency versions
└── example.env        # Environment variables example
```

## Development Notes

- JWT is used for authentication
- Passwords are securely stored with hash
- Email and password validations are implemented 