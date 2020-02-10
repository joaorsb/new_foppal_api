from pydantic import BaseModel
from bson import objectid
from datetime import datetime


class Event(BaseModel):
    _id: objectid.ObjectId
    tournament_name: str
    season_year: str
    round: int
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    event_name: str
    start_time: datetime
    sofa_score_event_id: int
    status_description: str
