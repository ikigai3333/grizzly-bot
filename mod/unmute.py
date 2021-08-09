import discord
from discord.ext import commands
from utils import utils


class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Unmute has been loaded.")
        
    
    @commands.command(name="unmute", aliases=['um'], description="Unmutes a member.", usage=".unmute <member> or .um <member>")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member=None):
        muted = ctx.guild.get_role(780712672937246731)

        if not member: 
            embed1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide the member's username / ID that you want to unmute.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed1)
            return
        elif muted not in member.roles:
            embed2=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, that member is already not muted.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed2)
            return
        
        else:
            member.remove_roles(muted)
            embed3=discord.Embed(description=f'{utils.MEMBERCHAR} **Unmuted Member:** {member} (ID: {member.id})\n{utils.MODCHAR} **Responsible Moderator:** {ctx.author.mention}', color=utils.OKCOLOR, timestamp=utils.TIMESTAMP)
            embed3.set_author(name=f"{utils.OKCHAR} Successfully unmuted.")
            embed3.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed3)
        
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embederr1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, couldn't find a member.", color=utils.ERRCOLOR)
            await ctx.send(embed=embederr1)
    
    
def setup(bot):
    bot.add_cog(Unmute(bot))