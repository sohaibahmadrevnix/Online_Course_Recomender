from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import uuid

from app.db.models.user_model import User
from app.core.security import hash_password, verify_password

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user(db: Session, user_id: uuid.UUID) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, *, email: str, username: str,first_name:str ,last_name:str , password: str, **extras) -> User:
    hashed = hash_password(password)
    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        username=username,
        password_hash=hashed,
        created_at=datetime.utcnow(),
        **extras
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username_or_email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, username_or_email) or get_user_by_username(db, username_or_email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        # increment failed attempts optionally
        user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
        db.add(user)
        db.commit()
        return None
    # reset failed attempts, update login info
    user.failed_login_attempts = 0
    user.last_login_at = datetime.utcnow()
    user.login_count = (user.login_count or 0) + 1
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
