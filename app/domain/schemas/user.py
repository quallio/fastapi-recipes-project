from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict

class UserRole(str, Enum):
    user = "user"
    admin = "admin"
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.user   # opctional, default a "user"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: UserRole   # 'user' o 'admin'

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
