from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, oauth2
from sqlalchemy.orm import Session
from repository import notification
from fastapi_pagination import Page
from datetime import datetime

router = APIRouter(
  prefix="/notifications",
  tags=["Notifications"]
)
get_db = database.get_db

@router.get('', response_model=Page[schemas.Notification])
def index(start_date: datetime = None, end_date: datetime = None, camera_id: int = 0, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return notification.get_all(start_date, end_date, db, camera_id, current_user.id)

@router.get('/unseen')
def indexUnseen(camera_id: int = 0,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return notification.get_all_unseen(db, camera_id, current_user.id)

@router.post('', status_code=status.HTTP_201_CREATED)
async def create(request: schemas.NotificationCreate, db: Session = Depends(get_db)):
  return  await notification.create(request, db)

@router.put('', status_code=status.HTTP_202_ACCEPTED)
def update(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return notification.updateStatus(db, current_user.id)

@router.get('/{id}', status_code=200, response_model=schemas.NotificationShow)
def show(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return notification.show(id, db, current_user.id)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return notification.destroy(id, db)
