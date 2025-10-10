"""
Authentication module constants and error codes.
"""

from enum import Enum


class AuthErrorCode(str, Enum):
    """Authentication error codes."""
    
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_INACTIVE = "USER_INACTIVE"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"


class AuthMessage(str, Enum):
    """Authentication messages."""
    
    LOGIN_SUCCESS = "Login successful"
    LOGOUT_SUCCESS = "Logout successful"
    REGISTRATION_SUCCESS = "Registration successful"
    PASSWORD_RESET_SUCCESS = "Password reset successful"
    PROFILE_UPDATE_SUCCESS = "Profile updated successfully"


# Token settings
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"

# Password settings
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

# User settings
MAX_EMAIL_LENGTH = 255
MAX_FULL_NAME_LENGTH = 255
