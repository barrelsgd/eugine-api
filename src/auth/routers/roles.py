"""
Role management endpoints.

This router handles role CRUD operations. All endpoints require superuser privileges.
"""
from typing import Any

from fastapi import APIRouter, Depends
from sqlmodel import func, select

from src.auth import service
from src.auth.dependencies import get_current_active_superuser
from src.auth.schemas import RoleCreate, RolePublic, RolesPublic
from src.dependencies import SessionDep

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    dependencies=[Depends(get_current_active_superuser)],
)


@router.get(
    "/",
    response_model=RolesPublic,
)
def read_roles(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve roles (superuser only).
    """
    roles = service.get_roles(session=session, skip=skip, limit=limit)
    count_statement = select(func.count()).select_from(service.Role)
    count = session.exec(count_statement).one()
    return RolesPublic(
        data=[RolePublic.model_validate(role) for role in roles], count=count
    )


@router.post(
    "/",
    response_model=RolePublic,
)
def create_role(*, session: SessionDep, role_in: RoleCreate) -> Any:
    """
    Create new role (superuser only).
    """
    role = service.create_role(session=session, role_in=role_in)
    return role

