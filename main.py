from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import user, authentication, place, box, camera, notification, websocket
from fastapi_pagination import add_pagination

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(place.router)
app.include_router(box.router)
app.include_router(camera.router)
app.include_router(notification.router)
app.include_router(websocket.router)

add_pagination(app)

manager = websocket.ConnectionManager()
@app.get('/')
def index():
  return "hello"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
