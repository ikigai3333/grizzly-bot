import discord
from discord.ext import commands
from utils import utils


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Kick has been loaded.")
        
    
    @commands.command(name="kick", aliases=['k'], description="Kicks a member and sends them a DM with the reason.", usage=".kick <member> <reason>")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, *, reason=None):

        if not member:
            embed1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide the member's username / ID that you want to kick.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed1)
            return
        
        elif not reason:
            embed2=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide a reason.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed2)
            return 
        
        elif member == ctx.author:
            embed3=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, you can't kick yourself.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed3)
            return
        
        elif ctx.author.top_role.position <= member.top_role.position:
            embed4=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, you can't kick a staff / someone who's higher than you.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed4)
            return
        
        try:
            embed5=discord.Embed(title=f"{member.name}, you have been kicked from {ctx.guild.name}.", description=f"Hello **{member.name}**, you have been kicked from {ctx.guild.name}. Please abide by the rules next time!", color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
            embed5.set_author(name=member, icon_url=member.avatar_url)
            embed5.set_thumbnail(url=member.avatar_url)
            embed5.add_field(name="Reasoning for Kick", value=reason, inline=False)
            embed5.set_footer(text=self.bot.user.name, icon_url=utils.ICON)
            await member.send(embed=embed5)
        
        except discord.HTTPException:
            pass 

        await member.kick(reason=f"Responsible Moderator: {ctx.author} (ID: {ctx.author.id}) | Reason: {reason}")

        embed6=discord.Embed(description=f'{utils.MEMBERCHAR} **Kicked Member:** {member} (ID: {member.id})\n{utils.MODCHAR} **Responsible Moderator:** {ctx.author.mention}\n{utils.REASONCHAR} **Reason:** "{reason}"', color=utils.OKCOLOR, timestamp=utils.TIMESTAMP)
        embed6.set_author(name=f"{utils.OKCHAR} Successfully kicked.")
        embed6.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed6)

        channel = self.bot.get_channel(831278012199862312)
        await channel.send(embed=embed6)
    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embederr1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, couldn't find a member.", color=utils.ERRCOLOR)
            await ctx.send(embed=embederr1)
    
    
def setup(bot):
    bot.add_cog(Kick(bot))