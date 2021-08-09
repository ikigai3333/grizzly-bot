import discord
from discord.ext import commands
from utils import utils


class ModVerify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"ModVerify has been loaded.")

    
    @commands.command(name="modverify", description="Verifies a member if they're not verified in the server.", usage=".modverify <member>")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def modverify(self, ctx, member: discord.Member=None):
        quarantine = ctx.guild.get_role(870895060651225118)
        verified = ctx.guild.get_role(749099324620669031)

        if not member:
            await ctx.reply(f"{utils.ERRCHAR} verify who?", delete_after=10.0)
            await ctx.message.delete()
            return
        
        if verified in member.roles:
            await ctx.reply(f"{utils.ERRCHAR} that member is already verified.", delete_after=10.0)
            await ctx.message.delete()
            return 
        
        else:
            await member.remove_roles(quarantine)
            await member.add_roles(verified)
            await ctx.send(f"{utils.OKCHAR} verified **{member}**.", delete_after=10.0)
            await ctx.message.delete()
    
    @modverify.error
    async def modverify_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{utils.ERRCHAR} couldn't find a member.", delete_after=10.0)
        
        
def setup(bot):
    bot.add_cog(ModVerify(bot))