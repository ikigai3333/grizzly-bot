import grizzly 
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.grizzly = grizzly.Grizzly(bot=self.bot)

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help cog has been loaded.')
    

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def help(self, ctx):
        await self.grizzly.help_main(ctx)
    

    @help.command()
    @commands.guild_only()
    async def avatar(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='avatar')
    
    @help.command()
    @commands.guild_only()
    async def banner(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='banner')

    @help.command()
    @commands.guild_only()
    async def translate(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='translate')

    @help.command()
    @commands.guild_only()
    async def bored(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='bored')

    @help.command()
    @commands.guild_only()
    async def genderize(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='genderize')

    @help.command()
    @commands.guild_only()
    async def ping(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='ping')
    
    @help.command()
    @commands.guild_only()
    async def roll(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='roll')
    
    @help.command()
    @commands.guild_only()
    async def miku(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='miku')
    
    @help.command()
    @commands.guild_only()
    async def cat(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='cat')
    
    @help.command()
    @commands.guild_only()
    async def dog(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='dog')
    
    @help.command()
    @commands.guild_only()
    async def panda(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='panda')
        
    @help.command()
    @commands.guild_only()
    async def duck(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='duck')
    

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def modhelp(self, ctx):
        await self.grizzly.help_mod(ctx)
    

    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def ban(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='ban')

    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def unban(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='unban')
    
    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def unbanid(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='unbanid')
    
    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='kick')
    
    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def warn(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='warn')
    
    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def mute(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='mute')
    
    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def unmute(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='unmute')
    
    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def muted(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='muted')
    
    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def purge(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='purge')

    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def color(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='color')
    
    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def snipe(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='snipe')
    
    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def esnipe(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='esnipe')
    
    @modhelp.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def userinfo(self, ctx):
        await self.grizzly.help_embeds(ctx=ctx, command='userinfo')

def setup(bot):
    bot.add_cog(Help(bot))