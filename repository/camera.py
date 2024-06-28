from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
import httpx

def get_all(db: Session):
  cameras = db.query(models.Camera).all()
  return cameras

def get_all_with_box(db: Session, box_id: int):
  if(int(box_id) < 1 ):
    cameras = db.query(models.Camera).all()
  else:
    cameras = db.query(models.Camera).filter(models.Camera.box_id == box_id).all()
  return cameras

async def create_camera_at_box(camera: schemas.CameraBox, boxUrl: str, user_id: int):
    async with httpx.AsyncClient() as client:
      try:
          response = await client.post((boxUrl + 'camera'), json=camera.dict())
          response.raise_for_status()  # Raise an exception for 4xx/5xx responses
          data = response.json()  # Parse the JSON response
          return data
      except httpx.HTTPStatusError as exc:
          raise HTTPException(status_code=exc.response.status_code, detail=f"Error calling external API: {exc.response.text}")
      except Exception as exc:
          raise HTTPException(status_code=500, detail=f"Internal server error: {str(exc)}")

async def update_camera_at_box(camera: schemas.CameraBox, id, boxUrl: str, user_id: int):
    async with httpx.AsyncClient() as client:
      try:
          print("update")
          print(camera.dict())
          response = await client.put((boxUrl + 'camera/' + str(id)), json=camera.dict())
          response.raise_for_status()  # Raise an exception for 4xx/5xx responses
          data = response.json()  # Parse the JSON response
          return data
      except httpx.HTTPStatusError as exc:
          raise HTTPException(status_code=exc.response.status_code, detail=f"Error calling external API: {exc.response.text}")
      except Exception as exc:
          raise HTTPException(status_code=500, detail=f"Internal server error: {str(exc)}")

async def delete_camera_at_box(id: int, boxUrl: str):
    async with httpx.AsyncClient() as client:
      try:
          await client.delete((boxUrl + 'camera/' + str(id)))
      except httpx.HTTPStatusError as exc:
          raise HTTPException(status_code=exc.response.status_code, detail=f"Error calling external API: {exc.response.text}")
      except Exception as exc:
          raise HTTPException(status_code=500, detail=f"Internal server error: {str(exc)}")

async def create(request: schemas.Camera, db: Session):
  new_camera =  models.Camera(name=request.name, url=request.url, box_id=request.box_id, detected=request.detected, points=request.points)
  box =  db.query(models.Box).filter(models.Box.id == request.box_id).first()
  if not box:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'box with id {id} is not available')
  try:
    db.add(new_camera)
    db.commit()
    db.refresh(new_camera)
    await create_camera_at_box(
        schemas.CameraBox(
            camera_id=new_camera.id,
            user_id=box.place.user_id,
            name=new_camera.name,
            url=new_camera.url,
            points=new_camera.points,
            detected=new_camera.detected
        ),
        box.link,
        box.place.user_id
      )
    return new_camera
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'bad request')

async def destroy(id: int, db: Session):
  camera = db.query(models.Camera).filter(models.Camera.id == id)
  if not camera.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'camera with id {id} is not available')
  await delete_camera_at_box(id, camera.first().box.link)
  camera.delete(synchronize_session=False)
  db.commit()
  return 'done'

async def update(id: int, request: schemas.CameraUpdate, db:Session):
  print("here"*10)
  camera = db.query(models.Camera).filter(models.Camera.id == id)
  box =  db.query(models.Box).filter(models.Box.id == camera.first().box_id).first()
  if not box:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'box with id {id} is not available')
  if not camera.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'camera with id {id} is not available')
  try:
    camera.update(request.dict())
    await update_camera_at_box(
        schemas.CameraBox(
            camera_id=camera.first().id,
            user_id=box.place.user_id,
            name=request.name,
            url=request.url,
            points=request.points,
            detected=request.detected
        ),
        camera.first().id,
        box.link,
        box.place.user_id
      )
    db.commit()
    return 'updated'
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'bad request')

def show(id: int, db: Session):
  camera =db.query(models.Camera).filter(models.Camera.id == id).first()
  if not camera:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'camera with id {id} is not available')
  box = db.query(models.Box).filter(models.Box.id == camera.box_id).first()
  camera.url = box.link + '?url=' + camera.url
  return camera
