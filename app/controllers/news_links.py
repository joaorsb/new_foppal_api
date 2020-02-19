from fastapi import APIRouter, Query
from typing import List, Optional
import arrow

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


@router.get("/{app_link}/recent/{last_date}", response_model=List[NewsLink])
async def get_recent_links(
        app_link: AppLinkModel,
        last_date: str
):

    """
    Get most recent news for country/date
    :param app_link: Country name
    :param last_date: date string 
    :return: List of News
    """
    collection = DBConnection.create_main_connection(app_link)
    parsed_date = arrow.get(last_date).datetime
    documents = collection.find({"visible": True, "publishing_date": { "$gt": parsed_date}}).sort('publishing_date')
    news = []
    async for doc in documents:
        news.append(doc)

    return news


@router.get("/{app_link}/league/{league}", response_model=List[NewsLink])
async def get_links_by_league(app_link: AppLinkModel, league: str, page: Optional[int] = None):
    """
    View for news based on country and filtered by league
    :param app_link: Country name
    :param league: league name
    :param page: query param for pagination
    :return: list of News
    """
    teams_collection = DBConnection.create_teams_connection(app_link)
    links_collection = DBConnection.create_main_connection(app_link)
    names = []
    news = []
    if app_link.value == 'brazil' or app_link.value == 'espana':
        league_name = league
    else:
        league_name = league.title()

    teams = teams_collection.find({'league': league_name})

    async for team in teams:
        names.append(team['intl_name'])

    documents = links_collection.find({
        "visible": True,
        "$or": [{"team_name": {"$in": names}}, {"secondary_team_names": {"$in": names}}],
    }).sort('publishing_date', -1)

    if page and page > 1:
        skip_counter = 25 * (page - 1)
        documents.skip(skip_counter)

    async for doc in documents.limit(25):
        news.append(doc)

    return news


@router.get("/{app_link}/league/{league}/recent/{last_date}", response_model=List[NewsLink])
async def get_recent_links_by_league(app_link: AppLinkModel, league: str, last_date: str):
    """
    View for news based on country and filtered by league
    :param app_link: Country name
    :param league: league name
    :param last_date: last date string
    :return: list of News
    """
    teams_collection = DBConnection.create_teams_connection(app_link)
    links_collection = DBConnection.create_main_connection(app_link)
    names = []
    news = []
    parsed_date = arrow.get(last_date).datetime

    if app_link.value == 'brazil' or app_link.value == 'espana':
        league_name = league
    else:
        league_name = league.title()

    teams = teams_collection.find({'league': league_name})

    async for team in teams:
        names.append(team['intl_name'])

    documents = links_collection.find({
        "visible": True,
        "publishing_date": { "$gt": parsed_date},
        "$or": [{"team_name": {"$in": names}}, {"secondary_team_names": {"$in": names}}],
    }).sort('publishing_date')

    async for doc in documents:
        news.append(doc)

    return news


@router.get("/{app_link}/teams/{team_name}", response_model=List[NewsLink])
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
    teams = [team_name]
    documents = links_collection.find({
        "visible": True,
        "$or": [{"team_name": team_name}, {"secondary_team_names": {"$in": teams}}]
    }).sort('publishing_date', -1)

    if page and page > 1:
        skip_counter = 25 * (page - 1)
        documents.skip(skip_counter)

    async for doc in documents.limit(25):
        news.append(doc)

    return news


@router.get("/{app_link}/teams/{team_name}/recent/{last_date}", response_model=List[NewsLink])
async def get_recent_links_by_team(app_link: AppLinkModel, team_name: str, last_date: str):
    """
    View for news based on country and filtered by league
    :param app_link: Country name
    :param team_name: league name
    :param last_date: last date string from frontend
    :return: list of News
    """
    links_collection = DBConnection.create_main_connection(app_link)
    news = []
    teams = [team_name]
    parsed_date = arrow.get(last_date).datetime

    documents = links_collection.find({
        "visible": True,
        "publishing_date": { "$gt": parsed_date},
        "$or": [{"team_name": team_name}, {"secondary_team_names": {"$in": teams}}]
    }).sort('publishing_date')

    async for doc in documents:
        news.append(doc)

    return news
