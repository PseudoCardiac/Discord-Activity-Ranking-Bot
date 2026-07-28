import discord, json
from discord.ext.commands import Bot, Cog
from utils import rankingToEmbed, statReset


class StatCog( Cog ):
    def __init__( self, bot: Bot ):
        self.bot = bot


    @discord.app_commands.command( name = "통계", description = "통계를 표시한다" )
    async def stat( self, interaction: discord.Interaction ):
        if not interaction.guild:
            return

        await interaction.response.send_message( embeds = rankingToEmbed( self.bot ) )


    @discord.app_commands.command( name = "초기화", description = "모든 기록 파일을 초기화한다" )
    async def statReset( self, interaction: discord.Interaction ):
        with open( "data/prev_ranking.json", 'w' ) as f:
            json.dump( {}, f )

        with open( "data/stat.json", 'w' ) as f:
            json.dump( {}, f )

        with open( "data/stream.json", 'w' ) as f:
            json.dump( {}, f )

        with open( "data/voice.json", 'w' ) as f:
            json.dump( {}, f )
        
        await interaction.response.send_message( "기록 초기화됨" )