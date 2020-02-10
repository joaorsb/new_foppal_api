from fastapi import APIRouter
from typing import List, Optional
from datetime import datetime, timedelta

from services.db import DBConnection
from models.app_link_model import AppLinkModel
from models.event_model import Event


router = APIRouter()


@router.get("/{app_link}/{league}/{season}", response_model=List[Event])
async def root(app_link: AppLinkModel, league: str, season: str):
    collection = DBConnection.create_events_connection(app_link)

    documents = collection.find({'tournament_name': league, 'season_year': season})
    events = []
    async for doc in documents:
        events.append(doc)

    return events


@router.get("/{app_link}/{league}/{season}/round/{league_round}", response_model=List[Event])
async def root(app_link: AppLinkModel, league: str, season: str, league_round: int):
    collection = DBConnection.create_events_connection(app_link)

    documents = collection.find({
        'tournament_name': league,
        'season_year': season,
        'round': league_round
    })
    events = []
    async for doc in documents:
        events.append(doc)

    return events


@router.get("/{app_link}/{league}/{season}/next_round", response_model=List[Event])
async def root(app_link: AppLinkModel, league: str, season: str):
    collection = DBConnection.create_events_connection(app_link)
    current_round = await collection.find_one({
        'tournament_name': league,
        'season_year': season,
        'start_time': {'$gte': datetime.now() + timedelta(days=180)}
    })

    documents = collection.find({
        'tournament_name': league,
        'season_year': season,
        'round': current_round['round']
    })
    events = []
    async for doc in documents:
        events.append(doc)

    return events
