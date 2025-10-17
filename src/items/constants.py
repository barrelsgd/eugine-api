"""
Items module constants.

This module contains all constants used throughout the items module.
"""

# HTTP Status codes
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404

# Error messages
ERROR_ITEM_NOT_FOUND = "Item not found"
ERROR_INSUFFICIENT_PERMISSIONS = "Not enough permissions"

# Success messages
SUCCESS_ITEM_DELETED = "Item deleted successfully"

# Item field constraints
MAX_TITLE_LENGTH = 255
MAX_CONTENT_LENGTH = 10000
MAX_DESCRIPTION_LENGTH = 1000

# Image constraints
MAX_ALT_TEXT_LENGTH = 255
MAX_OBJECT_KEY_LENGTH = 500

# Default pagination values
DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100
