import discord
import datetime
import platform
import psutil
import jishaku

from discord.ext import commands
from utils import utils
from typing import Union


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Dev has been loaded.")

    
    # developer commands
    @commands.group(invoke_without_command=True, hidden=True)
    @commands.is_owner()
    async def dev(self, ctx):
        embed = discord.Embed(description=f"written in python! made by `{ctx.author}` ♡", color=utils.GCOLOR)
        embed.set_author(name="developer commands :3", url="https://github.com/ikigai3333/grizzly-bot", icon_url=self.bot.user.avatar_url)
        embed.add_field(name="cogs", value="load, unload, reload, listcogs, listcmds", inline=False)
        embed.add_field(name="moderation", value="ban, kick, purge, color", inline=False)
        embed.add_field(name="misc", value="info, source, nick", inline=False)
        await ctx.send(embed=embed)
    

    # moderation
    @dev.command()
    async def ban(self, ctx, member: Union[discord.Member, discord.User]=None, *, reason=None):
        if not member:
            await ctx.reply('ban who', delete_after=5.0)
            return
        elif not reason:
            await ctx.reply('reason?', delete_after=5.0)
            return 
        elif member == ctx.author:
            await ctx.reply(f'dumbo', delete_after=5.0)
            return 
        
        try:
            await ctx.guild.ban(member, reason=f"by edgy!! | reason: {reason}")
            await ctx.send('👍', delete_after=5.0)
        except Exception as e:
            await ctx.send(e, delete_after=5.0)

    @dev.command()
    async def kick(self, ctx, member: discord.Member=None, *, reason=None):
        if not member:
            await ctx.reply('kick who', delete_after=5.0)
            return
        elif not reason:
            await ctx.reply('reason?', delete_after=5.0)
            return 
        elif member == ctx.author:
            await ctx.reply(f'dumbo', delete_after=5.0)
            return
        
        try:
            await member.kick(reason=f"by edgy! | reason: {reason}")
            await ctx.send('👍', delete_after=5.0)
        except Exception as e:
            await ctx.send(e, delete_after=5.0)

    @dev.command()
    async def purge(self, ctx, amount: int):
        if amount > 100:
            await ctx.reply("can't purge more than 100 messages", delete_after=5.0)
            return

        try:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f'purged {amount} messages 👍', delete_after=5.0)
        except Exception as e:
            await ctx.send(e, delete_after=5.0)

    @dev.command()
    async def color(self, ctx, color: discord.Color=None, *, role: discord.Role=None):
        if not color:
            await ctx.send("what color", delete_after=5.0)
            return 
        elif not role:
            await ctx.send("which role", delete_after=5.0)
            return 

        try:
            await role.edit(color=color)
            await ctx.send('👍', delete_after=5.0)
        except Exception as e:
            await ctx.send(e, delete_after=5.0)


    # cogs
    @dev.command()
    async def load(self, ctx, extension):
        self.bot.load_extension(extension)
        print(f'{extension} has been successfully loaded.')
        await ctx.send(f'**{extension}** cog has been successfully loaded.')
    
    @dev.command()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(extension)
        print(f'{extension} has been successfully unloaded.')
        await ctx.send(f'**{extension}** cog has been successfully unloaded.')

    @dev.command()
    async def reload(self, ctx, extension):
        self.bot.reload_extension(extension)
        print(f'{extension} has been successfully reloaded.')
        await ctx.send(f'**{extension}** cog has been successfully reloaded.')

    @dev.command()
    async def listcogs(self, ctx):
        embed1=discord.Embed(description=f'currently have `{len(self.bot.cogs)}` cogs!\n\u200b\n{chr(10).join(map(str, [cog for cog in self.bot.cogs]))}', color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
        embed1.set_author(name="all cogs :3", icon_url=self.bot.user.avatar_url)
        embed1.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed1)

    @dev.command()
    async def listcmds(self, ctx):
        embed2=discord.Embed(description=f'currently have `{len(self.bot.commands)}` commands!\n\u200b\n{chr(10).join(map(str, [cmd for cmd in self.bot.commands]))}', color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
        embed2.set_author(name="all commands :3", icon_url=self.bot.user.avatar_url)
        embed2.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed2)
        
        
    # misc
    @dev.command()
    async def info(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time  # i got this time thingy from someone's answer on stackoverflow so ty that person
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        botinfo = f"""
        Written by `{ctx.author}` with only `1.373` lines! ♡
        Grizzly's current version is `{self.bot.version}`.

        **__bot stuff__**
        Grizzly is currently in `{len(self.bot.guilds)}` servers.
        Grizzly can currently see `{len(self.bot.users)}` users.
        Grizzly currently has the `Member` and `Presence` intents enabled.
        Grizzly currently has `{len(self.bot.cogs)}` different cogs.
        Grizzly currently has `{len(self.bot.commands)}` different commands.

        **__server-side stuff__**
        Grizzly is currently running on OS `{platform.system()} {platform.release()}`.
        Grizzly currently has `%{psutil.cpu_percent()}` of CPU and `%{psutil.virtual_memory()[2]}` of RAM usage.
        Grizzly's current websocket latency is `{round(self.bot.latency * 1000)}ms`.
        Grizzly's uptime: `{days}` days, `{hours}` hrs, `{minutes}` mins and `{seconds}` secs.

        **__other stuff__**
        Grizzly is running on [Python](https://www.python.org) version `{platform.python_version()}`.
        Grizzly is running on [discord.py](https://github.com/Rapptz/discord.py) version `{discord.__version__}`.
        Grizzly is running on [jishaku](https://github.com/Gorialis/jishaku) version `{jishaku.__version__}`.
        Grizzly's used APIs can be found [here.](https://github.com/ikigai3333/grizzly-bot/blob/main/apis.txt)
        Grizzly's source code can be found [here.](https://github.com/ikigai3333/grizzly-bot)
        """
        embed3=discord.Embed(description=botinfo, color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
        embed3.set_author(name="bot info :3", url="https://github.com/ikigai3333/grizzly-bot", icon_url=self.bot.user.avatar_url)
        embed3.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed3)

    @dev.command()
    async def nick(self, ctx, *, nick=None):
        try:
            await ctx.me.edit(nick=nick)
            await ctx.send('👍', delete_after=5.0)
        except Exception as e:
            await ctx.send(e, delete_after=5.0)

    @dev.command()
    async def source(self, ctx):
        await ctx.send("https://github.com/ikigai3333/grizzly-bot lol")

    
def setup(bot):
    bot.add_cog(Dev(bot))