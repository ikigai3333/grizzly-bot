import discord
import datetime
import os
import utils

from discord.ext import commands, tasks
from itertools import cycle


bot = commands.Bot(commands.when_mentioned_or('.'), description="A moderation bot for grizzlypng's osu! server.", owner_id=847572855478026260, help_command=None, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False, replied_user=False), intents=discord.Intents.all())
bot.launch_time = datetime.datetime.utcnow()
bot.sniped_messages = {}
bot.edited_messages = {}
bot.current_version = 'v4.0'
bot.amount_of_lines = '1.157'
status = cycle(['osu!', 'grizzly lovs you ♡'])


os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"
bot.load_extension('jishaku')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    print(f'{bot.user} is up and running. Loading cogs...')

@tasks.loop(minutes=5.0)
async def changestatus():
    await bot.change_presence(activity=discord.Game(next(status)))

async def startup():
    await bot.wait_until_ready()
    await changestatus.start()
bot.loop.create_task(startup())

if __name__ == '__main__':
    try:
        bot.run(utils.GRIZZTOKEN)
    except discord.errors.HTTPException and discord.errors.LoginFailure as e:
        print(f'WARNING, LOGIN WAS UNSUCCESSFUL. ERROR: {e}')