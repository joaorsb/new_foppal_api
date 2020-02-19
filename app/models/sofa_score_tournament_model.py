from enum import Enum


class SofaScoreTournamentModel(str, Enum):
    serie_a = 'Brasileiro Série A'
    serie_b = 'Brasileiro Série B'
    bundesliga = 'Bundesliga'
    laliga = 'LaLiga'
    laliga_2 = 'LaLiga 2'
    eredivisie = 'Eredivisie'
    eliteserien = 'Eliteserien'
    obos = '1st Division'
    allsvenskan = 'Allsvenskan'
