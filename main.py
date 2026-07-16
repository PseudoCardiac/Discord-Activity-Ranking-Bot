import discord, os, datetime
from discord.ext import tasks, commands
from dotenv import load_dotenv

from cogs.task import TaskCog
from cogs.notif_channel_config import NotifChannelConfigCog
from utils.add_number import addNumber
from utils.stat_to_embed import statToEmbed
from utils.num_char import numChar


INTENTS = discord.Intents.all()
BOT = commands.Bot( command_prefix = "", intents = INTENTS )


@BOT.event
async def on_ready():
    TEST_CHANNEL: discord.TextChannel = BOT.get_channel( 1022402783485370398 )  # type: ignore
    await BOT.add_cog( TaskCog( BOT, TEST_CHANNEL ), override = True )
    await BOT.add_cog( NotifChannelConfigCog(), override = True )

    print( "Activity Ranker Currently Running On:" )
    print()
    for guild in BOT.guilds:
        print( f"{ guild.name } ({ str( guild.id ) })" )


@BOT.event
async def on_message( msg: discord.Message ):
    if msg.author.bot:
        return

    if msg.guild is None:
        return

    print( msg.content )
    
    addNumber( msg.guild.id, msg.author.id, numChar( msg.content ) )

    if msg.content == "통계":
        await msg.reply( embed = statToEmbed( BOT, msg.guild ) )


load_dotenv( "../.env" )
BOT.run( os.environ.get( "ACTIVITY_RANKER_TOKEN" ) ) # type: ignore