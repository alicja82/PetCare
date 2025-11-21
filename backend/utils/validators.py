"""
Validation utilities for PetCare application
"""
from datetime import datetime, date
import re

def validate_age(age):
    """
    Validate pet age
    Returns: (is_valid, error_message)
    """
    if age is None:
        return True, None
    
    try:
        age = int(age)
        if age < 0:
            return False, "Age cannot be negative"
        if age > 50:
            return False, "Age seems unrealistic (max 50 years)"
        return True, None
    except (ValueError, TypeError):
        return False, "Age must be a number"

def validate_weight(weight):
    """
    Validate pet weight in kg
    Returns: (is_valid, error_message)
    """
    if weight is None:
        return True, None
    
    try:
        weight = float(weight)
        if weight <= 0:
            return False, "Weight must be positive"
        if weight > 500:
            return False, "Weight seems unrealistic (max 500kg)"
        return True, None
    except (ValueError, TypeError):
        return False, "Weight must be a number"

def validate_email(email):
    """
    Validate email format
    Returns: (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    # Simple email regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, None

def validate_username(username):
    """
    Validate username
    Returns: (is_valid, error_message)
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(username) > 50:
        return False, "Username must be at most 50 characters"
    
    # Allow alphanumeric, underscore, dash
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscore and dash"
    
    return True, None

def validate_password(password):
    """
    Validate password strength
    Returns: (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if len(password) > 100:
        return False, "Password is too long (max 100 characters)"
    
    # Check for uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    # Check for digit
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    # Check for special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/~`]', password):
        return False, "Password must contain at least one special character (!@#$%^&*...)"
    
    return True, None

def validate_date(date_str, field_name="Date"):
    """
    Validate date string (ISO format)
    Returns: (is_valid, parsed_date, error_message)
    """
    if not date_str:
        return False, None, f"{field_name} is required"
    
    try:
        parsed_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return True, parsed_date, None
    except (ValueError, AttributeError):
        return False, None, f"Invalid {field_name} format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"

def validate_future_date(date_obj, field_name="Date"):
    """
    Check if date is not in the future
    Returns: (is_valid, error_message)
    """
    if date_obj and date_obj > datetime.now():
        return False, f"{field_name} cannot be in the future"
    return True, None

def validate_time(time_str):
    """
    Validate time string (HH:MM format)
    Returns: (is_valid, error_message)
    """
    if not time_str:
        return False, "Time is required"
    
    try:
        hour, minute = map(int, time_str.split(':'))
        if hour < 0 or hour > 23:
            return False, "Hour must be between 0 and 23"
        if minute < 0 or minute > 59:
            return False, "Minute must be between 0 and 59"
        return True, None
    except (ValueError, AttributeError):
        return False, "Invalid time format. Use HH:MM"

def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present
    Returns: (is_valid, missing_fields, error_message)
    """
    missing = [field for field in required_fields if not data.get(field)]
    
    if missing:
        return False, missing, f"Missing required fields: {', '.join(missing)}"
    
    return True, [], None

def validate_string_length(value, field_name, min_length=None, max_length=None):
    """
    Validate string length
    Returns: (is_valid, error_message)
    """
    if value is None:
        return True, None
    
    length = len(str(value))
    
    if min_length and length < min_length:
        return False, f"{field_name} must be at least {min_length} characters"
    
    if max_length and length > max_length:
        return False, f"{field_name} must be at most {max_length} characters"
    
    return True, None
