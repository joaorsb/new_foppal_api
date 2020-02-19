from fastapi import APIRouter
from typing import List

from app.services import DBConnection
from app.models import AppLinkModel, FootballTeam


router = APIRouter()


@router.get("/{app_link}/{league}", response_model=List[FootballTeam])
async def root(app_link: AppLinkModel, league: str):
    """
        Get the list of clubs based on given country and league
    :param app_link: Country name
    :param league: League name
    :return: List of football clubs
    """
    collection = DBConnection.create_teams_connection(app_link)
    if app_link.value == 'brazil' or app_link.value == 'espana':
        league_name = league
    elif league == "postnord":
        league_name = "PostNord"
    else:
        league_name = league.title()

    documents = collection.find({"league": league_name})
    teams = []
    async for doc in documents:
        teams.append(doc)

    return teams
