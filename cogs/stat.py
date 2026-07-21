import discord, json
from discord.ext.commands import Bot, Cog
from utils import rankingToEmbed, statReset


class StatCog( Cog ):
    def __init__( self, bot: Bot ):
        self.bot = bot


    @discord.app_commands.command( name = "통계", description = "통계를 표시한다" )
    async def stat( self, i: discord.Interaction ):
        if not i.guild:
            return

        await i.response.send_message( embeds = rankingToEmbed( self.bot, i.guild ) )


    @discord.app_commands.command( name = "통계_초기화", description = "통계를 초기화한다" )
    async def statReset( self, i: discord.Interaction ):
        statReset()

        await i.response.send_message( "통계 초기화됨" )