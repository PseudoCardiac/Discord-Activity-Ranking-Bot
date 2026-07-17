import re


def numChar( txt ):
    # 이모지
    emoji = r"<[a]?:.+?:[0-9]+>"
    txt = re.sub( emoji, 'e', txt )

    # URL
    url = r"((https?:\/\/)?(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\/=]*))"
    txt = re.sub( url, 'u', txt )

    return len( txt )