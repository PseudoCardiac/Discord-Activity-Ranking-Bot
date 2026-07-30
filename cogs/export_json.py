import discord, json
from discord.ext.commands import Cog


class ExportJsonCog( Cog ):
    @discord.app_commands.command( name = "내보내기", description = "JSON 파일을 내보낸다" )
    async def exportJson( self, i: discord.Interaction ):
        with open( "data/stat.json", 'rb' ) as f:
            stat = discord.File( f )

        with open( "data/prev_ranking.json", 'rb' ) as f:
            prevRanking = discord.File( f )

        with open( "data/voice.json", 'rb' ) as f:
            voice = discord.File( f )

        with open( "data/stream.json", 'rb' ) as f:
            stream = discord.File( f )

        await i.response.send_message( files = [ stat, prevRanking, voice, stream ] )