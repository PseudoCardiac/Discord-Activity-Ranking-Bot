import discord, json
from discord.ext.commands import Cog
from utils import reorderRoles


class ReorderRolesCog( Cog ):
    def __init__( self, bot ):
        self.mhd: discord.Guild = bot.get_guild( 1020825427025068123 )  # type: ignore
        self.pivotRole: discord.Role = self.mhd.get_role( 1527271285103792263 )   # type: ignore
    

    @discord.app_commands.command( name = "역할_재정렬", description = "순위에 따라 역할을 재정렬한다" )
    async def reorderRolesCommand( self, i: discord.Interaction ):
        await i.response.defer()

        await reorderRoles( self.mhd, self.pivotRole )

        await i.followup.send( "역할 재정렬됨" )