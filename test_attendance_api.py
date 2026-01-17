"""
Simple test script for Attendance API
Run this after starting the Django server to test the Attendance API
"""
import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8000/api"

def print_response(response, title):
    """Helper function to print API responses"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))

def test_mark_attendance():
    """Test marking attendance for an employee"""
    data = {
        "employeeId": "EMP001",
        "date": str(date.today()),
        "status": "Present"
    }
    response = requests.post(f"{BASE_URL}/attendance/", json=data)
    print_response(response, "MARK ATTENDANCE (Present)")
    return response.json().get('data', {}).get('id') if response.status_code == 201 else None

def test_mark_attendance_absent():
    """Test marking attendance as absent"""
    yesterday = date.today() - timedelta(days=1)
    data = {
        "employeeId": "EMP001",
        "date": str(yesterday),
        "status": "Absent"
    }
    response = requests.post(f"{BASE_URL}/attendance/", json=data)
    print_response(response, "MARK ATTENDANCE (Absent)")

def test_get_all_attendance():
    """Test getting all attendance records"""
    response = requests.get(f"{BASE_URL}/attendance/")
    print_response(response, "GET ALL ATTENDANCE RECORDS")

def test_get_attendance_by_employee():
    """Test getting attendance by employee ID"""
    response = requests.get(f"{BASE_URL}/attendance/?employeeId=EMP001")
    print_response(response, "GET ATTENDANCE BY EMPLOYEE ID")

def test_get_attendance_by_date():
    """Test getting attendance by date"""
    today = str(date.today())
    response = requests.get(f"{BASE_URL}/attendance/?date=" + today)
    print_response(response, "GET ATTENDANCE BY DATE")

def test_get_employee_attendance():
    """Test getting attendance for a specific employee"""
    response = requests.get(f"{BASE_URL}/employees/EMP001/attendance/")
    print_response(response, "GET EMPLOYEE ATTENDANCE RECORDS")

def test_get_employee_attendance_date_range():
    """Test getting attendance for employee with date range"""
    start_date = str(date.today() - timedelta(days=7))
    end_date = str(date.today())
    response = requests.get(f"{BASE_URL}/employees/EMP001/attendance/?start_date=" + start_date + "&end_date=" + end_date)
    print_response(response, "GET EMPLOYEE ATTENDANCE (Date Range)")

def test_update_attendance(attendance_id):
    """Test updating an attendance record"""
    if not attendance_id:
        print("\n⚠ No attendance ID available to test UPDATE")
        return
    data = {
        "employeeId": "EMP001",
        "date": str(date.today()),
        "status": "Absent"
    }
    response = requests.put(f"{BASE_URL}/attendance/{attendance_id}/", json=data)
    print_response(response, "UPDATE ATTENDANCE")

def test_duplicate_attendance():
    """Test duplicate attendance validation (should fail)"""
    data = {
        "employeeId": "EMP001",
        "date": str(date.today()),
        "status": "Present"
    }
    response = requests.post(f"{BASE_URL}/attendance/", json=data)
    print_response(response, "TEST DUPLICATE ATTENDANCE (Should Fail)")

def test_future_date():
    """Test marking attendance for future date (should fail)"""
    future_date = date.today() + timedelta(days=1)
    data = {
        "employeeId": "EMP001",
        "date": str(future_date),
        "status": "Present"
    }
    response = requests.post(f"{BASE_URL}/attendance/", json=data)
    print_response(response, "TEST FUTURE DATE (Should Fail)")

def test_invalid_employee():
    """Test marking attendance for invalid employee (should fail)"""
    data = {
        "employeeId": "INVALID123",
        "date": str(date.today()),
        "status": "Present"
    }
    response = requests.post(f"{BASE_URL}/attendance/", json=data)
    print_response(response, "TEST INVALID EMPLOYEE (Should Fail)")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("ATTENDANCE API TEST SCRIPT")
    print("="*50)
    print("\n⚠ Make sure Django server is running on http://localhost:8000")
    print("⚠ Make sure you have at least one employee with employeeId='EMP001'")
    print("⚠ Run: python manage.py runserver")
    print("\nPress Enter to start testing...")
    input()
    
    try:
        # Test marking attendance
        attendance_id = test_mark_attendance()
        
        # Test marking absent
        test_mark_attendance_absent()
        
        # Test getting all attendance
        test_get_all_attendance()
        
        # Test getting attendance by employee
        test_get_attendance_by_employee()
        
        # Test getting attendance by date
        test_get_attendance_by_date()
        
        # Test getting employee attendance
        test_get_employee_attendance()
        
        # Test getting employee attendance with date range
        test_get_employee_attendance_date_range()
        
        # Test updating attendance
        test_update_attendance(attendance_id)
        
        # Test validations
        test_duplicate_attendance()
        test_future_date()
        test_invalid_employee()
        
        print("\n" + "="*50)
        print("✅ ALL ATTENDANCE TESTS COMPLETED")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server.")
        print("Make sure Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
