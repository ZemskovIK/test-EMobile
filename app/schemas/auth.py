from pydantic import BaseModel, EmailStr, ConfigDict, Field, model_validator

class RegisterRequest(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    middle_name: str | None = Field(None, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    password_confirm: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "RegisterRequest":
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class ProfileUpdate(BaseModel):
    first_name: str | None = Field(None, min_length=2, max_length=50)
    last_name: str | None = Field(None, min_length=2, max_length=50)
    middle_name: str | None = Field(None, max_length=50)

class ProfileResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str | None
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class RefreshRequest(BaseModel):
    refresh_token: str