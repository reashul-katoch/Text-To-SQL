from fastapi import HTTPException


ROLE_PERMISSIONS = {
    "admin": {"SELECT", "INSERT", "UPDATE", "DELETE"},
    "analyst": {"SELECT"},
    "viewer": {"SELECT"},
}


def check_permission(role: str, operation: str):
    operation = operation.upper()

    allowed_operations = ROLE_PERMISSIONS.get(role, set())

    if operation not in allowed_operations:
        raise HTTPException(
            status_code=403,
            detail=f"Role '{role}' does not have permission for {operation}"
        )

    return True