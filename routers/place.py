from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, oauth2
from sqlalchemy.orm import Session
from repository import place
import httpx

router = APIRouter(
  prefix="/place",
  tags=["Places"]
)
get_db = database.get_db

# async def get_no_stream():
#     async with httpx.AsyncClient() as client:
#       try:
#           await client.get(('http://0.0.0.0:8001/stop-streaming'))
#       except httpx.HTTPStatusError as exc:
#           raise HTTPException(status_code=exc.response.status_code, detail=f"Error calling external API: {exc.response.text}")
#       except Exception as exc:
#           raise HTTPException(status_code=500, detail=f"Internal server error: {str(exc)}")

@router.get('/')
async def index(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  # await get_no_stream()
  return place.get_all(db)

@router.get('/{id}', status_code=200)
def show(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return place.show(id, db, current_user.id)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Place, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return place.create(request, db, current_user.id)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Place, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return place.update(id, request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  return place.destroy(id, db)
