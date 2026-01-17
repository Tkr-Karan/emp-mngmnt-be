"""
Views for Employee API
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mongoengine.errors import DoesNotExist, ValidationError
from bson.errors import InvalidId
from .models import Employee
from .serializers import EmployeeSerializer


@api_view(['GET', 'POST'])
def employee_list_create(request):
    """
    List all employees or create a new employee
    
    GET /api/employees/ - List all employees
    POST /api/employees/ - Create a new employee
    """
    if request.method == 'GET':
        try:
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'count': len(serializer.data)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': True,
                'message': 'Failed to retrieve employees',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
            serializer = EmployeeSerializer(data=request.data)
            if serializer.is_valid():
                employee = serializer.save()
                return Response({
                    'success': True,
                    'message': 'Employee created successfully',
                    'data': EmployeeSerializer(employee).data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error': True,
                    'message': 'Validation failed',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({
                'error': True,
                'message': 'Validation error',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': True,
                'message': 'Failed to create employee',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, employee_id):
    """
    Retrieve, update or delete an employee
    
    GET /api/employees/<id>/ - Get employee details
    PUT /api/employees/<id>/ - Update employee
    DELETE /api/employees/<id>/ - Delete employee
    """
    try:
        employee = Employee.objects.get(id=employee_id)
    except (DoesNotExist, Employee.DoesNotExist):
        return Response({
            'error': True,
            'message': 'Employee not found',
            'details': f'No employee found with id: {employee_id}'
        }, status=status.HTTP_404_NOT_FOUND)
    except (InvalidId, ValueError) as e:
        return Response({
            'error': True,
            'message': 'Invalid employee ID',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': True,
            'message': 'Error retrieving employee',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if request.method == 'GET':
        try:
            serializer = EmployeeSerializer(employee)
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': True,
                'message': 'Failed to retrieve employee',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PUT':
        try:
            serializer = EmployeeSerializer(employee, data=request.data, partial=False)
            if serializer.is_valid():
                updated_employee = serializer.save()
                return Response({
                    'success': True,
                    'message': 'Employee updated successfully',
                    'data': EmployeeSerializer(updated_employee).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': True,
                    'message': 'Validation failed',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({
                'error': True,
                'message': 'Validation error',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': True,
                'message': 'Failed to update employee',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'DELETE':
        try:
            employee.delete()
            return Response({
                'success': True,
                'message': 'Employee deleted successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': True,
                'message': 'Failed to delete employee',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
def employee_partial_update(request, employee_id):
    """
    Partially update an employee (PATCH method)
    
    PATCH /api/employees/<id>/ - Partially update employee
    """
    try:
        employee = Employee.objects.get(id=employee_id)
    except (DoesNotExist, Employee.DoesNotExist):
        return Response({
            'error': True,
            'message': 'Employee not found',
            'details': f'No employee found with id: {employee_id}'
        }, status=status.HTTP_404_NOT_FOUND)
    except (InvalidId, ValueError) as e:
        return Response({
            'error': True,
            'message': 'Invalid employee ID',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': True,
            'message': 'Error retrieving employee',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    try:
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            updated_employee = serializer.save()
            return Response({
                'success': True,
                'message': 'Employee updated successfully',
                'data': EmployeeSerializer(updated_employee).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': True,
                'message': 'Validation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        return Response({
            'error': True,
            'message': 'Validation error',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': True,
            'message': 'Failed to update employee',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
