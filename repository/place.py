from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status

def get_all(db: Session):
  places = db.query(models.Place).all()
  return places

def create(request: schemas.Place, db: Session, user_id: str):
  new_place =models.Place(name=request.name, description=request.description, user_id=user_id)
  db.add(new_place)
  db.commit()
  db.refresh(new_place)
  return new_place

def destroy(id: int, db: Session):
  place = db.query(models.Place).filter(models.Place.id == id)
  if not place.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'place with id {id} is not available')
  place.delete(synchronize_session=False)
  db.commit()
  return 'done'

def update(id: int, request: schemas.Place, db:Session):
  place = db.query(models.Place).filter(models.Place.id == id)
  if not place.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'place with id {id} is not available')
  place.update(request.dict())
  db.commit()
  return 'updated'

def show(id: int, db: Session, user_id: str):
  place =db.query(models.Place).filter(models.Place.id == id, models.Place.user_id == user_id).first()
  if not place:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'place with id {id} is not available')
  return place
