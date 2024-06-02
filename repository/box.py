from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
import ffmpegcv
import cv2
import time

def get_all(db: Session):
  boxes = db.query(models.Box).all()
  return boxes

def get_all_with_place(db: Session, place_id: int):
  if(int(place_id) < 1 ):
    boxes = db.query(models.Box).all()
  else:
    boxes = db.query(models.Box).filter(models.Box.place_id == place_id).all()
  return boxes

def create(request: schemas.Box, db: Session):
  new_box =models.Box(name=request.name, username=request.username, link= request.link, password=request.password, place_id=request.place_id)
  db.add(new_box)
  db.commit()
  db.refresh(new_box)
  return new_box

def destroy(id: int, db: Session):
  box = db.query(models.Box).filter(models.Box.id == id)
  if not box.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'box with id {id} is not available')
  box.delete(synchronize_session=False)
  db.commit()
  return 'done'

def update(id: int, request: schemas.BoxUpdate, db:Session):
  box = db.query(models.Box).filter(models.Box.id == id)
  if not box.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'box with id {id} is not available')
  box.update(request.dict())
  db.commit()
  return 'updated'

def show(id: int, db: Session):
  box =db.query(models.Box).filter(models.Box.id == id).first()
  if not box:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'box with id {id} is not available')
  return box
