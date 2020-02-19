from fastapi import APIRouter
from typing import List
from datetime import datetime, timedelta

from app.services import DBConnection
from app.models import AppLinkModel, Event, SofaScoreTournamentModel


router = APIRouter()


@router.get("/{app_link}/{league}/{season_year}", response_model=List[Event])
async def root(app_link: AppLinkModel, league: str, season_year: str):
    """
        Get all events based on country, league and season year
    :param app_link: Country
    :param league: League name from SofaScore
    :param season_year: season year
    :return: List of all events(matches) for the given league/season
    """
    collection = DBConnection.create_events_connection(app_link)
    documents = collection.find({'tournament_name': SofaScoreTournamentModel[league], 'season_year': season_year})
    events = []
    async for doc in documents:
        events.append(doc)

    return events


@router.get("/{app_link}/{league}/{season_year}/next_round", response_model=List[Event])
async def root(app_link: AppLinkModel, league: str, season_year: str):
    """
        Get next round for given country/league/year
    :param app_link: country
    :param league: League name based uppon SofaScore naming
    :param season_year: year
    :return: List of the next round events(matches) based on the current date
    """
    collection = DBConnection.create_events_connection(app_link)
    events = []

    next_round = await collection.find_one({
        'tournament_name': SofaScoreTournamentModel[league],
        'season_year': season_year,
        'start_time': {'$gte': datetime.now()}
    })

    if next_round:
        documents = collection.find({
            'tournament_name': SofaScoreTournamentModel[league],
            'season_year': season_year,
            'round': next_round['round']
        })
        async for doc in documents:
            events.append(doc)

    return events


@router.get("/{app_link}/{league}/{season_year}/round/{league_round_id}", response_model=List[Event])
async def root(app_link: AppLinkModel, league: str, season_year: str, league_round_id: int):
    """
        Get events(matches) by Country, league, year for especific round based on its id
    :param app_link: Country
    :param league: league name from SofaScore
    :param season_year: year
    :param round_id: round id number
    :return: List of matches for given league/year/round
    """
    collection = DBConnection.create_events_connection(app_link)
    documents = collection.find({
        'tournament_name': SofaScoreTournamentModel[league],
        'season_year': season_year,
        'round': league_round_id
    })
    events = []
    async for doc in documents:
        events.append(doc)

    return events
