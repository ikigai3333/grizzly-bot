import discord
from discord.ext import commands
from utils import utils


class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Unban has been loaded.")

    
    @commands.command(name="unban", aliases=['ub'], description="Unbans a user by their Discord username and tag.", usage=".unban <user> or .ub <user>") # i know this is a very shitty way of unbanning someone, but still works so / wish i could use typing.Union but couldn't figure out how to use it properly
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, *, member=None):
        if not member:
            embed1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide the member's username that you want to unban.\n*If you want to unban with a user ID, please use the `.unbanid` command*", color=utils.ERRCOLOR)
            await ctx.send(embed=embed1)
            return
        

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user, reason=f"Responsible Moderator: {ctx.author} (ID: {ctx.author.id})")

                embed2=discord.Embed(title=f"{utils.OKCHAR} Successfully unbanned.", description=f'{utils.MEMBERCHAR} **Unbanned User:** `{member}`\n{utils.MODCHAR} **Responsible Moderator:** {ctx.author.mention}', color=utils.OKCOLOR, timestamp=utils.TIMESTAMP)
                await ctx.send(embed=embed2)
    
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embederr1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, couldn't find a user in the banned members list.", color=utils.ERRCOLOR)
            await ctx.send(embed=embederr1)

    
def setup(bot):
    bot.add_cog(Unban(bot))