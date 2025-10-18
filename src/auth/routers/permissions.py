"""
Permission management endpoints.

This router handles permission CRUD operations. All endpoints require superuser privileges.
"""

from typing import Any

from fastapi import APIRouter, Depends
from sqlmodel import func, select

from src.auth import service
from src.auth.dependencies import get_current_active_superuser
from src.auth.schemas import PermissionCreate, PermissionPublic, PermissionsPublic
from src.dependencies import SessionDep

router = APIRouter(
    prefix="/permissions",
    tags=["permissions"],
    dependencies=[Depends(get_current_active_superuser)],
)


@router.get(
    "/",
    response_model=PermissionsPublic,
)
def read_permissions(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve permissions (superuser only).
    """
    permissions = service.get_permissions(session=session, skip=skip, limit=limit)
    count_statement = select(func.count()).select_from(service.Permission)
    count = session.exec(count_statement).one()
    return PermissionsPublic(
        data=[PermissionPublic.model_validate(perm) for perm in permissions],
        count=count,
    )


@router.post(
    "/",
    response_model=PermissionPublic,
)
def create_permission(*, session: SessionDep, permission_in: PermissionCreate) -> Any:
    """
    Create new permission (superuser only).
    """
    permission = service.create_permission(session=session, permission_in=permission_in)
    return permission
