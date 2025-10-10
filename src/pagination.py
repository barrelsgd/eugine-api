from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model."""
    data: list[T]
    count: int
    page: int = 1
    size: int = 100
    total_pages: int = 1

    def __init__(self, data: list[T], count: int, page: int = 1, size: int = 100, **kwargs):
        total_pages = (count + size - 1) // size if count > 0 else 1
        super().__init__(
            data=data,
            count=count,
            page=page,
            size=size,
            total_pages=total_pages,
            **kwargs
        )


class PaginationParams(BaseModel):
    """Pagination parameters for API endpoints."""
    page: int = 1
    size: int = 100

    @property
    def skip(self) -> int:
        """Calculate skip value for database queries."""
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        """Get limit value for database queries."""
        return self.size
