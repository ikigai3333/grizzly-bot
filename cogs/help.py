from os import name
import discord
from discord.ext import commands
from utils import utils 


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Help has been loaded.")

    async def embed_generate(self, ctx, command): # wish i did this sooner for all commands so my everything would be more simple and looked clean / who cares lol maybe next time if i rewrite this bot
        getcmd = self.bot.get_command(command)
        if getcmd.aliases:
            alias = f"({''.join(getcmd.aliases)})"
        else:
            alias = ""
        embed=discord.Embed(description=f"{getcmd.description}\n**Usage:** {getcmd.usage}", color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
        embed.set_author(name=f"{getcmd.name} {alias}", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)



    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def help(self, ctx):
        embed1=discord.Embed(description="All the available commands for Grizzly.\nTo see more info about a specific command, use the command `.help <command>`.", color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
        embed1.set_author(name=f"{self.bot.user.name} Help", url="https://github.com/ikigai3333/grizzly-bot", icon_url=self.bot.user.avatar_url)
        embed1.set_thumbnail(url=self.bot.user.avatar_url)
        embed1.add_field(name="Fun commands", value="avatar, userinfo, translate, bored, genderize, ping, roll", inline=False)
        embed1.add_field(name="Random image commands", value="miku, cat, dog, panda, duck", inline=False)
        embed1.set_footer(text="if you're a staff, see the .modhelp command!")
        await ctx.send(embed=embed1)
    

    @help.command()
    async def avatar(self, ctx):
        await self.embed_generate(ctx, 'avatar')
    @help.command()
    async def userinfo(self, ctx):
        await self.embed_generate(ctx, 'userinfo')
    @help.command()
    async def translate(self, ctx):
         await self.embed_generate(ctx, 'translate')
    @help.command()
    async def bored(self, ctx):
        await self.embed_generate(ctx, 'bored')
    @help.command()
    async def genderize(self, ctx):
        await self.embed_generate(ctx, 'genderize')
    @help.command()
    async def ping(self, ctx):
        await self.embed_generate(ctx, 'ping')
    @help.command()
    async def roll(self, ctx):
        await self.embed_generate(ctx, 'roll')
    @help.command()
    async def miku(self, ctx):
        await self.embed_generate(ctx, 'miku')
    @help.command()
    async def cat(self, ctx):
        await self.embed_generate(ctx, 'cat')
    @help.command()
    async def dog(self, ctx):
        await self.embed_generate(ctx, 'dog')
    @help.command()
    async def panda(self, ctx):
        await self.embed_generate(ctx, 'panda')
    @help.command()
    async def duck(self, ctx):
        await self.embed_generate(ctx, 'duck')

    
    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_any_role('mods', 'bot 3000', 'png')
    async def modhelp(self, ctx):
        embed2=discord.Embed(description="All the available staff-only commands for Grizzly.\nTo see more info about a specific command, use the command `.modhelp <command>`.", color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
        embed2.set_author(name=f"{self.bot.user.name} Moderation Help", url="https://github.com/ikigai3333/grizzly-bot", icon_url=self.bot.user.avatar_url)
        embed2.set_thumbnail(url=self.bot.user.avatar_url)
        embed2.add_field(name="Commands list", value="ban, unban, unbanid, kick, warn, mute, muted, unmute, purge, modverify, color")
        embed2.set_footer(text="All staff members bypass all cooldowns!")
        await ctx.send(embed=embed2)
    

    @modhelp.command()
    async def ban(self, ctx):
        await self.embed_generate(ctx, 'ban')
    @modhelp.command()
    async def unban(self, ctx):
        await self.embed_generate(ctx, 'unban')
    @modhelp.command()
    async def unbanid(self, ctx):
        await self.embed_generate(ctx, 'unbanid')
    @modhelp.command()
    async def kick(self, ctx):
        await self.embed_generate(ctx, 'kick')
    @modhelp.command()
    async def warn(self, ctx):
        await self.embed_generate(ctx, 'warn')
    @modhelp.command()
    async def mute(self, ctx):
        await self.embed_generate(ctx, 'mute')
    @modhelp.command()
    async def muted(self, ctx):
        await self.embed_generate(ctx, 'muted')
    @modhelp.command()
    async def unmute(self, ctx):
        await self.embed_generate(ctx, 'unmute')
    @modhelp.command()
    async def purge(self, ctx):
        await self.embed_generate(ctx, 'purge')
    @modhelp.command()
    async def modverify(self, ctx):
        await self.embed_generate(ctx, 'modverify')
    @modhelp.command()
    async def color(self, ctx):
        await self.embed_generate(ctx, 'color')
    
    
def setup(bot):
    bot.add_cog(Help(bot))