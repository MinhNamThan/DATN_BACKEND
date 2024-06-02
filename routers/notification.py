from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, oauth2
from sqlalchemy.orm import Session
from repository import notification
from twilio.rest import Client

router = APIRouter(
  prefix="/notifications",
  tags=["Notifications"]
)

TWILIO_ACCOUNT_SID='ACe9ccce274c3cfde7896c76a9867f1fa5'
TWILIO_AUTH_TOKEN = '34e034b21eb2f60833b7e87473ab7267'
TWILIO_PHONE_NUMBER = '+14129143633'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
get_db = database.get_db

@router.get('')
def index(camera_id: int = 0,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return notification.get_all(db, camera_id, current_user.id)

@router.get('/unseen')
def indexUnseen(camera_id: int = 0,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return notification.get_all_unseen(db, camera_id, current_user.id)

@router.post('', status_code=status.HTTP_201_CREATED)
async def create(request: schemas.NotificationCreate, db: Session = Depends(get_db)):
  return  await notification.create(request, db)

@router.put('', status_code=status.HTTP_202_ACCEPTED)
def update(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return notification.updateStatus(db, current_user.id)

@router.get('/send-message', status_code=status.HTTP_201_CREATED)
async def send_message():
    try:
        message = client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            body='Sample message',
            to='+84978675796'
        )
        return {"message": "Message sent successfully", "sid": message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
