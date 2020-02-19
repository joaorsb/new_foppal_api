from fastapi import FastAPI
from app.controllers import EventRouter, FootballTeamsRouter, NewsLinksRouter
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
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
