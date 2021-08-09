import discord
import asyncio
import random
import googletrans

from discord.ext import commands
from utils import utils
from typing import Union


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trans = googletrans.Translator()
        self.whitelist = ['mods', 'bot 3000', 'png'] 
    
    # listeners
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Misc has been loaded.")


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        self.bot.sniped_messages[message.guild.id, message.channel.id] = (message.content, message.author, message.created_at)
        await asyncio.sleep(180)
        try:
            del self.bot.sniped_messages[message.guild.id, message.channel.id]
        except KeyError:
            pass
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return
        self.bot.edited_messages[after.guild.id, after.channel.id] = (before.content, after.content, after.author)
        await asyncio.sleep(180)
        try:
            del self.bot.edited_messages[after.guild.id, after.channel.id]
        except KeyError:
            pass

    # commands
    @commands.command(name="avatar", aliases=['av'], description="Shows a user's avatar. If they're not in the server, you can use their Discord ID.", usage=".avatar <user> or .av <user>")
    @commands.guild_only()
    async def avatar(self, ctx, member: Union[discord.Member, discord.User]=None):
        if not member:
            member = ctx.author
        
        embed1=discord.Embed(color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
        embed1.set_author(name=member, icon_url=member.avatar_url)
        embed1.set_image(url=member.avatar_url)
        await ctx.send(embed=embed1)
    

    @commands.command(name="userinfo", aliases=['whois'], description="Shows info about the member.", usage=".userinfo <member> or .whois <member>")
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author

        # role stuff
        roles = [role for role in member.roles[1:]]
        roles.reverse()
        rolecount = len(roles)
        
        # joined stuff
        membercreatedat = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p")
        memberjoinedat = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p")

        # permission stuff (ty danny for this)
        permslist = []
        perms = ctx.channel.permissions_for(member)
        for name, value in perms:
            name = name.replace("_", " ").replace("guild", "server").title()
            if value:
                permslist.append(name)


        embed2=discord.Embed(description=member.mention, color=member.color, timestamp=utils.TIMESTAMP)
        embed2.set_author(name=member, icon_url=member.avatar_url)
        embed2.set_thumbnail(url=member.avatar_url)
        embed2.add_field(name="ID", value=member.id,)
        embed2.add_field(name="Color", value=member.color)
        embed2.add_field(name="Server Joined At", value=memberjoinedat, inline=False)
        embed2.add_field(name="Account Created At", value=membercreatedat, inline=False)
        if rolecount > 0:
            embed2.add_field(name=f"Roles ({rolecount})", value=", ".join(([role.mention for role in roles])), inline=False)
        else:
            embed2.add_field(name="Roles", value="This member currently has no roles.", inline=False)
        embed2.add_field(name="Permissions", value=", ".join(permslist), inline=False)
        await ctx.send(embed=embed2)


    @commands.command(name="translate", description="Translates the message to English.", usage=".translate")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def translate(self, ctx, *, message=None):
        if not message:
            embed7=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide a message to translate!", color=utils.ERRCOLOR)
            await ctx.send(embed=embed7)
            return
        
        loop = self.bot.loop
        ret = await loop.run_in_executor(None, self.trans.translate, message)
        src = googletrans.LANGUAGES.get(ret.src, '(auto-detected)').title()
        dest = googletrans.LANGUAGES.get(ret.dest, 'Unknown').title()

        embed8=discord.Embed(color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
        embed8.set_author(name="translator", icon_url=ctx.author.avatar_url)
        embed8.add_field(name=f"From {src}", value=ret.origin, inline=False)
        embed8.add_field(name=f"To {dest}", value=ret.text, inline=False)
        await ctx.send(embed=embed8)

    
    @commands.command(name="snipe", aliases=['s'], description="Sends the last deleted message.", usage=".snipe or .s")
    @commands.guild_only()
    @commands.has_any_role("mods", "bot 3000", "png")
    async def snipe(self, ctx):
        try:
            contents, author, time = self.bot.sniped_messages[ctx.guild.id, ctx.channel.id]
            embed3=discord.Embed(description=contents, color=utils.GCOLOR, timestamp=time)
            embed3.set_author(name=author, icon_url=author.avatar_url)
            await ctx.send(embed=embed3)
        
        except:
            embed4=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, there isn't any deleted message recently.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed4)
        
    
    @commands.command(name="esnipe", aliases=['es'], description="Sends the last edited message with before and after.", usage=".esnipe or .es")
    @commands.guild_only()
    @commands.has_any_role('mods', 'bot 3000', 'png')
    async def esnipe(self, ctx):
        try:
            content1, content2, author = self.bot.edited_messages[ctx.guild.id, ctx.channel.id]
            embed5=discord.Embed(color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
            embed5.set_author(name=author, icon_url=author.avatar_url)
            embed5.add_field(name="Before", value=content1, inline=False)
            embed5.add_field(name="After", value=content2, inline=False)
            await ctx.send(embed=embed5)
        
        except:
            embed6=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, there isn't any edited message recently.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed6)

    
    @commands.command(name="roll", description="Rolls a number between 0 and 100.", usage=".roll")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def roll(self, ctx):
        randnumber = random.randint(0, 100)
        await ctx.reply(f"you rolled {randnumber}", mention_author=False)
    
    
    @commands.command(name="ping", description='Just says "pong!". Oh and also sends the bot latency.', usage=".ping")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.reply(f"pong! <a:dancemiku:840294007241965599> `{round(self.bot.latency * 1000)}ms`")



    @roll.after_invoke
    async def rc(self, ctx):
        if ctx.author.guild_permissions.kick_members:
            self.roll.reset_cooldown(ctx)
    @ping.after_invoke
    async def rc(self, ctx):
        if ctx.author.guild_permissions.kick_members:
            self.ping.reset_cooldown(ctx)
    @translate.after_invoke
    async def rc(self, ctx):
        if ctx.author.guild_permissions.kick_members:
            self.translate.reset_cooldown(ctx)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embederr1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, couldn't find a user.", color=utils.ERRCOLOR)
            await ctx.send(embed=embederr1)
    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embederr1=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, couldn't find a member.", color=utils.ERRCOLOR)
            await ctx.send(embed=embederr1)
    
    
def setup(bot):
    bot.add_cog(Misc(bot))