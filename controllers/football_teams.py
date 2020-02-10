from fastapi import APIRouter
from typing import List, Optional

from services.db import DBConnection
from models.app_link_model import AppLinkModel
from models.team_model import FootballTeam


router = APIRouter()


@router.get("/{app_link}/{league}", response_model=List[FootballTeam])
async def root(app_link: AppLinkModel, league: str, page: Optional[int] = None):
    collection = DBConnection.create_teams_connection(app_link)
    documents = collection.find({'league': league})
    if page and page > 1:
        skip_counter = 25 * (page - 1)
        documents.skip(skip_counter)
    news = []
    async for doc in documents.limit(25):
        news.append(doc)

    return news
