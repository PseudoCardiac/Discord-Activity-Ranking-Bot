import json


def addNumber( guildId, memberId, number ):
    statDict: dict[ str, dict[ str, int ] ] = {}
    accountDict: dict[ str, str ] = {}

    guildId = str( guildId )
    memberId = str( memberId )

    with open( "data/account.json", 'r', encoding = "UTF-8" ) as f:
        accountDict = json.load( f )

    # 부계가 있는 경우 본계로 카운트
    if accountDict.get( memberId ):
        memberId = accountDict[ memberId ]

    with open( "data/stat.json", 'r', encoding = "UTF-8" ) as f:
        statDict = json.load( f )

    if statDict.get( memberId ) is None:
        statDict[ memberId ] = { "characters": number, "messages": 1 }
    else:
        statDict[ memberId ][ "characters" ] += number
        statDict[ memberId ][ "messages" ] += 1

    with open( "data/stat.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( statDict, f, indent = 4 )