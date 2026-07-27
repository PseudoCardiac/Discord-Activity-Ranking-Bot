import json, discord


roleDict: dict[ str, str ] = {}

with open( "data/role.json", 'r', encoding = "UTF-8" ) as f:
    roleDict = json.load( f )


async def reorderRoles( mhd: discord.Guild, pivotRole: discord.Role ):
    simpleRanking: dict[ str, int ] = {}
    with open( "data/prev_ranking.json", 'r', encoding = "UTF-8" ) as f:
        simpleRanking = json.load( f, indent = 4 )

    simplerRanking: list[ str ] = []

    for id, _ in sorted( simpleRanking.items(), key = lambda x: x[1] ):
        simplerRanking.append( id )

    prev = pivotRole

    for memberId in simplerRanking:
        if roleDict.get( memberId ) is None:
            continue

        role = mhd.get_role( int( roleDict[ memberId ] ) )
        if role is None:
            # print( f"role not found!" )
            continue
        # print( f"role { role.name } found!" )

        await role.move( above = prev, offset = -1 )
        # print( f"{ role.name } moved below { prev.name }!" )
        prev = role
        # print( f"prev role set to { role.name }!" )