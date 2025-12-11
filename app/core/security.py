from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt
import uuid
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_PASSWORD_LENGTH = 72 

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt (truncated to 72 bytes)."""
    if len(password.encode("utf-8")) > MAX_PASSWORD_LENGTH:
        password = password[:MAX_PASSWORD_LENGTH]
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies that a password matches the stored hash."""
    if len(plain_password.encode("utf-8")) > MAX_PASSWORD_LENGTH:
        plain_password = plain_password[:MAX_PASSWORD_LENGTH]
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token for the given subject (usually user_id)."""
    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": str(subject), "iat": now, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """Decode a JWT access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None


def get_subject_from_token(token_payload_sub: str) -> uuid.UUID:
    """Helper to convert subject from token to UUID."""
    return uuid.UUID(token_payload_sub)
