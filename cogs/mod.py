import discord
import grizzly
import utils

from discord.ext import commands


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.grizzly = grizzly.Grizzly(bot=self.bot)

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Mod cog has been loaded.')

    
    @commands.command(name='ban', aliases=['b'], description='Bans a member and sends them a DM with the reason and the ban appeal link.', usage='.ban <member> <reason>')
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, *, reason=None):
        if not member:
            await self.grizzly.mod_err_nomember(ctx)
            return
        elif member == ctx.author:
            await self.grizzly.mod_err_author(ctx)
            return
        elif ctx.author.top_role.position <= member.top_role.position:
            await self.grizzly.mod_err_hierarchy(ctx)
            return
        elif not reason:
            await self.grizzly.mod_err_noreason(ctx)
            return

        try:
            await self.grizzly.ban_dm(ctx=ctx, member=member, reason=reason)
        except discord.HTTPException:
            pass 

        await member.ban(reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id}) | Reason: {reason}')
        await self.grizzly.mod_embed_ok(ctx=ctx, member=member, reason=reason, word='banned')
        await self.grizzly.mod_log(ctx=ctx, member=member, reason=reason, word='banned')

    
    @commands.command(name='kick', aliases=['k'], description='Kicks a member and sends them a DM with the reason.', usage='.kick <member> <reason>')
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, *, reason=None):
        if not member:
            await self.grizzly.mod_err_nomember(ctx)
            return
        elif member == ctx.author:
            await self.grizzly.mod_err_author(ctx)
            return
        elif ctx.author.top_role.position <= member.top_role.position:
            await self.grizzly.mod_err_hierarchy(ctx)
            return
        elif not reason:
            await self.grizzly.mod_err_noreason(ctx)
            return
        
        try:
            await self.grizzly.kick_dm(ctx, member, reason)
        except discord.HTTPException:
            pass 

        await member.kick(reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id}) | Reason: {reason}')
        await self.grizzly.mod_embed_ok(ctx=ctx, member=member, reason=reason, word='kicked')
        await self.grizzly.mod_log(ctx=ctx, member=member, reason=reason, word='kicked')

    
    @commands.command(name='muted', description='A list of all the muted members in the server.', usage='.muted')
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def muted(self, ctx):
        await self.grizzly.muted_list(ctx)

    
    @commands.command(name='mute', aliases=['m'], description='Mutes a member indefinitely. Reason is optional.', usage='.mute <member> |reason|')
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member=None, * , reason=None):
        muted = ctx.guild.get_role(utils.MUTED)

        if not member:
            await self.grizzly.mod_err_nomember(ctx)
            return
        elif member == ctx.author:
            await self.grizzly.mod_err_author(ctx)
            return
        elif ctx.author.top_role.position <= member.top_role.position:
            await self.grizzly.mod_err_hierarchy(ctx)
            return
        elif muted in member.roles:
            await self.grizzly.mod_err_mute(ctx)
            return 
        elif not reason:
            reason = 'Not specified'
        
        member.add_roles(muted)
        await self.grizzly.mod_embed_ok(ctx=ctx, member=member, reason=reason, word='muted')

    
    @commands.command(name='unmute', aliases=['um'], description="Unmutes a member if they're muted.", usage='.unmute <member> or .um <member>')
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member=None):
        muted = ctx.guild.get_role(utils.MUTED)

        if not member:
            await self.grizzly.mod_err_nomember(ctx)
            return
        elif muted not in member.roles:
            await self.grizzly.mod_err_unmute(ctx)
            return
        
        member.remove_roles(muted)
        await self.grizzly.mod_embed_ok(ctx=ctx, member=member, reason='Unmute', word='unmuted')

    
    @commands.command(name='warn', aliases=['w'], description='Warns a member and sends them a warning DM. Reason is optional.', usage='.warn <member> |reason| or .w <member> |reason|')
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member=None, *, reason=None):
        if not member:
            await self.grizzly.mod_err_nomember(ctx)
            return
        elif member == ctx.author:
            await self.grizzly.mod_err_author(ctx)
            return
        elif ctx.author.top_role.position <= member.top_role.position:
            await self.grizzly.mod_err_hierarchy(ctx)
            return
        elif not reason:
            reason = 'Not specified'
        
        try:
            await self.grizzly.warn_dm(ctx, member)
        except discord.HTTPException:
            pass 

        await self.grizzly.mod_embed_ok(ctx=ctx, member=member, reason=reason, word='warned')

    
    @commands.command(name='purge', aliases=['p'], description='Purges a specific amount of messages.', usage='.purge <amount> or .p <amount>')
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int=None):
        if not amount:
            await self.grizzly.mod_err_purgeamount(ctx)
            return 
        elif amount > 100:
            await self.grizzly.mod_err_purgelimit(ctx)
            return 
        
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'{utils.OKCHAR} Successfully purged `{amount}` messages.', delete_after=10.0)
    

    @commands.command(name='unban', aliases=['ub'], description='Unbans a user by their Discord username and tag.', usage='.unban <user> or .ub <user>')
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, *, member=None):
        if not member:
            await self.grizzly.mod_err_nomember(ctx)
            return 
        
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user, reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id})')
                await self.grizzly.mod_embed_ok(ctx=ctx, member=member, reason='Unban', word='unbanned')
            
    
    @commands.command(name='unbanid', aliases=['ubid'], description='Unbans a user by their Discord ID.', usage='.unbanid <id> or .ubid <id>')
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unbanid(self, ctx, user: discord.User=None):
        if not user:
            await self.grizzly.mod_err_nomember(ctx)
            return 
        
        await ctx.guild.unban(user, reason=f'Responsible Moderator: {ctx.author} (ID: {ctx.author.id})')
        await self.grizzly.mod_embed_ok(ctx=ctx, member=user, reason='Unban', word='unbanned')
    

    @commands.command(name='color', description="Changes a role's color.", usage='.color <hex color code> <role>')
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def color(self, ctx, color: discord.Color=None, *, role: discord.Role=None):
        if not color:
            await self.grizzly.color_err_nocolor(ctx)
            return 
        elif not role:
            await self.grizzly.color_err_norole(ctx)
            return

        await role.edit(color=color)
        await self.grizzly.color_ok(ctx=ctx, role=role, color=color)
    

    @commands.command(name='userinfo', aliases=['whois'], description='Shows info about the member.', usage='.userinfo <member> or .whois <member>')
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def userinfo(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        
        await self.grizzly.userinfo_embed(ctx, member)
    

    @commands.command(name='snipe', aliases=['s'], description='Sends the last deleted message.', usage='.snipe or .s')
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def snipe(self, ctx):
        try:
            contents, author, time = self.bot.sniped_messages[ctx.guild.id, ctx.channel.id]
            await self.grizzly.snipe_embed(ctx=ctx, contents=contents, author=author, time=time)
        except:
            await self.grizzly.snipe_err(ctx)
        
    
    @commands.command(name='esnipe', aliases=['es'], description='Sends the last edited message with before and after.', usage='.esnipe or .es')
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def esnipe(self, ctx):
        try:
            before, after, author, time = self.bot.edited_messages[ctx.guild.id, ctx.channel.id]
            await self.grizzly.esnipe_embed(ctx=ctx, before=before, after=after, author=author, time=time)
        except:
            await self.grizzly.esnipe_err(ctx)

    
    @commands.command(name='scamlink', aliases=['sl'], description='Deletes all the scam links from a specific member.', usage='.scamlink <member> or .sl <member>')
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def scamlink(self, ctx, member: discord.Member=None):
        if not member:
            await self.grizzly.mod_err_nomember(ctx)
            return
        
        for channel in ctx.guild.text_channels:
            async for message in channel.history(limit=1):
                if message.author.id == member.id:
                    await message.delete()


    
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.grizzly.err_memberbadarg(ctx)
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.grizzly.err_memberbadarg(ctx)
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.grizzly.err_memberbadarg(ctx)
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.grizzly.err_memberbadarg(ctx)
    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.grizzly.err_memberbadarg(ctx)
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.grizzly.mod_err_purgebadarg(ctx)
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.grizzly.mod_err_unban(ctx)
    @unbanid.error
    async def unbanid_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.grizzly.mod_err_unban(ctx)
    @color.error
    async def color_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.grizzly.color_err_badarg(ctx)
    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await self.grizzly.err_memberbadarg(ctx)

def setup(bot):
    bot.add_cog(Mod(bot))