from fastapi import APIRouter
from typing import List, Optional

from services.db import DBConnection
from models.app_link_model import AppLinkModel
from models.news_link_model import NewsLink


router = APIRouter()


@router.get("/{app_link}", response_model=List[NewsLink])
async def root(app_link: AppLinkModel, page: Optional[int] = None):
    collection = DBConnection.create_main_connection(app_link)
    documents = collection.find({"visible": True}).sort('publishing_date', -1)
    if page and page > 1:
        skip_counter = 25 * (page - 1)
        documents.skip(skip_counter)
    news = []
    async for doc in documents.limit(25):
        news.append(doc)

    return news


@router.get("/{app_link}/{league}", response_model=List[NewsLink])
async def get_links_by_league(app_link: AppLinkModel, league: str, page: Optional[int] = None):
    teams_collection = DBConnection.create_teams_connection()
    links_collection = DBConnection.create_main_connection(app_link)
    names = []
    news = []
    teams = teams_collection.find({'league': league})

    for team in teams:
        names.append(team.intl_name)

    documents = links_collection.find({"visible": True}).sort('publishing_date', -1)

    if page and page > 1:
        skip_counter = 25 * (page - 1)
        documents.skip(skip_counter)

    async for doc in documents.limit(25):
        news.append(doc)

    return news
