import discord, datetime
from zoneinfo import ZoneInfo
from discord.ext import commands, tasks
from utils import rankingToEmbed, statReset, reorderRoles, cutVoice


MIDNIGHT = datetime.time(
    hour = 0, minute = 0, second = 0,
    tzinfo = ZoneInfo( "Asia/Seoul" )
)


class TaskCog( commands.Cog ):
    def __init__( self, bot: commands.Bot, notifChannel: discord.TextChannel ):
        self.bot = bot
        self.testChannel = notifChannel
        self.checkDay.start()


    @tasks.loop( time = MIDNIGHT )
    async def checkDay( self ):
        # isMonday = datetime.datetime.now( tz = ZoneInfo( "Asia/Seoul" ) ).weekday() == 0

        # if not isMonday:
        #     return

        await self.testChannel.send( embeds = rankingToEmbed( self.bot ) )

        cutVoice()
        statReset()

        mhd: discord.Guild = self.bot.get_guild( 1020825427025068123 )  # type: ignore
        pivotRole: discord.Role = mhd.get_role( 1527271285103792263 )   # type: ignore

        await reorderRoles( mhd, pivotRole )