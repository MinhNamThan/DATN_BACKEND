from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from hashing import Hash
from repository import user

router = APIRouter(
  prefix="/user",
  tags=["Users"]
)
get_db = database.get_db

@router.get('/')
def index(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  print(current_user.id)
  return user.get_all(db)

@router.get('/{id}', status_code=200)
def show(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return user.show(id, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.User, db: Session = Depends(get_db)):
  return user.create(request, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return user.update(id, request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return user.destroy(id, db)
