from .stat_to_ranking import statToRanking


def statToSimpleRanking():
    idAndScore: list[ tuple[ str, float ] ] = statToRanking()
    simpleRanking: dict[ str, int ] = {}

    i = 1
    for id, _ in idAndScore:
        simpleRanking[ id ] = i
        i += 1

    return simpleRanking