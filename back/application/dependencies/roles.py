from fastapi import Depends, HTTPException
from application.dependencies.auth import get_current_user


def require_role(*roles: str):
    """Dependency factory: raises 403 if current user's role is not in the allowed list."""
    def checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            allowed = ", ".join(roles)
            raise HTTPException(
                status_code=403,
                detail=f"Доступ только для: {allowed}",
            )
        return current_user
    return checker


def require_boss_or_admin(current_user=Depends(get_current_user)):
    if current_user.role not in ("boss", "admin"):
        raise HTTPException(status_code=403, detail="Доступ только для boss или admin")
    return current_user


def require_employee(current_user=Depends(get_current_user)):
    if current_user.role not in ("employee", "admin"):
        raise HTTPException(status_code=403, detail="Доступ только для employee")
    return current_user


def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Доступ только для admin")
    return current_user
