"""
error(error.py): Gives access to error classes
"""
from error import InputError

def echo(value):
    """
    Prints input
    """
    if value == 'echo':
        raise InputError('Input cannot be echo')
    return value
