from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from routers.websocket import manager
from datetime import datetime
from twilio.rest import Client
from fastapi_pagination import paginate
from sqlalchemy import asc, desc

TWILIO_ACCOUNT_SID='ACe9ccce274c3cfde7896c76a9867f1fa5'
TWILIO_AUTH_TOKEN = '01ae2e6a47c884ad6ac2c8169a06f1ef'
TWILIO_PHONE_NUMBER = '+14129143633'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

async def send_message(owner_phone: str, camera_name: str):
    try:
        message = client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            body='Phát hiện người từ camera tên ' + camera_name + ', vui lòng kiểm tra ngay!',
            to=owner_phone
        )
        return {"message": "Message sent successfully", "sid": message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_all(start_date, end_date, db: Session, camera_id: int, user_id: int):
  if(int(camera_id) < 1 ):
    queryNoti = db.query(models.Notification).filter(models.Notification.user_id == user_id).order_by(desc(models.Notification.created_at))
  else:
    queryNoti = db.query(models.Notification).filter(models.Notification.user_id == user_id, models.Notification.camera_id == camera_id).order_by(desc(models.Notification.created_at))
  if start_date:
    print(start_date)
    queryNoti = queryNoti.filter(models.Notification.created_at >= start_date)
  if end_date:
    print(end_date)
    queryNoti = queryNoti.filter(models.Notification.created_at <= end_date)
  notifications = queryNoti.all()
  return paginate(notifications)

def get_all_unseen(db: Session, camera_id: int, user_id: int):
  if(int(camera_id) < 1 ):
    notifications = db.query(models.Notification).filter(models.Notification.user_id == user_id, models.Notification.status == "unseen").all()
  else:
    notifications = db.query(models.Notification).filter(models.Notification.user_id == user_id, models.Notification.camera_id == camera_id, models.Notification.status == "unseen").all()
  return len(notifications)

async def create(request: schemas.NotificationCreate, db: Session):
  new_notification =models.Notification(title=request.title, description=request.description, videoUrl=request.videoUrl, status="unseen",created_at = datetime.now(), camera_id = request.camera_id, user_id = request.user_id)
  user = db.query(models.User).filter(models.User.id == request.user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {request.user_id} is not available')
  camera = db.query(models.Camera).filter(models.Camera.id == request.camera_id).first()
  if not camera:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {request.camera_id} is not available')
  db.add(new_notification)
  db.commit()
  db.refresh(new_notification)
  await manager.broadcast("new notification")
  await send_message(user.phoneNumber, camera.name)
  return new_notification

def updateStatus(db:Session, user_id: int):
  db.query(models.Notification).filter(models.Notification.user_id == user_id, models.Notification.status == "unseen").update({models.Notification.status: "seen"})
  # if not notification:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'notification with id {id} is not available')
  # notification.update({models.Notification.status: "seen"})
  db.commit()
  return 'updated'

def show(id: int, db: Session, user_id: str):
  notification =db.query(models.Notification).filter(models.Notification.id == id, models.Notification.user_id == user_id).first()
  if not notification:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'notification with id {id} is not available')
  return notification

def destroy(id: int, db: Session):
  notification = db.query(models.Notification).filter(models.Notification.id == id)
  if not notification.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'notification with id {id} is not available')
  notification.delete(synchronize_session=False)
  db.commit()
  return 'done'
