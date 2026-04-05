import asyncio
from app.database import async_session
from app.models.users import User
from app.models.access import Role, Permission, RolePermission, UserRole
from app.auth import hash_password

async def seed():
    async with async_session() as db:
        # 1. Роли
        admin_role = Role(name="admin")
        manager_role = Role(name="manager")
        db.add_all([admin_role, manager_role])
        await db.commit()

        # 2. Права
        perms = [
            Permission(resource="reports", action="read"),
            Permission(resource="analytics", action="write"),
            Permission(resource="access_control", action="manage"),
            Permission(resource="users", action="read"),
        ]
        db.add_all(perms)
        await db.commit()

        # 3. Связь прав с ролями
        db.add_all([RolePermission(role_id=admin_role.id, permission_id=p.id) for p in perms])
        db.add_all([RolePermission(role_id=manager_role.id, permission_id=p.id) for p in perms[:2]])
        await db.commit()

        # 4. Тестовые пользователи
        admin_user = User(
            first_name="Super", last_name="Admin", middle_name=None,
            email="admin@test.com", hashed_password=hash_password("admin123"), is_active=True
        )
        manager_user = User(
            first_name="Igor", last_name="Zemskov", middle_name=None,
            email="manager@test.com", hashed_password=hash_password("mgr123"), is_active=True
        )
        db.add_all([admin_user, manager_user])
        await db.commit()

        # 5. Назначение ролей
        db.add_all([
            UserRole(user_id=admin_user.id, role_id=admin_role.id),
            UserRole(user_id=manager_user.id, role_id=manager_role.id)
        ])
        await db.commit()
        print("Seed completed successfully.")

if __name__ == "__main__":
    asyncio.run(seed())