"""
Serializers for Attendance API
"""
from rest_framework import serializers
from .attendance_models import Attendance
from .models import Employee
from datetime import date


class AttendanceSerializer(serializers.Serializer):
    """
    Serializer for Attendance model
    """
    id = serializers.CharField(read_only=True)
    employeeId = serializers.CharField(required=True, write_only=True)  # For input
    employee = serializers.SerializerMethodField(read_only=True)  # For output
    date = serializers.DateField(required=True)
    status = serializers.ChoiceField(choices=['Present', 'Absent'], required=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def get_employee(self, obj):
        """Get employee details"""
        if obj.employee:
            return {
                'id': str(obj.employee.id),
                'employeeId': obj.employee.employeeId,
                'full_name': obj.employee.full_name,
                'email': obj.employee.email,
                'department': obj.employee.department or ''
            }
        return None
    
    def validate_date(self, value):
        """
        Validate date is not in the future
        """
        if value > date.today():
            raise serializers.ValidationError("Attendance date cannot be in the future")
        return value
    
    def validate_employeeId(self, value):
        """
        Validate employeeId exists
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Employee ID is required")
        
        employee = Employee.objects(employeeId=value.strip()).first()
        if not employee:
            raise serializers.ValidationError(f"Employee with ID '{value}' not found")
        
        return value.strip()
    
    def validate(self, data):
        """
        Validate that same employee cannot have duplicate attendance for same date
        """
        employee_id = data.get('employeeId')
        attendance_date = data.get('date')
        
        if employee_id and attendance_date:
            employee = Employee.objects(employeeId=employee_id).first()
            if employee:
                # Check if attendance already exists for this employee and date
                existing_attendance = Attendance.objects(
                    employee=employee,
                    date=attendance_date
                ).first()
                
                # If updating, exclude current instance
                if self.instance:
                    if existing_attendance and str(existing_attendance.id) != str(self.instance.id):
                        raise serializers.ValidationError({
                            'date': f'Attendance for this employee on {attendance_date} already exists'
                        })
                else:
                    # Creating new attendance - prevent duplicate
                    if existing_attendance:
                        raise serializers.ValidationError({
                            'date': f'Attendance for this employee on {attendance_date} already exists.'
                        })
        
        return data
    
    def create(self, validated_data):
        """
        Create and return a new Attendance instance
        """
        employee_id = validated_data.pop('employeeId')
        employee = Employee.objects(employeeId=employee_id).first()
        
        if not employee:
            raise serializers.ValidationError({
                'employeeId': 'Employee not found'
            })
        
        attendance = Attendance(
            employee=employee,
            date=validated_data.get('date'),
            status=validated_data.get('status')
        )
        attendance.save()
        return attendance
    
    def update(self, instance, validated_data):
        """
        Update and return an existing Attendance instance
        """
        # Update employee if employeeId is provided
        if 'employeeId' in validated_data:
            employee_id = validated_data.pop('employeeId')
            employee = Employee.objects(employeeId=employee_id).first()
            if not employee:
                raise serializers.ValidationError({
                    'employeeId': 'Employee not found'
                })
            instance.employee = employee
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """
        Convert MongoDB ObjectId to string
        """
        data = {
            'id': str(instance.id),
            'employee': self.get_employee(instance),
            'date': instance.date.isoformat() if instance.date else None,
            'status': instance.status,
            'created_at': instance.created_at.isoformat() if instance.created_at else None,
        }
        return data
