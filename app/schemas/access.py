from pydantic import BaseModel, Field

class RoleCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)

class PermissionCreate(BaseModel):
    resource: str = Field(min_length=2, max_length=50)
    action: str = Field(min_length=2, max_length=20)

class RolePermissionAssign(BaseModel):
    role_id: int
    permission_id: int