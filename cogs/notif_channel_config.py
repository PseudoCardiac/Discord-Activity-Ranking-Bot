import discord, json
from discord.ext.commands import Cog


class NotifChannelConfigCog( Cog ):
    @discord.app_commands.command( name = "통계_채널_설정", description = "통계 메시지를 전송할 채널을 설정한다" )
    async def notifChannelConfig( self, i: discord.Interaction, channel: discord.TextChannel ):
        with open( "data/channel.txt", 'w', encoding = "UTF-8" ) as f:
            f.write( str( channel.id ) )

        await i.response.send_message( f"통계 알림 채널 설정됨: { channel.name }" )