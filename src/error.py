"""
Stores error classes
"""
from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    """
    AccessError information
    """
    code = 400
    message = "No message specified"

class InputError(HTTPException):
    """
    InputError information
    """
    code = 400
    message = "No message specified"
    
