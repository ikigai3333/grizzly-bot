import utils
import asyncio
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    

    @commands.Cog.listener()
    async def on_ready(self):
        print('Events cog has been loaded.')

    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        quarantine = guild.get_role(utils.QUARANTINE)
        await member.add_roles(quarantine)

    
    @commands.Cog.listener()
    async def on_message(self, message):
        quarantine = message.guild.get_role(utils.QUARANTINE)
        verified = message.guild.get_role(utils.DISCORDMEMBERS)
        if message.channel.id == utils.VERIFYCHAT:
            if message.content == 'grizzly':
                await message.author.remove_roles(quarantine)
                await message.author.add_roles(verified)
                await message.delete()

            elif message.author.guild_permissions.kick_members:
                pass

            else:
                await message.delete()

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
        
        self.bot.edited_messages[after.guild.id, after.channel.id] = (before.content, after.content, after.author, after.created_at)
        await asyncio.sleep(180)
        try:
            del self.bot.edited_messages[after.guild.id, after.channel.id]
        except KeyError:
            pass 

def setup(bot):
    bot.add_cog(Events(bot))