from fastapi import APIRouter
from typing import List
from datetime import datetime, timedelta

from app.services import DBConnection
from app.models import AppLinkModel, Event, SofaScoreTournamentModel, LeaguesModel


router = APIRouter()


@router.get("/{app_link}/{league}", response_model=List[Event])
async def root(app_link: AppLinkModel, league: LeaguesModel):
    """
        Get all events based on country, league and season year
    :param app_link: Country
    :param league: League name from SofaScore
    :return: List of all events(matches) for the given league/season
    """
    season_year = LeaguesModel.get_league_year(league_name=league)
    collection = DBConnection.create_events_connection(app_link)
    documents = collection.find({
        'tournament_name': SofaScoreTournamentModel[league],
        'season_year': season_year
    }).sort('start_time')
    events = []
    async for doc in documents:
        events.append(doc)

    return events


@router.get("/{app_link}/{league}/next_round", response_model=List[Event])
async def next_round_events(app_link: AppLinkModel, league: LeaguesModel):
    """
        Get next round for given country/league/year
    :param app_link: country
    :param league: League name based uppon SofaScore naming
    :return: List of the next round events(matches) based on the current date
    """
    season_year = LeaguesModel.get_league_year(league_name=league)
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
        }).sort('start_time')
        async for doc in documents:
            events.append(doc)

    return events


@router.get("/{app_link}/{league}/round/{league_round_id}", response_model=List[Event])
async def events_by_round_id(app_link: AppLinkModel, league: LeaguesModel, league_round_id: int):
    """
        Get events(matches) by Country, league, year for especific round based on its id
    :param league_round_id:  Round number
    :param app_link: Country
    :param league: league name from SofaScore
    :param league_round_id: round id number
    :return: List of matches for given league/year/round
    """
    season_year = LeaguesModel.get_league_year(league_name=league)
    collection = DBConnection.create_events_connection(app_link)
    documents = collection.find({
        'tournament_name': SofaScoreTournamentModel[league],
        'season_year': season_year,
        'round': league_round_id
    }).sort('start_time')
    events = []
    async for doc in documents:
        events.append(doc)

    return events
