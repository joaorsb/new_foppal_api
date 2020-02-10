from fastapi import APIRouter
from typing import List, Optional

from services.db import DBConnection
from models.app_link_model import AppLinkModel
from models.team_model import FootballTeam


router = APIRouter()


@router.get("/{app_link}/{league}", response_model=List[FootballTeam])
async def root(app_link: AppLinkModel, league: str):
    collection = DBConnection.create_teams_connection(app_link)
    if app_link.value == 'brazil' or app_link.value == 'espana':
        league_name = league
    else:
        league.title()

    documents = collection.find({"league": league_name})
    teams = []
    async for doc in documents:
        teams.append(doc)

    return teams
