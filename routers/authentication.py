from fastapi import APIRouter, Depends, HTTPException, status
import schemas, database, models, jwt_token
from sqlalchemy.orm import Session
from hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
  tags=['Authentication']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  user = db.query(models.User).filter(models.User.email == request.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found user")
  if not Hash.verify(request.password, user.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not correct")

  access_token = jwt_token.create_access_token(
    data={"sub": user.email, "user_id": user.id}
  )
  return {"access_token": access_token, "token_type":"bearer"}
