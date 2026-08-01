import discord, os
from discord.ext.commands import Bot

from dotenv import load_dotenv

from cogs import TaskCog, NotifChannelConfigCog, RegisterSubaccountCog, StatCog, ReorderRolesCog, ExportJsonCog, VoiceStateListener
from utils import addNumber, numChar


class RankingBot( Bot ):
    def __init__( self ):
        super().__init__( command_prefix = "@RankingBot", intents = discord.Intents.all() )


    async def on_ready( self ):
        with open( "data/channel.txt", 'r', encoding = "UTF-8" ) as f:
            notifChannelId = int( f.read() )
        NOTIF_CHANNEL: discord.TextChannel = self.get_channel( notifChannelId )  # type: ignore
        await self.add_cog( TaskCog( self, NOTIF_CHANNEL ), override = True )
        await self.add_cog( NotifChannelConfigCog(), override = True )
        await self.add_cog( RegisterSubaccountCog(), override = True )
        await self.add_cog( StatCog( self ), override = True  )
        await self.add_cog( ReorderRolesCog( self ), override = True )
        await self.add_cog( ExportJsonCog( self ), override = True )
        await self.add_cog( VoiceStateListener( self ), override = True )

        # await self.tree.sync()

        print( "Activity Ranker" )


    async def on_message( self, msg: discord.Message ):
        if not msg.guild or msg.guild.id != 1020825427025068123:
            return

        if msg.author.bot:
            return

        addNumber( msg.guild.id, msg.author.id, numChar( msg.content ) )


    def runBot( self ):
        load_dotenv( "../.env" )
        self.run( os.environ.get( "ACTIVITY_RANKER_TOKEN" ) ) # type: ignore


RANKING_BOT = RankingBot()