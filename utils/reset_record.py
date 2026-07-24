import json


def resetRecord():
    with open( "data/voice.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( {}, f )

    with open( "data/stream.json", 'w', encoding = "UTF-8" ) as f:
        json.dump( {}, f )