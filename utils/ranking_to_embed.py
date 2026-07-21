import discord, json, math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discord.ext import commands
from .stat_to_ranking import statToRanking


def rankingToEmbed( bot: "commands.Bot", guild: discord.Guild ):
    ranking: list[ tuple[ str, float ] ] = statToRanking()
    stat: dict[ str, dict[ str, int ] ] = {}

    with open( "data/stat.json", 'r', encoding = "UTF-8" ) as f:
        stat = json.load( f )

    embed = discord.Embed( title = "통계" )
    embed2 = discord.Embed( title = "통계 (2페이지)" )

    i = 1

    for userId, score in ranking:
        if stat.get( userId ) is None:
            continue

        userObj = bot.get_user( int( userId ) )
        if userObj is None:
            continue

        userDisplayName = userObj.display_name
        userName = userObj.name
        char = stat[ userId ].get( "characters" ) or 0
        msg = stat[ userId ].get( "messages" ) or 1
        voice = stat[ userId ].get( "voice" ) or 0
        stream = stat[ userId ].get( "stream" ) or 0

        if i <= 25:
            embed.add_field(
                name = f"#{ i } { userDisplayName } · { score }점",
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