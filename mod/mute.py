import discord
from discord.ext import commands
from utils import utils


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Mute has been loaded.")
        
    
    @commands.command(name="mute", aliases=['m'], description="Mutes a member indefinitely. Reason is optional.", usage=".mute <member> |reason|")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member=None, *, reason=None):
        muted = ctx.guild.get_role(780712672937246731)
        if not member:
            embed1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide the member's username / ID that you want to mute.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed1)
            return
        
        elif not reason:
            reason = "Not specified"

        elif member == ctx.author:
            embed2=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, you can't mute yourself.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed2)
            return
        
        elif ctx.author.top_role.position <= member.top_role.position:
            embed3=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, you can't mute a staff / someone who's higher than you.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed3)
            return
        
        elif muted in member.roles:
            embed4=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, that member is already muted.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed4)
            return


        member.add_roles(muted, reason=f"Responsible Moderator: {ctx.author} (ID: {ctx.author.id}) | Reason: {reason}")

        try:
            embed5=discord.Embed(description=f"Hello **{member.name}**, you have been muted in {ctx.guild.name}. Please abide by the rules next time and respect the members. Thank you!\nYou can see all the server rules by clicking on [this link.](https://discord.com/channels/749099324620669030/749099325098950716/830248577481572383)", color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
            embed5.set_author(name=f"{member.name}, you have been muted.", icon_url=member.avatar_url)
            await member.send(embed=embed5)
            
        except discord.HTTPException:
            pass

        embed6=discord.Embed(description=f'{utils.MEMBERCHAR} **Muted Member:** {member} (ID: {member.id})\n{utils.MODCHAR} **Responsible Moderator:** {ctx.author.mention}\n{utils.REASONCHAR} **Reason:** "{reason}"', color=utils.OKCOLOR, timestamp=utils.TIMESTAMP)
        embed6.set_author(name=f"{utils.OKCHAR} Successfully muted.")
        embed6.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed6)
    
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embederr1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, couldn't find a member.", color=utils.ERRCOLOR)
            await ctx.send(embed=embederr1)
    
    
def setup(bot):
    bot.add_cog(Mute(bot))