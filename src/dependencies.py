from fastapi import Depends, HTTPException, status
from typing import Annotated

from sqlalchemy.orm import Session
from src.database import  get_db
from src.security import verify_access_token
from src.database import Users
from fastapi.security import OAuth2PasswordBearer

db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="")
token_dependency = Annotated[str, Depends(oauth2_bearer)]

def get_current_user(db: db_dependency, token: token_dependency) -> Users:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials", 
        headers={"www-Authenticate":"Bearer"},
    )
    try:
        payload = verify_access_token(token)
        user_id = payload["id"]
        username = payload["sub"]
        if username is None or user_id is None:
            raise credentials_exception 
    except ValueError as err:
        raise credentials_exception
    
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

current_user_dependency = Annotated[Users, Depends(get_current_user)]

def require_admin(current_user: current_user_dependency) -> Users: # type: ignore
    if current_user.role not in {"admin", "staff-admin"}:
        raise HTTPException(
            detail="Admin access is required",
            status_code=403
        )
    return current_user