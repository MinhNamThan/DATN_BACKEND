from fastapi import APIRouter, Depends, status
import schemas, database, oauth2
from sqlalchemy.orm import Session
from repository import box

router = APIRouter(
  prefix="/box",
  tags=["Boxes"]
)
get_db = database.get_db

@router.get('')
def indexWithPlace(place_id: int = 0,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return box.get_all_with_place(db, place_id)

@router.get('/{id}', status_code=200)
def show(id, db: Session = Depends(get_db)):
  return box.show(id, db)

@router.post('', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Box, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return box.create(request, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.BoxUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return box.update(id, request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return box.destroy(id, db)
