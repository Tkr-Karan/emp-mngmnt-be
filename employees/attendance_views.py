"""
Views for Attendance API
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mongoengine.errors import DoesNotExist, ValidationError
from bson.errors import InvalidId
from .attendance_models import Attendance
from .attendance_serializers import AttendanceSerializer
from .models import Employee
from datetime import date, datetime


@api_view(['GET', 'POST'])
def attendance_list_create(request):
    """
    List all attendance records or create a new attendance record
    
    GET /api/attendance/ - List all attendance records
    GET /api/attendance/?employeeId=EMP001 - Filter by employee ID
    GET /api/attendance/?date=2024-01-15 - Filter by date
    POST /api/attendance/ - Mark attendance for an employee
    """
    if request.method == 'GET':
        try:
            # Get query parameters
            employee_id = request.query_params.get('employeeId', None)
            attendance_date = request.query_params.get('date', None)
            
            # Start with all attendance records
            attendance_records = Attendance.objects.all()
            
            # Filter by employeeId if provided
            if employee_id:
                employee = Employee.objects(employeeId=employee_id).first()
                if not employee:
                    return Response({
                        'error': True,
                        'message': 'Employee not found',
                        'details': f'No employee found with ID: {employee_id}'
                    }, status=status.HTTP_404_NOT_FOUND)
                attendance_records = attendance_records.filter(employee=employee)
            
            # Filter by date if provided
            if attendance_date:
                try:
                    date_obj = datetime.strptime(attendance_date, '%Y-%m-%d').date()
                    attendance_records = attendance_records.filter(date=date_obj)
                except ValueError:
                    return Response({
                        'error': True,
                        'message': 'Invalid date format',
                        'details': 'Date must be in YYYY-MM-DD format'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Order by date (newest first)
            attendance_records = attendance_records.order_by('-date', '-created_at')
            
            serializer = AttendanceSerializer(attendance_records, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'count': len(serializer.data)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': True,
                'message': 'Failed to retrieve attendance records',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
            serializer = AttendanceSerializer(data=request.data)
            if serializer.is_valid():
                attendance = serializer.save()
                return Response({
                    'success': True,
                    'message': 'Attendance marked successfully',
                    'data': AttendanceSerializer(attendance).data
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
                'message': 'Failed to mark attendance',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def attendance_detail(request, attendance_id):
    """
    Retrieve, update or delete an attendance record
    
    GET /api/attendance/<id>/ - Get attendance details
    PUT /api/attendance/<id>/ - Update attendance
    DELETE /api/attendance/<id>/ - Delete attendance
    """
    try:
        attendance = Attendance.objects.get(id=attendance_id)
    except (DoesNotExist, Attendance.DoesNotExist):
        return Response({
            'error': True,
            'message': 'Attendance record not found',
            'details': f'No attendance record found with id: {attendance_id}'
        }, status=status.HTTP_404_NOT_FOUND)
    except (InvalidId, ValueError) as e:
        return Response({
            'error': True,
            'message': 'Invalid attendance ID',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': True,
            'message': 'Error retrieving attendance',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if request.method == 'GET':
        try:
            serializer = AttendanceSerializer(attendance)
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': True,
                'message': 'Failed to retrieve attendance',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PUT':
        try:
            serializer = AttendanceSerializer(attendance, data=request.data, partial=False)
            if serializer.is_valid():
                updated_attendance = serializer.save()
                return Response({
                    'success': True,
                    'message': 'Attendance updated successfully',
                    'data': AttendanceSerializer(updated_attendance).data
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
                'message': 'Failed to update attendance',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'DELETE':
        try:
            attendance.delete()
            return Response({
                'success': True,
                'message': 'Attendance record deleted successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': True,
                'message': 'Failed to delete attendance',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def employee_attendance(request, employee_id):
    """
    Get all attendance records for a specific employee
    
    GET /api/employees/<employeeId>/attendance/ - Get attendance for employee
    GET /api/employees/<employeeId>/attendance/?start_date=2024-01-01&end_date=2024-01-31 - Filter by date range
    """
    try:
        # Find employee by employeeId
        employee = Employee.objects(employeeId=employee_id).first()
        if not employee:
            return Response({
                'error': True,
                'message': 'Employee not found',
                'details': f'No employee found with ID: {employee_id}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get attendance records for this employee
        attendance_records = Attendance.objects(employee=employee)
        
        # Filter by date range if provided
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                attendance_records = attendance_records.filter(date__gte=start_date_obj)
            except ValueError:
                return Response({
                    'error': True,
                    'message': 'Invalid start_date format',
                    'details': 'Date must be in YYYY-MM-DD format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                attendance_records = attendance_records.filter(date__lte=end_date_obj)
            except ValueError:
                return Response({
                    'error': True,
                    'message': 'Invalid end_date format',
                    'details': 'Date must be in YYYY-MM-DD format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Order by date (newest first)
        attendance_records = attendance_records.order_by('-date', '-created_at')
        
        serializer = AttendanceSerializer(attendance_records, many=True)
        
        # Calculate statistics
        total_records = len(serializer.data)
        present_count = sum(1 for record in serializer.data if record.get('status') == 'Present')
        absent_count = sum(1 for record in serializer.data if record.get('status') == 'Absent')
        
        return Response({
            'success': True,
            'employee': {
                'id': str(employee.id),
                'employeeId': employee.employeeId,
                'full_name': employee.full_name,
                'email': employee.email,
                'department': employee.department or ''
            },
            'data': serializer.data,
            'count': total_records,
            'statistics': {
                'total': total_records,
                'present': present_count,
                'absent': absent_count
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': True,
            'message': 'Failed to retrieve employee attendance',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
