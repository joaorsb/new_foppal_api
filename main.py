from fastapi import FastAPI
from starlette.status import HTTP_404_NOT_FOUND
from controllers import news_links, football_teams, events

new_foppal = FastAPI()

new_foppal.include_router(
    news_links.router,
    prefix="/api", 
    responses={HTTP_404_NOT_FOUND: {"message": "Page not Found"}}
)

new_foppal.include_router(
    football_teams.router,
    prefix="/api/teams",
    responses={HTTP_404_NOT_FOUND: {"message": "Page not Found"}}
)

new_foppal.include_router(
    events.router,
    prefix="/api/events",
    responses={HTTP_404_NOT_FOUND: {"message": "Page not Found"}}
)
