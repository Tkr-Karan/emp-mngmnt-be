"""
Employee Model using MongoEngine
"""
from mongoengine import Document, StringField, EmailField
import re


class Employee(Document):
    """
    Employee Model with MongoDB
    Fields: id (MongoDB ObjectId), employeeId (custom ID from UI), full_name, email, department
    """
    # Required fields
    employeeId = StringField(required=True, unique=True, max_length=50)
    full_name = StringField(required=True, max_length=200)
    email = EmailField(required=True, unique=True)
    
    # Optional fields
    department = StringField(max_length=100, required=False)
    
    meta = {
        'collection': 'employees',
        'indexes': ['email', 'employeeId'],  # Index on email and employeeId for faster lookups
    }
    
    def clean(self):
        """
        Custom validation before saving
        """
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValueError("Invalid email format")
    
    def save(self, *args, **kwargs):
        """
        Override save to validate
        """
        self.clean()
        return super(Employee, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"
