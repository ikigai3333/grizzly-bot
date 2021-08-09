import discord
import aiohttp
from discord.ext import commands
from utils import utils


class RandomAPIs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.whitelist = ['mods', 'bot 3000', 'png'] 
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"RandomAPIs has been loaded.")


    @commands.command(name="miku", description="Sends a random Hatsune Miku image.", usage=".miku")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def miku(self, ctx):
        async with ctx.typing():
            async with aiohttp.ClientSession() as s:
                async with s.get("https://miku-for.us/api/v2/random") as r:
                    res = await r.json(content_type=None)

                    embed1=discord.Embed(color=utils.MIKUCOLOR, timestamp=utils.TIMESTAMP)
                    embed1.set_author(name="miku! <a:dancemiku:840294007241965599>", url="https://miku-for.us", icon_url=res['url'])
                    embed1.set_image(url=res['url'])
                    await ctx.send(embed=embed1)

    
    @commands.command(name="duck", description="Sends a random duck image.", usage=".duck")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def duck(self, ctx):
        async with ctx.typing():
            async with aiohttp.ClientSession() as s:
                async with s.get("https://random-d.uk/api/v2/random") as r:
                    res = await r.json(content_type=None)

                    embed2=discord.Embed(color=utils.DUCKCOLOR, timestamp=utils.TIMESTAMP)
                    embed2.set_author(name="duck :o", url="https://random-d.uk", icon_url=res['url'])
                    embed2.set_image(url=res['url'])
                    await ctx.send(embed=embed2)

    
    @commands.command(name="cat", description="Sends a random cat image.", usage=".cat")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cat(self, ctx):
        async with ctx.typing():
            async with aiohttp.ClientSession() as s:
                async with s.get("https://some-random-api.ml/img/cat") as r:
                    res = await r.json(content_type=None)

                    embed3=discord.Embed(color=utils.CDCOLOR, timestamp=utils.TIMESTAMP)
                    embed3.set_author(name="cat :3", url="https://some-random-api.ml", icon_url=res['link'])
                    embed3.set_image(url=res['link'])
                    await ctx.send(embed=embed3)

    
    @commands.command(name="dog", aliases=['dawg'], description="Sends a random dog image.", usage=".dog or .dawg")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dog(self, ctx):
        async with ctx.typing():
            async with aiohttp.ClientSession() as s:
                async with s.get("https://some-random-api.ml/img/dog") as r:
                    res = await r.json(content_type=None)

                    embed4=discord.Embed(color=utils.CDCOLOR, timestamp=utils.TIMESTAMP)
                    embed4.set_author(name=f"dawg <a:dawg:858489651332644884>", url="https://some-random-api.ml", icon_url=res['link'])
                    embed4.set_image(url=res['link'])
                    await ctx.send(embed=embed4)


    @commands.command(name="panda", description="Sends a random panda image.", usage=".panda")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def panda(self, ctx):
        async with ctx.typing():
            async with aiohttp.ClientSession() as s:
                async with s.get("https://some-random-api.ml/img/panda") as r:
                    res = await r.json(content_type=None)

                    embed5=discord.Embed(color=utils.PANDACOLOR, timestamp=utils.TIMESTAMP)
                    embed5.set_author(name=f"panda \U0001f43c", url="https://some-random-api.ml", icon_url=res['link'])
                    embed5.set_image(url=res['link'])
                    await ctx.send(embed=embed5)

    
    @commands.command(name="genderize", aliases=['gender'], description="Guesses a name's gender.", usage=".genderize <name> or .gender <name>")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def genderize(self, ctx, name=None):
        if not name:
            embed6=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, please provide a name to genderize!", color=utils.ERRCOLOR, timestamp=utils.TIMESTAMP)
            await ctx.send(embed=embed6)
            return 
        
        async with ctx.typing():
            async with aiohttp.ClientSession() as s:
                async with s.get(f"https://api.genderize.io?name={name}") as r:
                    res = await r.json(content_type=None)

                    embed7=discord.Embed(description=f"<:tiktokthinking:820808828470689824> I'm guessing that the name **{name}** is a **{res['gender']}** name! The probability of being it correct is **{res['probability']}/1.00**.", color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
                    embed7.set_author(name="Genderize!", url="https://api.genderize.io", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed7)

    
    @commands.command(name="bored", description="Sends a random activity to do when you're bored.", usage=".bored")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bored(self, ctx):
        async with ctx.typing():
            async with aiohttp.ClientSession() as s:
                async with s.get("https://www.boredapi.com/api/activity/?participants=1") as r:
                    res = await r.json(content_type=None)

                    embed8=discord.Embed(description=f"<:peepoThink:840307631285075978> This activity type is about **{res['type'].title()}**.\nWhat you can do is **{res['activity'].lower()}!**", color=utils.GCOLOR, timestamp=utils.TIMESTAMP)
                    embed8.set_author(name="cure your boredom", url="https://www.boredapi.com/", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed8)

    # cooldowns reset for staff members :peepoWicked:
    @miku.after_invoke
    async def rc(self, ctx):
        if ctx.author.guild_permissions.kick_members:
            self.miku.reset_cooldown(ctx)
    @duck.after_invoke
    async def rc(self, ctx):
        if ctx.author.guild_permissions.kick_members:
            self.duck.reset_cooldown(ctx)
    @cat.after_invoke
    async def rc(self, ctx):
        if ctx.author.guild_permissions.kick_members:
            self.cat.reset_cooldown(ctx)
    @dog.after_invoke
    async def rc(self, ctx):
        if ctx.author.guild_permissions.kick_members:
            self.dog.reset_cooldown(ctx)
    @panda.after_invoke
    async def rc(self, ctx):
        if ctx.author.guild_permissions.kick_members:
            self.panda.reset_cooldown(ctx)
    @genderize.after_invoke
    async def rc(self, ctx):
        if ctx.author.guild_permissions.kick_members:
            self.genderize.reset_cooldown(ctx)
    @bored.after_invoke
    async def rc(self, ctx):
        if ctx.author.guild_permissions.kick_members:
            self.bored.reset_cooldown(ctx)
            
        
def setup(bot):
    bot.add_cog(RandomAPIs(bot))