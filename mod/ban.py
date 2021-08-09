import discord
from discord.ext import commands
from utils import utils


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Ban has been loaded.")

    
    @commands.command(name="ban", aliases=['b'], description="Bans a member and sends them a DM with the reason and the ban appeal link.", usage=".ban <member> <reason>")
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, *, reason=None):
        if not member:
            embed1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide the member's username / ID that you want to ban.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed1)
            return

        elif not reason:
            embed2=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide a reason.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed2)
            return 
        
        elif member == ctx.author:
            embed3=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, you can't ban yourself.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed3)
            return
        
        elif ctx.author.top_role.position <= member.top_role.position:
            embed4=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, you can't ban a staff / someone who's higher than you.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed4)
            return

        try:
            embed5=discord.Embed(title=f"{member.name}, you have been banned from {ctx.guild.name}.", description=f"Hello **{member.name}**, you are able to appeal your ban after 3-7 days using the Ban Appeal form by using the link below (if you believe you were wrongfully banned).", color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
            embed5.set_author(name=member, icon_url=member.avatar_url)
            embed5.add_field(name="Reasoning for Ban", value=reason, inline=False)
            embed5.add_field(name="Ban Appeal Form", value="[Click Here](https://forms.gle/i8PE2uAYQMJwEYeUA)", inline=False)
            embed5.set_thumbnail(url=member.avatar_url)
            embed5.set_image(url=utils.IMAGE)
            embed5.set_footer(text=self.bot.user.name, icon_url=utils.ICON)
            await member.send(embed=embed5)

        except discord.HTTPException:
            pass

        await member.ban(reason=f"Responsible Moderator: {ctx.author} (ID: {ctx.author.id}) | Reason: {reason}")

        embed6=discord.Embed(description=f'{utils.MEMBERCHAR} **Banned Member:** {member} (ID: {member.id})\n{utils.MODCHAR} **Responsible Moderator:** {ctx.author.mention}\n{utils.REASONCHAR} **Reason:** "{reason}"', color=utils.OKCOLOR, timestamp=utils.TIMESTAMP)
        embed6.set_author(name=f"{utils.OKCHAR} Successfully banned.")
        embed6.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed6)

        channel = self.bot.get_channel(831278012199862312)
        await channel.send(embed=embed6)
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embederr1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, couldn't find a member.", color=utils.ERRCOLOR)
            await ctx.send(embed=embederr1)

    
def setup(bot):
    bot.add_cog(Ban(bot))