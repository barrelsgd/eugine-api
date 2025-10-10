from typing import Annotated

from fastapi import Depends

from src.dependencies import CurrentUser, get_current_user


def get_current_active_superuser(current_user: CurrentUser) -> "User":
    """Get current active superuser dependency."""
    from fastapi import HTTPException
    
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


CurrentActiveUser = Annotated["User", Depends(get_current_user)]
CurrentSuperUser = Annotated["User", Depends(get_current_active_superuser)]
