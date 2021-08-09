# imports
import discord 
import datetime
import os

from discord.ext import commands 
from discord.ext import tasks
from utils import utils

# bot variables
bot = commands.Bot(commands.when_mentioned_or(utils.PREFIX), intents=utils.INTENTS, owner_id=utils.OWNERID, help_command=None, status=discord.Status.idle)
bot.launch_time = datetime.datetime.utcnow()
bot.sniped_messages = {}
bot.edited_messages = {}
bot.version = "v3.0"


# jishaku variables
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"
bot.load_extension('jishaku')


# cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
for filename in os.listdir('./mod'):
    if filename.endswith('.py'):
        bot.load_extension(f'mod.{filename[:-3]}')


# startup
@bot.event
async def on_ready():
    print("Grizzly is up and running. Loading cogs...")
    print(f"Currently can see {len(bot.users)} members.")

@tasks.loop(minutes=5.0)
async def changestatus():
    await bot.change_presence(activity=discord.Game(next(utils.STATUS)))

async def startup():
    await bot.wait_until_ready()
    await changestatus.start()
bot.loop.create_task(startup())


# run
if __name__ == '__main__':
    try:
        bot.run(utils.GRIZZTOKEN)
    except discord.errors.HTTPException and discord.errors.LoginFailure as e:
        print(f"WARNING, LOGIN WAS UNSUCCESSFUL. ERROR: {e}")