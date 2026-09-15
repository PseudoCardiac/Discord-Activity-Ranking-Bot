import discord, json
from discord.ext.commands import Cog, Bot
from utils import reorderRoles
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import RankingBot


class ReorderRolesCog( Cog ):
    def __init__( self, bot: "RankingBot" ):
        self.bot = bot


    @discord.app_commands.command( name = "역할_재정렬", description = "순위에 따라 역할을 재정렬한다" )
    async def reorderRolesCommand( self, i: discord.Interaction ):
        await i.response.defer()

        await reorderRoles( self.bot.MHD, self.bot.PIVOT_ROLE )

        await i.followup.send( "역할 재정렬됨" )