"""
Items-specific exceptions.
"""

from src.exceptions import AppException, NotFoundError, AuthorizationError
from src.items.constants import ItemErrorCode


class ItemNotFoundError(NotFoundError):
    """Item not found exception."""
    
    def __init__(self):
        super().__init__("Item not found")
        self.error_code = ItemErrorCode.ITEM_NOT_FOUND


class ItemAlreadyExistsError(AppException):
    """Item already exists exception."""
    
    def __init__(self):
        super().__init__("Item with this title already exists", 409)
        self.error_code = ItemErrorCode.ITEM_ALREADY_EXISTS


class InvalidItemDataError(AppException):
    """Invalid item data exception."""
    
    def __init__(self, message: str = "Invalid item data"):
        super().__init__(message, 422)
        self.error_code = ItemErrorCode.INVALID_ITEM_DATA


class UnauthorizedItemAccessError(AuthorizationError):
    """Unauthorized item access exception."""
    
    def __init__(self):
        super().__init__("You don't have permission to access this item")
        self.error_code = ItemErrorCode.UNAUTHORIZED_ACCESS


class ItemLimitExceededError(AppException):
    """Item limit exceeded exception."""
    
    def __init__(self):
        super().__init__("Maximum number of items exceeded", 429)
        self.error_code = ItemErrorCode.ITEM_LIMIT_EXCEEDED
