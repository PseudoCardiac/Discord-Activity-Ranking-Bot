import json, math


def statToRanking():
    rankingDict: dict[ str, float ] = {}
    statDict: dict[ str, dict[ str, int ] ] = {}

    with open( "data/stat.json", 'r', encoding = "UTF-8" ) as f:
        statDict = json.load( f )

    for userId, stat in statDict.items():
        score = 0

        if stat.get( "characters" ):
            score += math.log( stat[ "characters" ] // 5 + 1 )

        if stat.get( "voice" ):
            score += math.log( stat[ "voice" ] + ( stat.get( "stream" ) or 0 ) // 2 + 1 )

        rankingDict[ userId ] = round( score * 10, 2 )

    # 점수 순위 리스트
    return [ ( userId, score ) for userId, score
                in sorted( rankingDict.items(),
                            key = lambda x: x[1],
                            reverse = True ) ]