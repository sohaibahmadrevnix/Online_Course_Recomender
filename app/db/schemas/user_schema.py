from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str 
    last_name: str   
    display_name: Optional[str] = None

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    email_verified: bool
    status: Optional[str] = None

    class Config:
       from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordWithTokenRequest(BaseModel):
    email: EmailStr
    token: str  
    new_password: str
