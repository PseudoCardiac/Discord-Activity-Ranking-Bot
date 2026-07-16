import json


def addNumber( guildId, memberId, number ):
    d: dict[ str, dict[ str, dict[ str, int ] ] ] = {}
    guildId = str( guildId )
    memberId = str( memberId )

    with open( "data/stat.json", 'r', encoding = "UTF-8" ) as f:
        d = json.load( f )

    if d.get( guildId ) is None:
        d[ guildId ] = {}

    if d[ guildId ].get( memberId ) is None:
        d[ guildId ][ memberId ] = { "characters": number, "messages": 1 }
    else:
        d[ guildId ][ memberId ][ "characters" ] += number
        d[ guildId ][ memberId ][ "messages" ] += 1

    with open( "data/stat.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( d, f, indent = 4 )