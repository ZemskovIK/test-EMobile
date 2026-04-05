from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_depends import get_async_db
from app.auth import get_current_user
from app.models.users import User
from app.schemas.auth import ProfileUpdate, ProfileResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/profile", response_model=ProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/profile", response_model=ProfileResponse)
async def update_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update")

    await db.execute(
        update(User)
        .where(User.id == current_user.id)
        .values(**update_data)
    )
    await db.commit()

    result = await db.execute(select(User).where(User.id == current_user.id))
    return result.scalars().first()

@router.delete("/profile", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    await db.execute(
        update(User)
        .where(User.id == current_user.id)
        .values(is_active=False)
    )
    await db.commit()

    return None