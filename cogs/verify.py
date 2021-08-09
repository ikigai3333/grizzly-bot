import discord
from discord.ext import commands 


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Verify has been loaded.")
        
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        quarantine = guild.get_role(870895060651225118)
        await member.add_roles(quarantine)

    
    @commands.command()
    async def grizzly(self, ctx):
        quarantine = ctx.guild.get_role(870895060651225118)
        verified = ctx.guild.get_role(749099324620669031)
        if ctx.channel.id != 870827254857478164:
            return 
        await ctx.author.remove_roles(quarantine)
        await ctx.author.add_roles(verified)
        await ctx.message.delete()
    
    
def setup(bot):
    bot.add_cog(Verify(bot))