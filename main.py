import discord, os, datetime
from discord.ext import commands
from dotenv import load_dotenv

from cogs import TaskCog, NotifChannelConfigCog, RegisterSubaccountCog
from utils import addNumber, statToEmbed, numChar


INTENTS = discord.Intents.all()
BOT = commands.Bot( command_prefix = "", intents = INTENTS )


@BOT.event
async def on_ready():
    TEST_CHANNEL: discord.TextChannel = BOT.get_channel( 1022402783485370398 )  # type: ignore
    # await BOT.add_cog( TaskCog( BOT, TEST_CHANNEL ), override = True )
    await BOT.add_cog( NotifChannelConfigCog(), override = True )
    await BOT.add_cog( RegisterSubaccountCog(), override = True )

    await BOT.tree.sync()

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

    addNumber( msg.guild.id, msg.author.id, numChar( msg.content ) )

    if msg.content == "통계":
        await msg.reply( embeds = statToEmbed( BOT, msg.guild ) )


load_dotenv( "../.env" )
BOT.run( os.environ.get( "ACTIVITY_RANKER_TOKEN" ) ) # type: ignore