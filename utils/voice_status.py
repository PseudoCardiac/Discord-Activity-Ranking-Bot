import json, datetime, discord
from zoneinfo import ZoneInfo
from .get_alt_account import getAltAccount, getMainAccount


def recordVoiceJoin( id: str, guild: discord.Guild ):
    """
    보이스 참여 시간을 기록한다 (멤버 참여 시 호출)
    """
    mainAcc = getMainAccount( id, guild )
    if mainAcc is not None:
        id = str( mainAcc.id )

    voiceDict: dict[ str, str ]

    with open( "data/voice.json", 'r', encoding = "UTF-8" ) as f:
        voiceDict = json.load( f )

    voiceDict[ id ] = datetime.datetime.now( tz = ZoneInfo( "Asia/Seoul" ) ).strftime( "%Y/%m/%d %H:%M:%S %z" )

    with open( "data/voice.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( voiceDict, f, indent = 4 )


def addVoiceTime( id: str, guild: discord.Guild ):
    """
    보이스 참여 시간과 현재 시간의 차를 통계에 더한다 (멤버 퇴장 시 호출)
    """
    mainAcc = getMainAccount( id, guild )
    if mainAcc is not None:
        id = str( mainAcc.id )

    statDict: dict[ str, dict[ str, int ] ] = {}
    voiceDict: dict[ str, str ] = {}

    with open( "data/stat.json", 'r', encoding = "UTF-8" ) as f:
        statDict = json.load( f )

    with open( "data/voice.json", 'r', encoding = "UTF-8" ) as f:
        voiceDict = json.load( f )

    # 예외: 기록된 참가 시간이 없음
    joinTime = voiceDict.get( id )
    if joinTime is None:
        return
    else:
        del voiceDict[ id ]

    timeDelta = datetime.datetime.now( tz = ZoneInfo( "Asia/Seoul" ) ) - datetime.datetime.strptime( joinTime, "%Y/%m/%d %H:%M:%S %z" )
    minutes = timeDelta.seconds // 60

    with open( "data/account.json", 'r', encoding = "UTF-8" ) as f:
        accountDict = json.load( f )

    # 부계가 있는 경우 본계로 카운트
    if accountDict.get( id ):
        id = accountDict[ id ]

    if not statDict.get( id ):
        statDict[ id ] = {}

    if statDict[ id ].get( "voice" ):
        statDict[ id ][ "voice" ] += minutes
    else:
        statDict[ id ][ "voice" ] = minutes

    with open( "data/stat.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( statDict, f, indent = 4 )

    with open( "data/voice.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( voiceDict, f, indent = 4 )


def recordStreamStart( id: str, guild: discord.Guild ):
    """
    스트림 시간을 기록한다 (스트림 시작 시 호출)
    """
    mainAcc = getMainAccount( id, guild )
    if mainAcc is not None:
        id = str( mainAcc.id )

    streamDict: dict[ str, str ]

    with open( "data/stream.json", 'r', encoding = "UTF-8" ) as f:
        streamDict = json.load( f )

    streamDict[ id ] = datetime.datetime.now( tz = ZoneInfo( "Asia/Seoul" ) ).strftime( "%Y/%m/%d %H:%M:%S %z" )

    with open( "data/stream.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( streamDict, f, indent = 4 )


def addStreamTime( id: str, guild: discord.Guild ):
    """
    스트리 시작 시간과 현재 시간의 차를 통계에 더한다 (스트림 종료 시 호출)
    """
    mainAcc = getMainAccount( id, guild )
    if mainAcc is not None:
        id = str( mainAcc.id )

    statDict: dict[ str, dict[ str, int ] ] = {}
    streamDict: dict[ str, str ] = {}

    with open( "data/stat.json", 'r', encoding = "UTF-8" ) as f:
        statDict = json.load( f )

    with open( "data/stream.json", 'r', encoding = "UTF-8" ) as f:
        streamDict = json.load( f )

    # 예외: 기록된 스트리밍 시작 시간이 없음
    startTime = streamDict.get( id )
    if startTime is None:
        return
    else:
        del streamDict[ id ]

    timeDelta = datetime.datetime.now( tz = ZoneInfo( "Asia/Seoul" ) ) - datetime.datetime.strptime( startTime, "%Y/%m/%d %H:%M:%S %z" )
    minutes = timeDelta.seconds // 60

    with open( "data/account.json", 'r', encoding = "UTF-8" ) as f:
        accountDict = json.load( f )

    # 부계가 있는 경우 본계로 카운트
    if accountDict.get( id ):
        id = accountDict[ id ]
        
    if not statDict.get( id ):
        statDict[ id ] = {}
        
    if statDict[ id ].get( "stream" ):
        statDict[ id ][ "stream" ] += minutes
    else:
        statDict[ id ][ "stream" ] = minutes

    with open( "data/stat.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( statDict, f, indent = 4 )

    with open( "data/stream.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( streamDict, f, indent = 4 )


async def checkVoiceStatus( id: str, guild: discord.Guild ):
    """
    주어진 계정의 본계 또는 부계가 동시 접속 중인지 확인
    """
    altAcc = getAltAccount( id, guild )
    if altAcc is None:
        return

    try:
        altVoiceStatus = await altAcc.fetch_voice()
    except:
        return False
    
    if altVoiceStatus.channel is None:
        return False

    return True


async def checkStreamStatus( id: str, guild: discord.Guild ):
    """
    주어진 계정의 본계 또는 부계가 동시 라이브 중인지 확인
    """
    altAcc = getAltAccount( id, guild )
    if altAcc is None:
        return

    try:
        altVoiceStatus = await altAcc.fetch_voice()
    except:
        return False
    
    if not altVoiceStatus.self_stream:
        return False

    return True