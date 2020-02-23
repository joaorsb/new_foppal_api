from enum import Enum
from datetime import datetime


class LeaguesModel(str, Enum):
    serie_a = 'serie_a'
    serie_b = 'serie_b'
    bundesliga = 'bundesliga'
    laliga = 'laliga'
    laliga_2 = 'laliga_2'
    eredivisie = 'eredivisie'
    eliteserien = 'eliteserien'
    obos = 'obos'
    allsvenskan = 'allsvenskan'

    @staticmethod
    def get_league_year(league_name: str) -> str:
        norge_brazil = [
            LeaguesModel.eliteserien,
            LeaguesModel.obos,
            LeaguesModel.serie_a,
            LeaguesModel.serie_b
        ]
        current_year = str(datetime.now().year)

        if league_name not in norge_brazil:
            last_year = str(datetime.now().year - 1)[-2:]
            season_year = f"{last_year}/{current_year[-2:]}"
        else:
            season_year = current_year

        return season_year
