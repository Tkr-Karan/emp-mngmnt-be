"""
Simple test script for Employee API
Run this after starting the Django server to test the API
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_response(response, title):
    """Helper function to print API responses"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))

def test_create_employee():
    """Test creating a new employee"""
    data = {
        "employeeId": "EMP001",
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "department": "Engineering"
    }
    response = requests.post(f"{BASE_URL}/employees/", json=data)
    print_response(response, "CREATE EMPLOYEE")
    return response.json().get('data', {}).get('id') if response.status_code == 201 else None

def test_get_all_employees():
    """Test getting all employees"""
    response = requests.get(f"{BASE_URL}/employees/")
    print_response(response, "GET ALL EMPLOYEES")

def test_get_employee(employee_id):
    """Test getting a specific employee"""
    if not employee_id:
        print("\n⚠ No employee ID available to test GET")
        return
    response = requests.get(f"{BASE_URL}/employees/{employee_id}/")
    print_response(response, "GET EMPLOYEE BY ID")

def test_update_employee(employee_id):
    """Test updating an employee"""
    if not employee_id:
        print("\n⚠ No employee ID available to test UPDATE")
        return
    data = {
        "employeeId": "EMP002",
        "full_name": "Jane Doe",
        "email": "jane.doe@example.com",
        "department": "Marketing"
    }
    response = requests.put(f"{BASE_URL}/employees/{employee_id}/", json=data)
    print_response(response, "UPDATE EMPLOYEE (PUT)")

def test_partial_update_employee(employee_id):
    """Test partial update of an employee"""
    if not employee_id:
        print("\n⚠ No employee ID available to test PARTIAL UPDATE")
        return
    data = {
        "department": "Sales"
    }
    response = requests.patch(f"{BASE_URL}/employees/{employee_id}/update/", json=data)
    print_response(response, "PARTIAL UPDATE EMPLOYEE (PATCH)")

def test_duplicate_email():
    """Test duplicate email validation"""
    data = {
        "employeeId": "EMP003",
        "full_name": "Test User",
        "email": "john.doe@example.com",  # Same email as first employee
        "department": "IT"
    }
    response = requests.post(f"{BASE_URL}/employees/", json=data)
    print_response(response, "TEST DUPLICATE EMAIL (Should Fail)")

def test_duplicate_employeeId():
    """Test duplicate employeeId validation"""
    data = {
        "employeeId": "EMP001",  # Same employeeId as first employee
        "full_name": "Test User",
        "email": "test@example.com",
        "department": "IT"
    }
    response = requests.post(f"{BASE_URL}/employees/", json=data)
    print_response(response, "TEST DUPLICATE EMPLOYEE ID (Should Fail)")

def test_invalid_email():
    """Test invalid email validation"""
    data = {
        "employeeId": "EMP004",
        "full_name": "Test User",
        "email": "invalid-email",  # Invalid email format
        "department": "IT"
    }
    response = requests.post(f"{BASE_URL}/employees/", json=data)
    print_response(response, "TEST INVALID EMAIL (Should Fail)")

def test_delete_employee(employee_id):
    """Test deleting an employee"""
    if not employee_id:
        print("\n⚠ No employee ID available to test DELETE")
        return
    response = requests.delete(f"{BASE_URL}/employees/{employee_id}/")
    print_response(response, "DELETE EMPLOYEE")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("EMPLOYEE API TEST SCRIPT")
    print("="*50)
    print("\n⚠ Make sure Django server is running on http://localhost:8000")
    print("⚠ Run: python manage.py runserver")
    print("\nPress Enter to start testing...")
    input()
    
    try:
        # Test creating employee
        employee_id = test_create_employee()
        
        # Test getting all employees
        test_get_all_employees()
        
        # Test getting specific employee
        test_get_employee(employee_id)
        
        # Test updating employee
        test_update_employee(employee_id)
        
        # Test partial update
        test_partial_update_employee(employee_id)
        
        # Test validations
        test_duplicate_email()
        test_duplicate_employeeId()
        test_invalid_email()
        
        # Test deleting employee (commented out so you can see the employee in database)
        # test_delete_employee(employee_id)
        
        print("\n" + "="*50)
        print("✅ ALL TESTS COMPLETED")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server.")
        print("Make sure Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
