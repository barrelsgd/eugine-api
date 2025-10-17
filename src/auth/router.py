import uuid
from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import col, delete, func, select

from src.config import settings
from src.dependencies import CurrentUser, SessionDep
from src.email import (
    generate_new_account_email,
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)
from src.items.models import Item
from src.models import Message, Token

from . import service
from .constants import (
    ERROR_INACTIVE_USER,
    ERROR_INCORRECT_CREDENTIALS,
    ERROR_INSUFFICIENT_PRIVILEGES,
    ERROR_INVALID_TOKEN,
    ERROR_PASSWORD_INCORRECT,
    ERROR_PASSWORD_SAME,
    ERROR_SUPERUSER_DELETE_SELF,
    ERROR_USER_EXISTS,
    ERROR_USER_NOT_FOUND,
    SUCCESS_PASSWORD_UPDATED,
    SUCCESS_PASSWORD_RECOVERY_SENT,
    SUCCESS_USER_DELETED,
)
from .dependencies import get_current_active_superuser
from .models import User
from .schemas import (
    NewPassword,
    PermissionCreate,
    PermissionPublic,
    PermissionsPublic,
    RoleCreate,
    RolePublic,
    RolesPublic,
    UpdatePassword,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from .utils import create_access_token, get_password_hash, verify_password

router = APIRouter()


# Authentication routes
@router.post(
    "/login/access-token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login with OAuth2",
    description="OAuth2 compatible token login. Returns an access token for future requests.",
    tags=["login"],
    responses={
        status.HTTP_200_OK: {
            "description": "Login successful, access token returned",
            "model": Token,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Incorrect email/password or inactive user",
        },
    },
)
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = service.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail=ERROR_INCORRECT_CREDENTIALS)
    elif not user.is_active:
        raise HTTPException(status_code=400, detail=ERROR_INACTIVE_USER)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(user.id, expires_delta=access_token_expires)
    )


@router.post("/login/test-token", response_model=UserPublic, tags=["login"])
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", tags=["login"])
def recover_password(email: str, session: SessionDep) -> Message:
    """
    Password Recovery
    """
    user = service.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=ERROR_USER_NOT_FOUND,
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message=SUCCESS_PASSWORD_RECOVERY_SENT)


@router.post("/reset-password/", tags=["login"])
def reset_password(session: SessionDep, body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail=ERROR_INVALID_TOKEN)
    user = service.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=ERROR_USER_NOT_FOUND,
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail=ERROR_INACTIVE_USER)
    hashed_password = get_password_hash(password=body.new_password)
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()
    return Message(message=SUCCESS_PASSWORD_UPDATED)


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
    tags=["login"],
)
def recover_password_html_content(email: str, session: SessionDep) -> Any:
    """
    HTML Content for Password Recovery
    """
    user = service.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )


# User management routes
@router.get(
    "/users/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
    tags=["users"],
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return UsersPublic(
        data=[UserPublic.model_validate(user) for user in users], count=count
    )


@router.post(
    "/users/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
    tags=["users"],
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = service.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail=ERROR_USER_EXISTS,
        )

    user = service.create_user(session=session, user_create=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user


@router.patch("/users/me", response_model=UserPublic, tags=["users"])
def update_user_me(
    *, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> Any:
    """
    Update own user.
    """
    if user_in.email:
        existing_user = service.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail=ERROR_USER_EXISTS
            )
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.patch("/users/me/password", response_model=Message, tags=["users"])
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    """
    Update own password.
    """
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail=ERROR_PASSWORD_INCORRECT)
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail=ERROR_PASSWORD_SAME
        )
    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()
    return Message(message=SUCCESS_PASSWORD_UPDATED)


@router.get("/users/me", response_model=UserPublic, tags=["users"])
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.delete("/users/me", response_model=Message, tags=["users"])
def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Delete own user.
    """
    if current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail=ERROR_SUPERUSER_DELETE_SELF
        )
    session.delete(current_user)
    session.commit()
    return Message(message=SUCCESS_USER_DELETED)


@router.post(
    "/users/signup",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account without authentication. Public endpoint for user registration.",
    tags=["users"],
    responses={
        status.HTTP_201_CREATED: {
            "description": "User registered successfully",
            "model": UserPublic,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "User with this email already exists",
        },
    },
)
def register_user(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = service.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail=ERROR_USER_EXISTS,
        )
    user_create = UserCreate.model_validate(user_in)
    user = service.create_user(session=session, user_create=user_create)
    return user


@router.get("/users/{user_id}", response_model=UserPublic, tags=["users"])
def read_user_by_id(
    user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get a specific user by id.
    """
    user = session.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail=ERROR_INSUFFICIENT_PRIVILEGES,
        )
    return user


@router.patch(
    "/users/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
    tags=["users"],
)
def update_user(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = service.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail=ERROR_USER_EXISTS
            )

    db_user = service.update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user


@router.delete(
    "/users/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    tags=["users"],
)
def delete_user(
    session: SessionDep, current_user: CurrentUser, user_id: uuid.UUID
) -> Message:
    """
    Delete a user.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=ERROR_USER_NOT_FOUND)
    if user == current_user:
        raise HTTPException(
            status_code=403, detail=ERROR_SUPERUSER_DELETE_SELF
        )
    statement = delete(Item).where(col(Item.owner_id) == user_id)
    session.exec(statement)
    session.delete(user)
    session.commit()
    return Message(message=SUCCESS_USER_DELETED)


# Role management routes
@router.get(
    "/roles/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RolesPublic,
    tags=["roles"],
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
    "/roles/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=RolePublic,
    tags=["roles"],
)
def create_role(*, session: SessionDep, role_in: RoleCreate) -> Any:
    """
    Create new role (superuser only).
    """
    role = service.create_role(session=session, role_in=role_in)
    return role


# Permission management routes
@router.get(
    "/permissions/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=PermissionsPublic,
    tags=["permissions"],
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
    "/permissions/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=PermissionPublic,
    tags=["permissions"],
)
def create_permission(*, session: SessionDep, permission_in: PermissionCreate) -> Any:
    """
    Create new permission (superuser only).
    """
    permission = service.create_permission(session=session, permission_in=permission_in)
    return permission
