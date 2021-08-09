import discord
from discord.ext import commands
from utils import utils


class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Purge has been loaded.")


    @commands.command(name="purge", aliases=['p'], description="Purges a specific amount of messages.", usage=".purge <amount> or .p <amount>")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int=None):
        if not amount:
            embed1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide an amount of messages to purge.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed1)
            return
        
        elif amount > 100:
            embed2=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, you can't purge more than 100 messages.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed2)
            return

        else:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f'{utils.OKCHAR} Successfully purged `{amount}` messages.', delete_after=10.0)
    
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embederr1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide a correct amount.", color=utils.ERRCOLOR)
            await ctx.send(embed=embederr1)

        
def setup(bot):
    bot.add_cog(Purge(bot))