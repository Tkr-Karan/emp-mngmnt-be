# Employee Management System - Backend API

A Django REST API backend with MongoDB for managing employees. This is a beginner-friendly implementation with clear structure and documentation.

## Tech Stack

- **Django 4.2.7** - Web framework
- **Django REST Framework** - For building REST APIs
- **MongoDB** - NoSQL database
- **MongoEngine** - MongoDB ODM (Object Document Mapper) for Django

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8+** - Check with `python3 --version`
2. **MongoDB** - Install MongoDB on your system
   - Ubuntu/Debian: `sudo apt-get install mongodb`
   - macOS: `brew install mongodb-community`
   - Windows: Download from [MongoDB website](https://www.mongodb.com/try/download/community)

3. **pip** - Python package manager (usually comes with Python)

## Installation & Setup

### Step 1: Create Virtual Environment

```bash
# Navigate to project directory
cd /home/karan/Desktop/Learning/Assignment/BE

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Start MongoDB

Make sure MongoDB is running on your system:

```bash
# Start MongoDB service
# On Linux:
sudo systemctl start mongodb

# On macOS:
brew services start mongodb-community

# On Windows:
# MongoDB should start automatically as a service
```

Verify MongoDB is running:
```bash
mongosh  # or mongo (older versions)
```

### Step 4: Configure MongoDB Connection

Edit `employee_management/settings.py` if your MongoDB requires authentication:

```python
MONGODB_DATABASE = {
    'name': 'employee_db',
    'host': 'localhost',
    'port': 27017,
    'username': 'your_username',  # Only if required
    'password': 'your_password',  # Only if required
}
```

### Step 5: Run Django Server

```bash
# Make migrations (not needed for MongoDB, but Django requires it)
python manage.py makemigrations

# Run the server
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`

## API Endpoints

### Base URL: `http://localhost:8000/api/`

---

## Employee Management APIs

### 1. Get All Employees
- **URL:** `/api/employees/`
- **Method:** `GET`
- **Response:** List of all employees

**Example:**
```bash
curl http://localhost:8000/api/employees/
```

### 2. Create New Employee
- **URL:** `/api/employees/`
- **Method:** `POST`
- **Body (JSON):**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "department": "Engineering",
    "position": "Software Developer",
    "salary": 75000
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/employees/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "department": "Engineering",
    "position": "Software Developer",
    "salary": 75000
  }'
```

### 3. Get Employee by ID
- **URL:** `/api/employees/<employee_id>/`
- **Method:** `GET`

**Example:**
```bash
curl http://localhost:8000/api/employees/507f1f77bcf86cd799439011/
```

### 4. Update Employee (Full Update)
- **URL:** `/api/employees/<employee_id>/`
- **Method:** `PUT`
- **Body (JSON):** All fields required

**Example:**
```bash
curl -X PUT http://localhost:8000/api/employees/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com",
    "phone": "+1234567890",
    "department": "Marketing",
    "position": "Marketing Manager",
    "salary": 85000
  }'
```

### 5. Partial Update Employee
- **URL:** `/api/employees/<employee_id>/update/`
- **Method:** `PATCH`
- **Body (JSON):** Only fields to update

**Example:**
```bash
curl -X PATCH http://localhost:8000/api/employees/507f1f77bcf86cd799439011/update/ \
  -H "Content-Type: application/json" \
  -d '{
    "salary": 90000
  }'
```

### 6. Delete Employee
- **URL:** `/api/employees/<employee_id>/`
- **Method:** `DELETE`

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/employees/507f1f77bcf86cd799439011/
```

---

## Attendance Management APIs

### 1. Mark Attendance
- **URL:** `/api/attendance/`
- **Method:** `POST`
- **Body (JSON):**
```json
{
    "employeeId": "EMP001",
    "date": "2024-01-15",
    "status": "Present"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/attendance/ \
  -H "Content-Type: application/json" \
  -d '{
    "employeeId": "EMP001",
    "date": "2024-01-15",
    "status": "Present"
  }'
```

**Status Options:** `Present` or `Absent`

### 2. Get All Attendance Records
- **URL:** `/api/attendance/`
- **Method:** `GET`
- **Query Parameters (optional):**
  - `employeeId` - Filter by employee ID
  - `date` - Filter by date (YYYY-MM-DD format)

**Example:**
```bash
# Get all attendance
curl http://localhost:8000/api/attendance/

# Get attendance for specific employee
curl http://localhost:8000/api/attendance/?employeeId=EMP001

# Get attendance for specific date
curl http://localhost:8000/api/attendance/?date=2024-01-15
```

### 3. Get Employee Attendance Records
- **URL:** `/api/employees/<employeeId>/attendance/`
- **Method:** `GET`
- **Query Parameters (optional):**
  - `start_date` - Start date for date range (YYYY-MM-DD)
  - `end_date` - End date for date range (YYYY-MM-DD)

**Example:**
```bash
# Get all attendance for employee
curl http://localhost:8000/api/employees/EMP001/attendance/

# Get attendance with date range
curl "http://localhost:8000/api/employees/EMP001/attendance/?start_date=2024-01-01&end_date=2024-01-31"
```

**Response includes statistics:**
```json
{
    "success": true,
    "employee": {...},
    "data": [...],
    "count": 10,
    "statistics": {
        "total": 10,
        "present": 8,
        "absent": 2
    }
}
```

### 4. Get Attendance by ID
- **URL:** `/api/attendance/<attendance_id>/`
- **Method:** `GET`

**Example:**
```bash
curl http://localhost:8000/api/attendance/507f1f77bcf86cd799439011/
```

### 5. Update Attendance
- **URL:** `/api/attendance/<attendance_id>/`
- **Method:** `PUT`
- **Body (JSON):** All fields required

**Example:**
```bash
curl -X PUT http://localhost:8000/api/attendance/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json" \
  -d '{
    "employeeId": "EMP001",
    "date": "2024-01-15",
    "status": "Absent"
  }'
```

### 6. Delete Attendance
- **URL:** `/api/attendance/<attendance_id>/`
- **Method:** `DELETE`

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/attendance/507f1f77bcf86cd799439011/
```

---

## Validation Rules

### Employee Validation

1. **Required Fields:**
   - `employeeId` - Cannot be empty, must be unique
   - `full_name` - Cannot be empty
   - `email` - Must be valid email format, must be unique

2. **Email Validation:**
   - Must be valid email format (e.g., user@example.com)
   - Duplicate emails are not allowed

3. **Employee ID Validation:**
   - Must be unique
   - Duplicate employee IDs are not allowed

### Attendance Validation

1. **Required Fields:**
   - `employeeId` - Must exist in the system
   - `date` - Required, cannot be in the future
   - `status` - Must be either "Present" or "Absent"

2. **Date Validation:**
   - Cannot be in the future
   - Must be in YYYY-MM-DD format

3. **Duplicate Prevention:**
   - Same employee cannot have multiple attendance records for the same date

## Response Format

### Success Response
```json
{
    "success": true,
    "message": "Employee created successfully",
    "data": {
        "id": "507f1f77bcf86cd799439011",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "department": "Engineering",
        "position": "Software Developer",
        "salary": 75000,
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-01-15T10:30:00"
    }
}
```

### Error Response
```json
{
    "error": true,
    "message": "Validation failed",
    "details": {
        "email": ["Employee with this email already exists"]
    }
}
```

## HTTP Status Codes

- `200 OK` - Successful GET, PUT, PATCH, DELETE
- `201 Created` - Successful POST (creation)
- `400 Bad Request` - Validation error or invalid request
- `404 Not Found` - Employee not found
- `500 Internal Server Error` - Server error

## Project Structure

```
BE/
├── employee_management/      # Main Django project
│   ├── __init__.py
│   ├── settings.py           # Django settings with MongoDB config
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── employees/                # Employees app
│   ├── __init__.py
│   ├── models.py            # Employee MongoDB model
│   ├── serializers.py       # API serializers
│   ├── views.py             # API views
│   ├── urls.py              # App URL routes
│   └── utils.py             # Utility functions
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Testing the API

You can test the API using:

1. **cURL** (command line)
2. **Postman** (GUI tool)
3. **Browser** (for GET requests only)
4. **Python requests library**

### Example Python Test Script

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Create employee
response = requests.post(f"{BASE_URL}/employees/", json={
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "department": "Engineering",
    "position": "Developer",
    "salary": 75000
})
print(response.json())

# Get all employees
response = requests.get(f"{BASE_URL}/employees/")
print(response.json())
```

## Troubleshooting

### MongoDB Connection Error
- Make sure MongoDB is running: `sudo systemctl status mongodb`
- Check MongoDB connection settings in `settings.py`
- Verify MongoDB is accessible: `mongosh`

### Import Errors
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use
- Change port: `python manage.py runserver 8001`
- Or kill the process using port 8000

## Notes for Beginners

1. **Virtual Environment:** Always activate your virtual environment before working
2. **MongoDB:** MongoDB must be running before starting Django server
3. **No Migrations:** MongoDB doesn't use Django migrations like SQL databases
4. **ObjectId:** MongoDB uses ObjectId instead of auto-incrementing integers
5. **JSON Format:** Always send data in JSON format for POST/PUT/PATCH requests

## Next Steps

- Connect a frontend application
- Add more employee fields
- Implement search and filtering
- Add pagination for large datasets

## License

This project is for educational purposes.
