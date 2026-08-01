import json, discord


def getAltAccount( id: str, guild: discord.Guild ):
    with open( "data/account.json", 'r', encoding = "UTF-8" ) as f:
        accountDict: dict[ str, str ] = json.load( f )

    altAccId = None

    for subAcc, mainAcc in accountDict.items():
        if subAcc == id:
            altAccId = mainAcc
            break
        elif mainAcc == id:
            altAccId = subAcc
            break
    else:
        return None

    altAcc: discord.Member = guild.get_member( int( altAccId ) )    # type: ignore
    
    return altAcc


def getMainAccount( id: str, guild: discord.Guild ):
    with open( "data/account.json", 'r', encoding = "UTF-8" ) as f:
        accountDict: dict[ str, str ] = json.load( f )

    mainAccId = accountDict.get( id )
    if mainAccId is None:
        return None

    mainAcc: discord.Member = guild.get_member( int( mainAccId ) )  # type: ignore

    return mainAcc