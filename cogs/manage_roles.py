import discord, json
from discord.ext.commands import Bot, Cog


class ManageRolesCog( Cog ):
    def __init__( self, bot: Bot ):
        self.bot = bot
        self.MHD: discord.Guild = self.bot.get_guild( 1020825427025068123 ) # type: ignore
        self.PIVOT: discord.Role = self.MHD.get_role( 1527271285103792263 ) # type: ignore
        self.roleDict: dict[ str, str ] = {}

        with open( "data/role.json", 'r', encoding = "UTF-8" ) as f:
            self.roleDict = json.load( f )


    async def reorderRoles( self, ranking: list[ str ] ):
        prev = self.PIVOT

        for memberId in ranking:
            if self.roleDict.get( memberId ) is None:
                return

            role = self.MHD.get_role( int( self.roleDict[ memberId ] ) )
            if role is None:
                print( f"role not found!" )
                return
            print( f"role { role.name } found!" )

            await role.move( above = prev, offset = -1 )
            print( f"{ role.name } moved below { prev.name }!" )
            prev = role
            print( f"prev role set to { role.name }!" )


    @discord.app_commands.command( name = "역할_재정렬", description = "통계 메시지를 전송할 채널을 설정한다" )
    async def reorderRolesCommand( self, i: discord.Interaction ):
        await self.reorderRoles(
            [
                "749919908988452874",
                "632152187962785793",
                "289968032527155200",
                "464784467391676436",
                "513676568745213953"
            ]
        )

        await i.response.send_message( "역할 재정렬됨" )