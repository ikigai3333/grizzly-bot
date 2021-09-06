import discord
import typing
import grizzly
import utils

from discord.ext import commands 


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.grizzly = grizzly.Grizzly(bot=self.bot)

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Dev cog has been loaded.')
    

    @commands.group(aliases=['developer'], invoke_without_command=True)
    @commands.is_owner()
    async def dev(self, ctx):
        await self.grizzly.dev_help(ctx)

    @dev.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.bot.load_extension(extension)
        res = f'{extension} has been successfully loaded.'
        print(res)
        await ctx.send(res)
    
    @dev.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(extension)
        res = f'{extension} has been successfully unloaded.'
        print(res)
        await ctx.send(res)
    
    @dev.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.bot.reload_extension(extension)
        res = f'{extension} has been successfully reloaded.'
        print(res)
        await ctx.send(res)
    
    @dev.command()
    @commands.is_owner()
    async def reloadall(self, ctx):
        for cog in self.bot.cogs:
            self.bot.reload_extension(cog)
        res = 'reloaded all the cogs.'
        print(res)
        await ctx.send(res)
    
    @dev.command()
    @commands.is_owner()
    async def listcogs(self, ctx):
        await self.grizzly.dev_listcogs(ctx)
    
    @dev.command(aliases=['listcmds'])
    @commands.is_owner()
    async def listcommands(self, ctx):
        await self.grizzly.dev_listcmds(ctx)
    
    @dev.command()
    @commands.is_owner()
    async def botinfo(self, ctx):
        await self.grizzly.dev_botinfo(ctx)
    
    @dev.command()
    @commands.is_owner()
    async def rawuserinfo(self, ctx, member: typing.Union[discord.Member, discord.User]=None):
        if not member:
            member = ctx.author

        authorization = f'Bot {utils.GRIZZTOKEN}'
        headerss = {
            "Authorization": authorization
        }
        data = await self.grizzly.botsession(url=f'https://discord.com/api/v9/users/{member.id}', headers=headerss)
        await self.grizzly.dev_rawuserinfo(ctx=ctx, data=data)
       
    @dev.command()
    @commands.is_owner()
    async def nick(self, ctx, *, nick=None):
        try:
            await ctx.me.edit(nick=nick)
            await ctx.send('👍', delete_after=5.0)
        except Exception as e:
            await ctx.send(e, delete_after=5.0)

    @dev.command()
    @commands.is_owner()
    async def source(self, ctx):
        await ctx.send('https://github.com/ikigai3333/grizzly-bot lol')
    
def setup(bot):
    bot.add_cog(Dev(bot))