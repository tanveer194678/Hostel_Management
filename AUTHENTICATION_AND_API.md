# Student Management System - Authentication & API Setup Guide

## Installation

Install the required packages:
```bash
pip install -r requirements.txt
```

## Features Added

### 1. Authentication System
- User Registration (`/register/`)
- User Login (`/login/`)
- User Logout (`/logout/`)
- Session-based authentication
- @login_required decorators on protected views

### 2. CORS Middleware
- Enabled for localhost development
- Allows requests from http://localhost:3000, http://localhost:8000
- Configurable in settings.py

### 3. REST API Endpoints

#### Authentication
- POST `/api-auth/login/` - Login and get session
- POST `/api-auth/logout/` - Logout

#### Student API (All require authentication)
- GET `/api/students/` - List all students
- POST `/api/students/create/` - Create new student
- GET `/api/students/{id}/` - Get student detail
- PUT `/api/students/{id}/` - Update student
- DELETE `/api/students/{id}/` - Delete student

#### Using the ViewSet
- GET `/api/students/` - List all students
- POST `/api/students/` - Create new student
- GET `/api/students/{id}/` - Get student detail
- PUT `/api/students/{id}/` - Update student
- PATCH `/api/students/{id}/` - Partial update
- DELETE `/api/students/{id}/` - Delete student

## Database Migrations

If you modified the model, run:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Testing the API

### Using cURL:
```bash
# Login
curl -X POST http://localhost:8000/api-auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'

# Get students
curl -X GET http://localhost:8000/api/students/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create student
curl -X POST http://localhost:8000/api/students/create/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John","age":20,"grade":"A"}'
```

### Using Python:
```python
import requests

# Login
session = requests.Session()
response = session.post('http://localhost:8000/api-auth/login/', 
    data={'username': 'user', 'password': 'pass'})

# Get students
response = session.get('http://localhost:8000/api/students/')
print(response.json())

# Create student
response = session.post('http://localhost:8000/api/students/create/',
    json={'name': 'John', 'age': 20, 'grade': 'A'})
print(response.json())
```

## Web Interface URLs

- `/` - Home page (public)
- `/register/` - Register new account (public)
- `/login/` - Login page (public)
- `/logout/` - Logout (requires login)
- `/dashboard/` - Dashboard (requires login)
- `/add-student/` - Add student form (requires login)
- `/view-students/` - View all students (requires login)
- `/delete-student/<id>/` - Delete student (requires login)

## Configuration

### CORS Settings (settings.py)
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### REST Framework Settings
- Default authentication: SessionAuthentication
- Default permission: IsAuthenticated
- Pagination: 10 items per page
