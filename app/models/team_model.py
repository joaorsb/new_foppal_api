from pydantic import BaseModel
from bson import objectid


class FootballTeam(BaseModel):
    _id: objectid.ObjectId
    team_name: str
    intl_name: str
    league: str
    sites: str