from datetime import datetime, timedelta, timezone
from typing import Union
from jose import JWTError, jwt
import schemas
import models
from sqlalchemy.orm import Session

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception, db: Session):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    id: str = payload.get("user_id")
    if email is None:
        raise credentials_exception
    token_data = schemas.TokenData(email=email)
    user = db.query(models.User).filter(models.User.id == id, models.User.email == email).first()
    if(user):
      return user
  except JWTError:
    raise credentials_exception
