from pydantic import BaseModel
from bson import objectid
from datetime import datetime


class NewsLink(BaseModel):
    _id: objectid.ObjectId
    team_name: str
    url: str
    visible: bool = True
    headline: str
    publishing_date: datetime
    last_updated: datetime
    secondary_team_names: str
    language: str
