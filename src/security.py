from src.config.settings import settings

from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError

bcrypt_context = CryptContext(schemes=['bcrypt'])

def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(password, hashed_password)

def create_access_token(
    subject: str, 
    user_id: str, 
    role: str,
    expires_delta: timedelta
):  
    if not settings.JWT_ALGO or not settings.JWT_SECRET_KEY:
        raise RuntimeError("JWT_ALGO and JWT_SECRET_KEY are required")
        
    expires_at = datetime.now() + expires_delta
    payload = {
        "sub": subject,
        "id": user_id,
        "role": role,
        "exp": expires_delta
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGO)

def verify_access_token(
    token: str
):
    if not settings.JWT_ALGO or not settings.JWT_SECRET_KEY:
        raise RuntimeError("JWT_ALGO and JWT_SECRET_KEY are required")
    
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGO])
    except JWTError as exc:
        raise ValueError("could not validate credentials") from exc