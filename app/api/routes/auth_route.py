from app.db.schemas.user_schema import UserCreate, UserOut, Token , ForgotPasswordRequest , ResetPasswordWithTokenRequest
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.email_utils import send_reset_code_email
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token
from app.core.security import hash_password
from datetime import datetime, timedelta
from app.dep.dependencies import get_db
from app.dep.dependencies import get_current_user
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from app.db.models.user_model import User
import random
import uuid
from app.crud.user_crud import (
    get_user_by_email,
    get_user_by_username,
    create_user,
    authenticate_user,
)

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    user = create_user(
        db,
        email=payload.email,
        username=payload.username,
        password=payload.password,
        first_name=payload.first_name,
        last_name=payload.last_name,  
        display_name = payload.display_name,
    )
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # 🔒 Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        remaining = (user.locked_until - datetime.utcnow()).seconds // 60
        raise HTTPException(
            status_code=403,
            detail=f"Account locked. Try again in {remaining} minutes."
        )

    # ✅ Validate password
    if not authenticate_user(db, form_data.username, form_data.password):
        user.failed_login_attempts += 1

        # Lock account after 3 failed attempts
        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=10)
            user.failed_login_attempts = 0  # reset counter after locking
            db.commit()
            raise HTTPException(
                status_code=403,
                detail="Account locked due to too many failed attempts. Try again in 10 minutes."
            )

        db.commit()
        raise HTTPException(
            status_code=401,
            detail=f"Incorrect password. {5 - user.failed_login_attempts} attempts remaining."
        )

    # ✅ Successful login — reset failed attempts
    user.failed_login_attempts = 0
    user.locked_until = None
    db.commit()

    # Generate token
    access_token = create_access_token(subject=str(user.id))
    expires_min = ACCESS_TOKEN_EXPIRE_MINUTES
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_min * 60
    }


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(payload: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a random 6-digit numeric code
    reset_code = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    user.reset_code = reset_code
    user.reset_code_expires_at = expires_at
    db.commit()

    # Send email asynchronously
    background_tasks.add_task(send_reset_code_email, user.email, reset_code)

    return {"message": "Verification code sent to your email."}

@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(payload: ResetPasswordWithTokenRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify code and expiry
    if user.reset_code != payload.token:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    if user.reset_code_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification code has expired")

    # Reset password
    user.password_hash = hash_password(payload.new_password)
    user.reset_code = None
    user.reset_code_expires_at = None
    user.password_changed_at = datetime.utcnow()
    db.commit()

    return {"message": "Password reset successfully"}
