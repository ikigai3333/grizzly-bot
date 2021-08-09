import discord
from discord.ext import commands
from utils import utils


class UnbanID(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"UnbanID has been loaded.")

    
    @commands.command(name="unbanid", aliases=['ubid'], description="Unbans a user by their Discord ID.", usage=".unbanid <id> or .ubid <id>")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unbanid(self, ctx, user: discord.User=None):
        if not user:
            embed1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide the user's ID that you want to unban.\n*If you want to unban with a username, please use the `.unban` command*", color=utils.ERRCOLOR)
            await ctx.send(embed=embed1)
            return


        await ctx.guild.unban(user, reason=f"Responsible Moderator: {ctx.author} (ID: {ctx.author.id})")
        embed2=discord.Embed(description=f'{utils.MEMBERCHAR} **Unbanned User:** {user}\n{utils.MODCHAR} **Responsible Moderator:** {ctx.author.mention}', color=utils.OKCOLOR, timestamp=utils.TIMESTAMP)
        embed2.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed2)

    @unbanid.error
    async def unbanid_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embederr1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, couldn't find a user in the banned members list.", color=utils.ERRCOLOR)
            await ctx.send(embed=embederr1)
        
    
def setup(bot):
    bot.add_cog(UnbanID(bot))