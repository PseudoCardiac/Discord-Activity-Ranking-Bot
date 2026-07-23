import discord, json, math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discord.ext import commands
from .stat_to_ranking import statToRanking


def rankingToEmbed( bot: "commands.Bot" ):
    ranking: list[ tuple[ str, float ] ] = statToRanking()
    prevRanking: dict[ str, int ] = {}
    stat: dict[ str, dict[ str, int ] ] = {}

    with open( "data/prev_ranking.json", 'r', encoding = "UTF-8" ) as f:
        prevRanking = json.load( f )

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
        char = stat[ userId ].get( "characters" ) or 0
        msg = stat[ userId ].get( "messages" ) or 1
        voice = stat[ userId ].get( "voice" ) or 0
        stream = stat[ userId ].get( "stream" ) or 0

        prevRank = prevRanking.get( userId )

        if prevRank:
            rankDiff = prevRank - i
        else:
            rankDiff = None

        if rankDiff is not None:
            if rankDiff > 0:
                rankDiffText = "<:rank_up:1529688180587102239>" + str( rankDiff )
            elif rankDiff < 0:
                rankDiffText = "<:rank_down:1529688178888278057>" + str( -rankDiff )
            else:
                rankDiffText = "<:rank_unchanged:1529699376816193616>0"
        else:
            rankDiffText = ""

        if i <= 25:
            embed.add_field(
                name = f"#{ i } { userDisplayName } · { score }점  { rankDiffText }",
                value = f"텍스트 | { char }자, { msg }건 ({ round( char / msg, 2 ) }자/건)\n" + \
                        f"보이스 | { voice }분\n" + \
                        f"라이브 | { stream }분",
                inline = False
            )
        else:
            embed2.add_field(
                name = f"#{ i } { userDisplayName } · { score }점  { rankDiffText }",
                value = f"텍스트 | { char }자, { msg }건 ({ round( char / msg, 2 ) }자/건)\n" + \
                        f"보이스 | { voice }분\n" + \
                        f"라이브 | { stream }분",
                inline = False
            )

        i += 1        

    if i <= 26:
        return [ embed ]
    else:
        return [ embed, embed2 ]