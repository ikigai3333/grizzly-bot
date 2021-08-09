import discord
from discord.ext import commands
from utils import utils


class Muted(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Muted has been loaded.")

    
    @commands.command(name="muted", description="A list of all the muted members in the server.", usage=".muted")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def muted(self, ctx):
        muted = ctx.guild.get_role(780712672937246731)

        if len(muted.members) > 0:
            embed1=discord.Embed(title="Muted Members", description=f"Currently have **{len(muted.members)}** muted members.\n\u200b\n{chr(10).join(map(str, muted.members))}", color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
            await ctx.send(embed=embed1)

        else:
            embed2=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, no one is currently muted.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed2)
        
    
def setup(bot):
    bot.add_cog(Muted(bot))