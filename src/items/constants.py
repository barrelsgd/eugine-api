"""
Items module constants and error codes.
"""

from enum import Enum


class ItemErrorCode(str, Enum):
    """Item error codes."""
    
    ITEM_NOT_FOUND = "ITEM_NOT_FOUND"
    ITEM_ALREADY_EXISTS = "ITEM_ALREADY_EXISTS"
    INVALID_ITEM_DATA = "INVALID_ITEM_DATA"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    ITEM_LIMIT_EXCEEDED = "ITEM_LIMIT_EXCEEDED"


class ItemMessage(str, Enum):
    """Item messages."""
    
    ITEM_CREATED = "Item created successfully"
    ITEM_UPDATED = "Item updated successfully"
    ITEM_DELETED = "Item deleted successfully"
    ITEMS_RETRIEVED = "Items retrieved successfully"


# Item settings
MAX_TITLE_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 1000
MIN_TITLE_LENGTH = 1

# Pagination settings
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
