import discord, json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discord.ext import commands


def statToEmbed( bot: "commands.Bot", guild: discord.Guild ):
    d: dict[ str, dict[ str, dict[ str, int ] ] ] = {}
    guildId = str( guild.id )

    with open( "data/stat.json", 'r', encoding = "UTF-8" ) as f:
        d = json.load( f )

    embed = discord.Embed( title = "통계" )
    embed2 = discord.Embed( title = "통계 (2페이지)" )

    i = 1
    for userId, stat in sorted( d.items(), key = lambda x: x[1][ "characters" ], reverse = True ):  # type: ignore
        user = bot.get_user( int( userId ) )
        if user is None:
            continue

        userDisplayName = user.display_name
        userName = user.name
        char = stat.get( "characters" ) or 0
        msg = stat.get( "messages" ) or 0
        voice = stat.get( "voice" ) or 0
        stream = stat.get( "stream" ) or 0

        if i <= 25:
            embed.add_field(
                name = f"#{ i } { userDisplayName } (`@{ userName }`)",
                value = f"텍스트 | { char }자, { msg }건 ({ round( char / msg, 2 ) }자/건)\n" + \
                        f"보이스 | { voice }초\n" + \
                        f"라이브 | { stream }초",
                inline = False
            )
        else:
            embed2.add_field(
                name = f"#{ i } { userDisplayName } (`@{ userName }`)",
                value = f"{ char }자, { msg }건 ({ round( char / msg, 2 ) }자/건)",
                inline = False
            )

        i += 1

    if i <= 26:
        return [ embed ]
    else:
        return [ embed, embed2 ]