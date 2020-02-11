from fastapi import FastAPI
from app.controllers import EventRouter, FootballTeamsRouter, NewsLinksRouter

app = FastAPI()

app.include_router(
    NewsLinksRouter,
    prefix="/api", 
)

app.include_router(
    FootballTeamsRouter,
    prefix="/api/teams",
)

app.include_router(
    EventRouter,
    prefix="/api/events",
)
