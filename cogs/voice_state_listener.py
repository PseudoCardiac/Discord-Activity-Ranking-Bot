import discord
from discord.ext.commands import Cog
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import RankingBot

from utils import recordVoiceJoin, addVoiceTime, recordStreamStart, addStreamTime


class VoiceStateListener( Cog ):
    def __init__( self, rankingBot: "RankingBot" ):
        self.rankingBot = rankingBot


    @Cog.listener( name = "on_voice_state_update" )
    async def on_voice_state_update( self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState ):
        if member.guild.id != 1020825427025068123:
            return

        # on member join
        if ( before.channel is None and after.channel is not None ) and not after.afk and not member.bot:
            # print( f"{ member.display_name } { after.channel.name } 음성 채널에 참가" )
            recordVoiceJoin( str( member.id ) )

        # on member leave
        elif ( before.channel is not None and after.channel is None ) and not before.afk and not member.bot:
            # print( f"{ member.display_name } { before.channel.name } 음성 채널에서 나감" )
            addVoiceTime( str( member.id ) )

            if before.self_stream or before.self_video:
                addStreamTime( str( member.id ) )

        # on member move
        elif before.channel is not None and after.channel is not None and before.channel != after.channel:
            # print( f"{ member.display_name } { before.channel.name } 음성 채널에서 { after.channel.name } 으로 이동" )
            # from afk to non-afk
            if before.afk and not after.afk:
                recordVoiceJoin( str( member.id ) )

            # from non-afk to afk
            elif not before.afk and after.afk:
                addVoiceTime( str( member.id ) )

                if before.self_stream or before.self_video:
                    addStreamTime( str( member.id ) )

        # on member live / video start
        if ( not before.self_stream and not before.self_video ) and ( after.self_stream or after.self_video ) and after.channel and not member.bot:
            # print( f"{ member.display_name } { after.channel.name } 음성 채널에서 스트리밍 시작" )
            recordStreamStart( str( member.id ) )

        # on member live / video end
        # WARN: 음성 채널에서 나가면서 스트리밍이 종료된 경우, 이 이벤트가 발생하지 않음
        if ( before.self_stream or before.self_video ) and ( not after.self_stream and not after.self_video ) and before.channel and not member.bot:
            # print( f"{ member.display_name } { before.channel.name } 음성 채널에서 스트리밍 종료" )
            addStreamTime( str( member.id ) )