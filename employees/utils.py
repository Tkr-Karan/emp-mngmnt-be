"""
Utility functions for error handling
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler for better error messages
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Customize the response
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': 'An error occurred',
            'details': response.data
        }
        
        # Handle validation errors
        if isinstance(response.data, dict):
            error_messages = []
            for field, errors in response.data.items():
                if isinstance(errors, list):
                    error_messages.append(f"{field}: {', '.join(str(e) for e in errors)}")
                else:
                    error_messages.append(f"{field}: {str(errors)}")
            
            if error_messages:
                custom_response_data['message'] = 'Validation error'
                custom_response_data['details'] = '; '.join(error_messages)
        
        response.data = custom_response_data
    
    # Handle other exceptions
    else:
        custom_response_data = {
            'error': True,
            'message': str(exc) if exc else 'An unexpected error occurred',
            'details': None
        }
        response = Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
