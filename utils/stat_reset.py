import json
from .stat_to_simple_ranking import statToSimpleRanking


def statReset():
    """
    순위를 `ranking_prev.json`으로 옮기고 리셋한다.
    """
    ranking = statToSimpleRanking()

    with open( "data/prev_ranking.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( ranking, f, indent = 4 )

    statDict = {}

    with open( "data/stat.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( statDict, f, indent = 4 )