from fastapi import Depends, HTTPException, status
import jwt_token
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
get_db = database.get_db

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  return jwt_token.verify_token(token, credentials_exception, db)
