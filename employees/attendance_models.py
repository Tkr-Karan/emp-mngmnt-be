"""
Attendance Model using MongoEngine
"""
from mongoengine import Document, StringField, ReferenceField, DateField, DateTimeField
from datetime import datetime, date


class Attendance(Document):
    """
    Attendance Model with MongoDB
    Fields: id, employee (reference to Employee), date, status (Present/Absent)
    """
    employee = ReferenceField('Employee', required=True)
    date = DateField(required=True)
    status = StringField(required=True, choices=['Present', 'Absent'], default='Present')
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'attendance',
        'indexes': [
            ('employee', 'date'),  # Composite index for faster lookups
            'date',
            'employee'
        ],
    }
    
    def clean(self):
        """
        Custom validation before saving
        """
        # Validate date is not in the future
        if self.date > date.today():
            raise ValueError("Attendance date cannot be in the future")
    
    def save(self, *args, **kwargs):
        """
        Override save to validate
        """
        self.clean()
        return super(Attendance, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.status}"
