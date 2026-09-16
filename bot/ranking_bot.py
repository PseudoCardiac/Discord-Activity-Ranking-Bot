import discord, os, asyncio, tracemalloc
from discord.ext.commands import Bot

from dotenv import load_dotenv

from cogs import TaskCog, NotifChannelConfigCog, RegisterSubaccountCog, StatCog, ReorderRolesCog, ExportJsonCog, VoiceStateListener
from utils import addNumber, numChar


tracemalloc.start()


class RankingBot( Bot ):
    def __init__( self ):
        super().__init__( command_prefix = "@RankingBot", intents = discord.Intents.all() )


    async def setup_hook( self ):
        with open( "data/channel.txt", 'r', encoding = "UTF-8" ) as f:
            notifChannelId = int( f.read() )

        NOTIF_CHANNEL: discord.TextChannel = await self.fetch_channel( notifChannelId ) # type: ignore
        self.MHD: discord.Guild = await self.fetch_guild( 1020825427025068123 )   # type: ignore
        self.PIVOT_ROLE = await self.MHD.fetch_role( 1527271285103792263 )
        self.SCY = await self.fetch_user( 513676568745213953 )

        await self.add_cog( TaskCog( self, NOTIF_CHANNEL ), override = True )
        await self.add_cog( NotifChannelConfigCog(), override = True )
        await self.add_cog( RegisterSubaccountCog(), override = True )
        await self.add_cog( StatCog( self ), override = True  )
        await self.add_cog( ReorderRolesCog( self ), override = True )
        await self.add_cog( ExportJsonCog( self ), override = True )
        await self.add_cog( VoiceStateListener( self ), override = True )

        # await self.tree.sync()

        self.memoryTask = asyncio.create_task( self.memorySnapshotTask() )


    async def memorySnapshotTask( self ):
        snapshot1 = None

        while True:
            try:
                snapshot2 = tracemalloc.take_snapshot()

                if snapshot1:
                    top_stats = snapshot2.compare_to( snapshot1, 'lineno' )
                    await self.SCY.send( "[ 메모리 증가 Top 10 ]" )

                    for stat in top_stats[:10]:
                        await self.SCY.send( str( stat ) )

                else:
                    await self.SCY.send( "메모리 모니터링 개시" )

                snapshot1 = snapshot2

            except Exception as e:
                await self.SCY.send( f"Error: {e}" )

            await asyncio.sleep( 3600 )


    async def on_ready( self ):
        print( "Activity Ranker" )


    async def on_message( self, msg: discord.Message ):
        if not msg.guild or msg.guild.id != 1020825427025068123:
            return

        if msg.author.bot:
            return

        if msg.channel.type == discord.ChannelType.voice:
            return

        addNumber( msg.guild.id, msg.author.id, numChar( msg.content ) )


    def runBot( self ):
        load_dotenv( "../.env" )
        self.run( os.environ.get( "ACTIVITY_RANKER_TOKEN" ) ) # type: ignore


RANKING_BOT = RankingBot()