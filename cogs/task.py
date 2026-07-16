import discord, datetime
from zoneinfo import ZoneInfo
from discord.ext import commands, tasks


MIDNIGHT = datetime.time(
    hour = 0, minute = 0, second = 0,
    tzinfo = ZoneInfo( "Asia/Seoul" )
)


class TaskCog( commands.Cog ):
    def __init__( self, bot, testChannel: discord.TextChannel ):
        self.bot = bot
        self.testChannel = testChannel
        self.checkDay.start()

    @tasks.loop( time = MIDNIGHT )
    async def checkDay( self ):
        isMonday = datetime.datetime.now( tz = ZoneInfo( "Asia/Seoul" ) ).weekday() == 0

        # 통계 내기 + 기록 초기화
        if isMonday:
            pass