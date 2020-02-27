from fastapi import FastAPI
from app.controllers import EventRouter, FootballTeamsRouter, NewsLinksRouter
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect
from app.services import Notifier
from app.models import AppLinkModel

app = FastAPI()
notifier = Notifier()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://35.188.14.229",
    "http://35.188.14.229:3000",
    "http://35.188.14.229:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    NewsLinksRouter,
    prefix="/api", 
    tags=['news'],
)

app.include_router(
    FootballTeamsRouter,
    prefix="/api/teams",
    tags=['teams']
)

app.include_router(
    EventRouter,
    prefix="/api/events",
    tags=['events']
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)


@app.get("/push/{app_link}")
async def push_to_connected_websockets(app_link: AppLinkModel):
    await notifier.push(f"{app_link}")


@app.on_event("startup")
async def startup():
    # Prime the push notification generator
    await notifier.generator.asend(None)
