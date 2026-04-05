from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_depends import get_async_db
from app.auth import get_current_user
from app.models.users import User
from app.models.access import Permission, RolePermission, UserRole

def require_permission(resource: str, action: str):
    async def check_permission(
        db: AsyncSession = Depends(get_async_db),
        current_user: User = Depends(get_current_user)
    ) -> User:
        stmt = (
            select(Permission.id)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .join(UserRole, RolePermission.role_id == UserRole.role_id)
            .where(
                UserRole.user_id == current_user.id,
                Permission.resource == resource,
                Permission.action == action
            )
        )
        result = (await db.scalars(stmt)).first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: insufficient permissions"
            )
        return current_user
    return check_permission