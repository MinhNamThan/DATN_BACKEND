from sqlalchemy.orm import Session
import models, schemas
from hashing import Hash
from fastapi import HTTPException, status

def get_all(db: Session):
  users = db.query(models.User).all()
  return users

def create(request: schemas.User, db: Session):
  new_user =models.User(email=request.email, password=Hash.bcrypt(request.password), phoneNumber=request.phoneNumber, fullName=request.fullName)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def destroy(id: int, db: Session):
  user = db.query(models.User).filter(models.User.id == id)
  if not user.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not available')
  user.delete(synchronize_session=False)
  db.commit()
  return 'done'

def update(id: int, request: schemas.User, db:Session):
  user = db.query(models.User).filter(models.User.id == id)
  if not user.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not available')
  user.update(request.dict())
  db.commit()
  return 'updated'

def show(id: int, db: Session):
  user =db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} is not available')
  return user
