from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_depends import get_async_db
from app.dependencies import require_permission
from app.models.access import Role, Permission, RolePermission
from app.schemas.access import RoleCreate, PermissionCreate, RolePermissionAssign

router = APIRouter(prefix="/admin/access", tags=["admin"])

@router.post("/roles", status_code=status.HTTP_201_CREATED)
async def create_role(
    data: RoleCreate,
    db: AsyncSession = Depends(get_async_db),
    _=Depends(require_permission("access_control", "manage"))
):
    if (await db.scalars(select(Role).where(Role.name == data.name))).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role exists")
    role = Role(name=data.name);
    
    db.add(role)
    await db.commit()
    await db.refresh(role)

    return {"id": role.id, "name": role.name}

@router.post("/permissions", status_code=status.HTTP_201_CREATED)
async def create_perm(
    data: PermissionCreate,
    db: AsyncSession = Depends(get_async_db),
    _=Depends(require_permission("access_control", "manage"))
):
    if (await db.scalars(select(Permission).where(Permission.resource==data.resource,
                                                  Permission.action==data.action))).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission exists")
    
    perm = Permission(resource=data.resource, action=data.action)
    db.add(perm)
    await db.commit()

    return {"id": perm.id, "resource": perm.resource, "action": perm.action}

@router.post("/assign", status_code=status.HTTP_204_NO_CONTENT)
async def assign_role_perm(
    data: RolePermissionAssign,
    db: AsyncSession = Depends(get_async_db),
    _=Depends(require_permission("access_control", "manage"))
):
    db.add(RolePermission(role_id=data.role_id, permission_id=data.permission_id))
    await db.commit()