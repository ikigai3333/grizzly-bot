import discord
import grizzly
import utils
import typing
import googletrans
import random

from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.grizzly = grizzly.Grizzly(bot=self.bot)
        self.trans = googletrans.Translator()

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Misc cog has been loaded.')
    

    @commands.command(name='avatar', aliases=['av'], description="Shows a user's profile picture. If they're not in the server, you can use their Discord ID instead.", usage='.avatar <user> or .av <user>')
    @commands.guild_only()
    async def avatar(self, ctx, *, member: typing.Union[discord.Member, discord.User]=None):
        if not member:
            member = ctx.author
        await self.grizzly.avatar_embed(ctx, member)

    
    @commands.command(name='banner', description="Shows a user's banner. If they're not in the server, you can use their discord ID instead.", usage='.banner <user>')
    @commands.guild_only()
    async def banner(self, ctx, *, member: typing.Union[discord.Member, discord.User]=None):
        if not member:
            member = ctx.author
        
        await self.grizzly.banner(ctx, member)
    
    
    @commands.command(name='translate', description='Translates the message to English.', usage='.translate <message>')
    @commands.guild_only()
    async def translate(self, ctx, *, message: commands.clean_content=None):
        if message is None:
            ref = ctx.message.reference
            if ref and isinstance(ref.resolved, discord.Message):
                message = ref.resolved.content
            else:
                await self.grizzly.translate_err_nomsg(ctx)
                return
        
        loop = self.bot.loop
        ret = await loop.run_in_executor(None, self.trans.translate, message)
        src = googletrans.LANGUAGES.get(ret.src, '(auto-detected)').title()
        dest = googletrans.LANGUAGES.get(ret.dest, 'Unknown').title()
        await self.grizzly.translate_embed(ctx=ctx, src=src, dest=dest, ret=ret)
    

    @commands.command(name='roll', description='Rolls a number between 0 and 100.', usage='.roll')
    @commands.guild_only()
    async def roll(self, ctx):
        rand = random.randint(0, 100)
        await ctx.reply(f'you rolled {rand}')
    

    @commands.command(name='ping', description='Pings the bot and sends the bot latency.', usage='.ping')
    @commands.guild_only()
    async def ping(self, ctx):
        await ctx.reply(f'pong! <a:dancemiku:840294007241965599> `{round(self.bot.latency * 1000)}ms`')
    

    @commands.command()
    @commands.guild_only()
    async def invite(self, ctx):
        await ctx.reply('no i am not a public bot!!!!!!!!!!')
    


    #api stuff
    @commands.command(name='miku', description='Sends a random Hatsune Miku image.', usage='.miku')
    @commands.guild_only()
    async def miku(self, ctx):
        async with ctx.typing():
            data = await self.grizzly.botsession('https://miku-for.us/api/v2/random')
            embed=discord.Embed(color=0x137a7f, timestamp=utils.TS)
            embed.set_author(name='miku!')
            embed.set_image(url=data['url'])
            await ctx.send(embed=embed)
    

    @commands.command(name='duck', description='Sends a random duck image.', usage='.duck')
    @commands.guild_only()
    async def duck(self, ctx):
        async with ctx.typing():
            data = await self.grizzly.botsession('https://random-d.uk/api/v2/random')
            embed=discord.Embed(color=0xffd45c, timestamp=utils.TS)
            embed.set_author(name='duck')
            embed.set_image(url=data['url'])
            await ctx.send(embed=embed)
    

    @commands.command(name='cat', description='Sends a random cat image.', usage='.cat')
    @commands.guild_only()
    async def cat(self, ctx):
        async with ctx.typing():
            data = await self.grizzly.botsession('https://some-random-api.ml/img/cat')
            embed=discord.Embed(color=0xd9c9c2, timestamp=utils.TS)
            embed.set_author(name='catkittycatcat')
            embed.set_image(url=data['link'])
            await ctx.send(embed=embed)
    

    @commands.command(name='dog', aliases=['dawg'], description='Sends a random dog image.', usage='.dog or .dawg')
    @commands.guild_only()
    async def dog(self, ctx):
        async with ctx.typing():
            data = await self.grizzly.botsession('https://some-random-api.ml/img/dog')
            embed=discord.Embed(color=0xd9c9c2, timestamp=utils.TS)
            embed.set_author(name='dawg')
            embed.set_image(url=data['link'])
            await ctx.send(embed=embed)

    
    @commands.command(name='panda', description='Sends a random panda image.', usage='.panda')
    @commands.guild_only()
    async def panda(self, ctx):
        async with ctx.typing():
            data = await self.grizzly.botsession('https://some-random-api.ml/img/panda')
            embed=discord.Embed(color=0xffffff, timestamp=utils.TS)
            embed.set_author(name='pandas')
            embed.set_image(url=data['link'])
            await ctx.send(embed=embed)
        
    
    @commands.command(name='genderize', aliases=['gender'], description="Guesses a name's gender.", usage='.genderize <name> or .gender <name>')
    @commands.guild_only()
    async def genderize(self, ctx, name=None):
        if not name:
            await self.grizzly.gender_err(ctx)
            return

        async with ctx.typing():
            data = await self.grizzly.botsession(f'https://api.genderize.io?name={name}')
            embed=discord.Embed(description=f"<:peepoThink:840307631285075978> I'm guessing that the name **{name}** is a **{data['gender']}** name! The probability of being it correct is **{data['probability']}/1.00**.", color=utils.GCOLOR, timestamp=utils.TS)
            embed.set_author(name='genderize', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
    

    @commands.command(name='bored', description="Sends a random activity to do when you're bored.", usage='.bored')
    @commands.guild_only()
    async def bored(self, ctx):
        async with ctx.typing():
            data = await self.grizzly.botsession('https://www.boredapi.com/api/activity/?participants=1')
            embed=discord.Embed(description=f"<a:peepoSleep:883344247259037730> This activity type is about **{data['type'].title()}**.\nWhat you can do is **{data['activity'].lower()}!**", color=utils.GCOLOR, timestamp=utils.TS)
            embed.set_author(name="cure your boredom", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))
