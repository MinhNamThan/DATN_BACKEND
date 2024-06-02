from pydantic import BaseModel
from typing import Union, List

class User(BaseModel):
    email: str
    password: str

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

class BoxUpdate(BaseModel):
    name: str
    link: str
    username: str
    password: str

class Camera(BaseModel):
    box_id: int
    name: str
    url: str

class CameraBox(BaseModel):
    camera_id: int
    user_id: int
    name: str
    url: str
    points:str

class CameraUpdate(BaseModel):
    name: str
    url: str

class Notification(BaseModel):
    title: str
    description: str
    videoUrl: str
    camera_id: int

class NotificationCreate(BaseModel):
    title: str
    description: str
    videoUrl: str
    camera_id: int
    user_id: int
