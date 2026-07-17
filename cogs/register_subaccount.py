import discord, json
from discord.ext.commands import Cog


class RegisterSubaccountCog( Cog ):
    @discord.app_commands.command( name = "부계정_등록", description = "통계를 합산할 부계정을 등록한다" )
    @discord.app_commands.rename( subacc = "부계정" )
    @discord.app_commands.rename( mainacc = "본계정" )
    async def registerSubaccount( self, i: discord.Interaction, subacc: discord.Member, mainacc: discord.Member ):
        accountDict: dict[ str, str ] = {}

        with open( "data/account.json", 'r', encoding = "UTF-8" ) as f:
            accountDict = json.load( f )

        # 부계정이 이미 등록되어 있음
        if accountDict.get( str( subacc.id ) ):
            await i.response.send_message( "부계정이 이미 등록되어 있습니다." )
            return

        # 본계정이 이미 부계정으로서 등록되어 있음
        if accountDict.get( str( mainacc.id ) ):
            await i.response.send_message( "본계정이 다른 계정의 부계정으로서 등록되어 있습니다." )
            return

        accountDict[ str( subacc.id ) ] = str( mainacc.id )

        with open( "data/account.json", 'w', encoding = "UTF-8" ) as f:
            json.dump( accountDict, f, indent = 4 )

        await i.response.send_message( f"{ subacc.display_name }가 { mainacc.display_name }의 부계정으로서 등록되었습니다." )
        


    @discord.app_commands.command( name = "부계정_삭제", description = "등록된 부계정을 삭제한다" )
    @discord.app_commands.rename( subacc = "부계정" )
    async def deleteSubaccount( self, i: discord.Interaction, subacc: discord.Member ):
        accountDict: dict[ str, str ] = {}

        with open( "data/account.json", 'r', encoding = "UTF-8" ) as f:
            accountDict = json.load( f )

        # 부계정이 등록되어 있지 않음
        if not accountDict.get( str( subacc.id ) ):
            await i.response.send_message( "해당 부계정은 등록되어 있지 않습니다." )
            return

        del accountDict[ str( subacc.id ) ]

        with open( "data/account.json", 'w', encoding = "UTF-8" ) as f:
            json.dump( accountDict, f, indent = 4 )

        await i.response.send_message( f"{ subacc.display_name }의 부계정 등록이 해제되었습니다." )