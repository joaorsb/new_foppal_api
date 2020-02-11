from fastapi import APIRouter, Query
from typing import List, Optional

from app.services import DBConnection
from app.models import AppLinkModel, NewsLink

router = APIRouter()


@router.get("/{app_link}", response_model=List[NewsLink])
async def get_all_links(
        app_link: AppLinkModel,
        page: int = Query(None)
):

    """
        Main view for news links based on country
    :param app_link: Country name
    :param page: query param for pagination
    :return: List of News
    """
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
    """
        View for news based on country and filtered by league
    :param app_link: Country name
    :param league: league name
    :param page: query param for pagination
    :return: list of News
    """
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


@router.get("/{app_link}/{team_name}", response_model=List[NewsLink])
async def get_links_by_team(app_link: AppLinkModel, team_name: str, page: Optional[int] = None):
    """
        View for news based on country and filtered by league
    :param app_link: Country name
    :param team_name: league name
    :param page: query param for pagination
    :return: list of News
    """
    links_collection = DBConnection.create_main_connection(app_link)
    news = []
    documents = links_collection.find({
        "visible": True,
        "team_name": team_name,
        "secondary_team_names": {"$in": [team_name]}
    }).sort('publishing_date', -1)

    if page and page > 1:
        skip_counter = 25 * (page - 1)
        documents.skip(skip_counter)

    async for doc in documents.limit(25):
        news.append(doc)

    return news
