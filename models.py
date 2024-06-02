from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String)
  password = Column(String)
  fullName = Column(String)
  phoneNumber = Column(String)

  places = relationship("Place", back_populates="owner")
  notifications = relationship("Notification", back_populates="owner")

class Place(Base):
  __tablename__ = "places"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  description = Column(String)
  user_id = Column(Integer, ForeignKey("users.id"))
  owner = relationship("User", back_populates="places")
  boxes = relationship("Box", back_populates="place")

class Box(Base):
  __tablename__ = "boxes"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  link = Column(String)
  username = Column(String)
  password = Column(String)
  place_id = Column(Integer, ForeignKey("places.id"))
  place = relationship("Place", back_populates="boxes")
  cameras = relationship("Camera", back_populates="box")

class Camera(Base):
  __tablename__ = "cameras"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  url = Column(String)
  box_id = Column(Integer, ForeignKey("boxes.id"))
  box = relationship("Box", back_populates="cameras")
  notifications = relationship("Notification", back_populates="camera")

class Notification(Base):
  __tablename__ = "notifications"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  description = Column(String)
  videoUrl = Column(String)
  status = Column(String)
  created_at = Column(String)
  camera_id = Column(Integer, ForeignKey("cameras.id"))
  user_id = Column(Integer, ForeignKey("users.id"))
  camera = relationship("Camera", back_populates="notifications")
  owner = relationship("User", back_populates="notifications")
