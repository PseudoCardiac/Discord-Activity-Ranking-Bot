import discord, json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discord.ext import commands


def statToEmbed( bot: "commands.Bot", guild: discord.Guild ):
    d: dict[ str, dict[ str, dict[ str, int ] ] ] = {}
    id = str( guild.id )

    with open( "data/stat.json", 'r', encoding = "UTF-8" ) as f:
        d = json.load( f )

    embed = discord.Embed( title = "통계" )

    i = 1
    for id, char_and_msg in sorted( d[ id ].items(), key = lambda x: x[1], reverse = True ):  # type: ignore
        user = bot.get_user( int( id ) )
        if user is None:
            continue

        userName = user.display_name
        userId = user.name
        char = char_and_msg[ "characters" ]
        msg = char_and_msg[ "messages" ]

        embed.add_field(
            name = f"#{ i } { userName } (`@{ userId }`)",
            value = f"{ char }자, { msg }건 ({ round( char / msg, 2 ) }자/건)",
            inline = False
        )
        i += 1

    return embed