import discord, json
from discord.ext.commands import Cog


class NotifChannelConfigCog( Cog ):
    @discord.app_commands.command( name = "통계_채널_설정", description = "통계 메시지를 전송할 채널을 설정한다" )
    async def notifChannelConfig( self, i: discord.Interaction, channel: discord.TextChannel ):
        d: dict[ str, str ] = {}

        with open( "data/channel.json", 'r', encoding = "UTF-8" ) as f:
            d = json.load( f )

        d[ str( i.guild_id ) ] = str( channel.id )

        with open( "data/channel.json", 'w', encoding = "UTF-8" ) as f:
            json.dump( d, f, indent = 4 )

        await i.response.send_message( channel.name )