import discord
from discord.ext import commands
from utils import utils


class Color(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Color has been loaded.")

    
    @commands.command(name="color", description="Changes a role's color.", usage=".color <hex color code> <role>")
    @commands.guild_only()
    @commands.has_any_role('mods', 'bot 3000', 'png')
    async def color(self, ctx, color: discord.Color=None, *, role: discord.Role=None):
        if not color:
            embed1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide a color.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed1)
        
        elif not role:
            embed2=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide a role.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed2)

        await role.edit(color=color)
        embed3=discord.Embed(title=f"{utils.OKCHAR} Successfully changed the color.", description=f"Changed **{role}**'s color to `{color}`.\n<-- This embed's color is the role's new color.", color=color, timestamp=utils.TIMESTAMP)
        await ctx.send(embed=embed3)

    @color.error
    async def color_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embederr1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, couldn't find a role or color.", color=utils.ERRCOLOR)
            await ctx.send(embed=embederr1)

    
def setup(bot):
    bot.add_cog(Color(bot))