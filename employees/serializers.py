"""
Serializers for Employee API
"""
from rest_framework import serializers
from .models import Employee
import re


class EmployeeSerializer(serializers.Serializer):
    """
    Serializer for Employee model
    Fields: id (MongoDB ObjectId), employeeId (custom ID from UI), full_name, email, department
    """
    id = serializers.CharField(read_only=True)
    employeeId = serializers.CharField(required=True, max_length=50)
    full_name = serializers.CharField(required=True, max_length=200)
    email = serializers.EmailField(required=True)
    department = serializers.CharField(required=False, max_length=100, allow_blank=True)
    
    def validate_email(self, value):
        """
        Validate email format
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise serializers.ValidationError("Invalid email format")
        return value.lower()  # Store emails in lowercase
    
    def validate_full_name(self, value):
        """
        Validate full name is not empty
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Full name is required")
        return value.strip()
    
    def validate_employeeId(self, value):
        """
        Validate employeeId is not empty
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Employee ID is required")
        return value.strip()
    
    def create(self, validated_data):
        """
        Create and return a new Employee instance
        """
        # Check for duplicate email
        email = validated_data.get('email')
        if Employee.objects(email=email).first():
            raise serializers.ValidationError({
                'email': 'Employee with this email already exists'
            })
        
        # Check for duplicate employeeId
        employee_id = validated_data.get('employeeId')
        if Employee.objects(employeeId=employee_id).first():
            raise serializers.ValidationError({
                'employeeId': 'Employee with this Employee ID already exists'
            })
        
        employee = Employee(**validated_data)
        employee.save()
        return employee
    
    def update(self, instance, validated_data):
        """
        Update and return an existing Employee instance
        """
        # Check for duplicate email if email is being updated
        email = validated_data.get('email', instance.email)
        if email != instance.email:
            # Check if another employee with this email exists (excluding current instance)
            existing_employee = Employee.objects(email=email).first()
            if existing_employee and str(existing_employee.id) != str(instance.id):
                raise serializers.ValidationError({
                    'email': 'Employee with this email already exists'
                })
        
        # Check for duplicate employeeId if employeeId is being updated
        employee_id = validated_data.get('employeeId', instance.employeeId)
        if employee_id != instance.employeeId:
            # Check if another employee with this employeeId exists (excluding current instance)
            existing_employee = Employee.objects(employeeId=employee_id).first()
            if existing_employee and str(existing_employee.id) != str(instance.id):
                raise serializers.ValidationError({
                    'employeeId': 'Employee with this Employee ID already exists'
                })
        
        # Update fields
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
            'employeeId': instance.employeeId,
            'full_name': instance.full_name,
            'email': instance.email,
            'department': instance.department or '',
        }
        return data
