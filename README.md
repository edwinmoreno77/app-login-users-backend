# Authentication Backend

This is an authentication backend developed with Flask that provides endpoints for user registration, login, and user management.

## Prerequisites

- Python 3.8 or higher
- Pipenv (dependency manager)
- MongoDB (local or MongoDB Atlas)

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

## MongoDB Configuration

### Local MongoDB
1. Install MongoDB Community Edition from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
2. Start MongoDB service
3. Set `MONGODB_URI` in your `.env` file:
```
MONGODB_URI=mongodb://localhost:27017/login_db
```

### MongoDB Atlas (Recommended for Production)
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Set up database access (create a user with password)
4. Set up network access (allow access from anywhere or specific IPs)
5. Get your connection string from the "Connect" button
6. Set `MONGODB_URI` in your `.env` file:
```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/login_db?retryWrites=true&w=majority
```

### Database Initialization
To initialize the database with sample users, run:
```bash
python init_db.py
```

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

## Database Structure

### User Model
The application uses MongoDB with the following user schema:

```python
{
    'name': String,          # Required, max length 100
    'email': String,         # Required, unique
    'password_hash': String, # Required, hashed password
    'is_active': Boolean,    # Default: true
    'created_at': DateTime,  # Auto-generated
    'updated_at': DateTime,  # Auto-updated
    'last_login': DateTime,  # Updated on login
    'profile': {
        'avatar': String,    # Optional
        'phone': String,     # Optional
        'address': String    # Optional
    }
}
```

### Indexes
The following indexes are created for optimal performance:
- `email` (unique)
- `is_active`
- `created_at`

## Development Notes

- JWT is used for authentication
- Passwords are securely stored with hash
- Email and password validations are implemented
- MongoDB Atlas is recommended for production deployments
- The database connection is configured through environment variables 