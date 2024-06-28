from pydantic import BaseModel
from typing import Union, List
from datetime import datetime

class User(BaseModel):
    email: str
    password: str
    phoneNumber: str
    fullName: str

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None

class Place(BaseModel):
    name: str
    description: str

class Box(BaseModel):
    place_id: int
    name: str
    link: str
    username: str
    password: str

class BoxShow(BaseModel):
    place: Place
    name: str
    link: str
    username: str
    password: str

    class Config:
        orm_mode = True

class BoxUpdate(BaseModel):
    name: str
    link: str
    username: str
    password: str

class Camera(BaseModel):
    box_id: int
    name: str
    url: str
    detected: bool
    points:str

class CameraShow(BaseModel):
    id: int
    name: str
    url: str
    box: BoxShow
    detected: bool
    points:str

    class Config:
        orm_mode = True

class CameraBox(BaseModel):
    camera_id: int
    user_id: int
    name: str
    url: str
    points:str
    detected: bool

class CameraUpdate(BaseModel):
    name: str
    url: str
    detected: bool
    points:str

class Notification(BaseModel):
    id: int
    title: str
    description: str
    videoUrl: str
    camera_id: int
    created_at: datetime

class NotificationShow(BaseModel):
    id: int
    title: str
    description: str
    videoUrl: str
    camera: CameraShow
    created_at: datetime

    class Config:
        orm_mode = True

class NotificationCreate(BaseModel):
    title: str
    description: str
    videoUrl: str
    camera_id: int
    user_id: int
