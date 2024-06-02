from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from routers.websocket import manager
from datetime import datetime

def get_all(db: Session, camera_id: int, user_id: int):
  if(int(camera_id) < 1 ):
    notifications = db.query(models.Notification).filter(models.Notification.user_id == user_id).all()
  else:
    notifications = db.query(models.Notification).filter(models.Notification.user_id == user_id, models.Notification.camera_id == camera_id).all()
  return notifications

def get_all_unseen(db: Session, camera_id: int, user_id: int):
  if(int(camera_id) < 1 ):
    notifications = db.query(models.Notification).filter(models.Notification.user_id == user_id, models.Notification.status == "unseen").all()
  else:
    notifications = db.query(models.Notification).filter(models.Notification.user_id == user_id, models.Notification.camera_id == camera_id, models.Notification.status == "unseen").all()
  return len(notifications)

async def create(request: schemas.NotificationCreate, db: Session):
  new_notification =models.Notification(title=request.title, description=request.description, videoUrl=request.videoUrl, status="unseen",created_at = datetime.now(), camera_id = request.camera_id, user_id = request.user_id)
  db.add(new_notification)
  db.commit()
  db.refresh(new_notification)
  await manager.broadcast("new notification")
  return new_notification

def updateStatus(db:Session, user_id: int):
  db.query(models.Notification).filter(models.Notification.user_id == user_id, models.Notification.status == "unseen").update({models.Notification.status: "seen"})
  # if not notification:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'notification with id {id} is not available')
  # notification.update({models.Notification.status: "seen"})
  db.commit()
  return 'updated'
