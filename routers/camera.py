from fastapi import APIRouter, Depends, status
import schemas, database, oauth2
from sqlalchemy.orm import Session
from repository import camera
from typing import List

router = APIRouter(
  prefix="/camera",
  tags=["Cameras"]
)
get_db = database.get_db

@router.get('', response_model=List[schemas.CameraShow])
def indexWithPlace(place_id: int = 0,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return camera.get_all_with_box(db, place_id)

@router.get('/{id}', status_code=200)
def show(id, db: Session = Depends(get_db)):
  return camera.show(id, db)

@router.post('', status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Camera, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return await camera.create(request, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update(id, request: schemas.CameraUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return await camera.update(id, request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return await camera.destroy(id, db)
