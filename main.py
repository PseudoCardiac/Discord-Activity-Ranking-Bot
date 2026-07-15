import discord, os, datetime
from discord.ext import tasks, commands
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

from task import TaskCog


INTENTS = discord.Intents.all()
BOT = commands.Bot( command_prefix = "", intents = INTENTS )


@BOT.event
async def on_ready():
    TEST_CHANNEL: discord.TextChannel = BOT.get_channel( 1022402783485370398 )  # type: ignore
    await BOT.add_cog( TaskCog( BOT, TEST_CHANNEL ), override = True )

    print( "Activity Ranker Currently Running On:" )
    print()
    for guild in BOT.guilds:
        print( f"{ guild.name } ({ str( guild.id ) })" )


@BOT.event
async def on_message( msg: discord.Message ):
    print( f"{ msg.author }: { len( msg.content ) } characters" )


load_dotenv( "../.env" )
BOT.run( os.environ.get( "ACTIVITY_RANKER_TOKEN" ) ) # type: ignore