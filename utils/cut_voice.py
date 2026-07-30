import json, datetime
from zoneinfo import ZoneInfo
from .voice_status import addVoiceTime, addStreamTime


def cutVoice():
    """
    현재 기록 중인 보이스와 스트림을 끊고, 통계에 더한다.
    정기 통계를 산출할 때, 점수를 내기 직전에 호출한다.
    """
    # 파일 읽기
    with open( "data/voice.json", 'r', encoding = "UTF-8" ) as f:
        voiceDict: dict[ str, str ] = json.load( f )

    with open( "data/stream.json", 'r', encoding = "UTF-8" ) as f:
        streamDict: dict[ str, str ] = json.load( f )

    # 1. 기록 중인 보이스와 스트림을 현재 시간에 종료된 것으로 간주하고, 통계에 기록한다.
    # 2. 동일 유저에 대해 현재 시간에 보이스 또는 스트림을 다시 시작한 것으로 기록한다.  
    for id, _ in voiceDict.items():
        addVoiceTime( id )
        voiceDict[ id ] = datetime.datetime.now( tz = ZoneInfo( "Asia/Seoul" ) ).strftime( "%Y/%m/%d %H:%M:%S" )

    for id, _ in streamDict.items():
        addStreamTime( id )
        streamDict[ id ] = datetime.datetime.now( tz = ZoneInfo( "Asia/Seoul" ) ).strftime( "%Y/%m/%d %H:%M:%S" )

    # 파일 쓰기
    with open( "data/voice.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( voiceDict, f, indent = 4 )

    with open( "data/stream.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( streamDict, f, indent = 4 )