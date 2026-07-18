import discord, os, datetime
from discord.ext import commands
from dotenv import load_dotenv

from cogs import TaskCog, NotifChannelConfigCog, RegisterSubaccountCog
from utils import addNumber, statToEmbed, numChar, recordVoiceJoin, addVoiceTime, recordStreamStart, addStreamTime


INTENTS = discord.Intents.all()
BOT = commands.Bot( command_prefix = "", intents = INTENTS )


@BOT.event
async def on_ready():
    TEST_CHANNEL: discord.TextChannel = BOT.get_channel( 1022402783485370398 )  # type: ignore
    # await BOT.add_cog( TaskCog( BOT, TEST_CHANNEL ), override = True )
    await BOT.add_cog( NotifChannelConfigCog(), override = True )
    await BOT.add_cog( RegisterSubaccountCog(), override = True )

    # await BOT.tree.sync()

    print( "Activity Ranker Currently Running On:" )
    print()
    for guild in BOT.guilds:
        print( f"{ guild.name } ({ str( guild.id ) })" )


@BOT.event
async def on_message( msg: discord.Message ):
    if not msg.guild or msg.guild.id != 1020825427025068123:
        return

    if msg.author.bot:
        return

    if msg.guild is None:
        return

    addNumber( msg.guild.id, msg.author.id, numChar( msg.content ) )

    if msg.content == "통계":
        await msg.reply( embeds = statToEmbed( BOT, msg.guild ) )


@BOT.event
async def on_voice_state_update( member: discord.Member, before: discord.VoiceState, after: discord.VoiceState ):
    if member.guild.id != 1020825427025068123:
        return

    # on member join
    if before.channel is None and after.channel is not None:
        print( f"{ member.display_name } { after.channel.name } 음성 채널에 참가" )
        recordVoiceJoin( str( member.id ) )

    # on member leave
    elif before.channel is not None and after.channel is None:
        print( f"{ member.display_name } { before.channel.name } 음성 채널에서 나감" )
        addVoiceTime( str( member.id ) )

        if before.self_stream or before.self_video:
            addStreamTime( str( member.id ) )

    # on member move
    elif before.channel is not None and after.channel is not None and before.channel != after.channel:
        print( f"{ member.display_name } { before.channel.name } 음성 채널에서 { after.channel.name } 으로 이동" )

    # on member live / video start
    if ( not before.self_stream and not before.self_video ) and ( after.self_stream or after.self_video ) and after.channel:
        print( f"{ member.display_name } { after.channel.name } 음성 채널에서 스트리밍 시작" )
        recordStreamStart( str( member.id ) )

    # on member live / video end
    # WARN: 음성 채널에서 나가면서 스트리밍이 종료된 경우, 이 이벤트가 발생하지 않음
    if ( before.self_stream or before.self_video ) and ( not after.self_stream and not after.self_video ) and before.channel:
        print( f"{ member.display_name } { before.channel.name } 음성 채널에서 스트리밍 종료" )
        addStreamTime( str( member.id ) )


load_dotenv( "../.env" )
BOT.run( os.environ.get( "ACTIVITY_RANKER_TOKEN" ) ) # type: ignore