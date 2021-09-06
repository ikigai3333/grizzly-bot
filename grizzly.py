import discord
import utils
import aiohttp
import datetime
import jishaku
import psutil
import platform


class Grizzly:
    def __init__(self, bot):
        self.bot = bot

    # mod stuff
    async def mod_embed_ok(self, ctx, member, reason, word):
        embed=discord.Embed(description=f'{utils.MEMBERCHAR} **{word.title()} Member:** {member} (ID: ||{member.id}||)\n{utils.MODCHAR} **Responsible Moderator:** {ctx.author.mention}\n{utils.REASONCHAR} **Reason:** "{reason}"', color=utils.OKCOLOR, timestamp=utils.TS)
        embed.set_author(name=f'{utils.OKCHAR} Successfully {word}.')
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)
    
    async def mod_log(self, ctx, member, reason, word):
        chan = self.bot.get_channel(utils.LOGCHAT)
        embed=discord.Embed(description=f'{utils.MEMBERCHAR} **{word.title()} Member:** {member} (ID: ||{member.id}||)\n{utils.MODCHAR} **Responsible Moderator:** {ctx.author.mention}\n{utils.REASONCHAR} **Reason:** "{reason}"', color=utils.OKCOLOR, timestamp=utils.TS)
        embed.set_author(name=f'{utils.OKCHAR} Successfully {word}.')
        embed.set_thumbnail(url=member.avatar.url)
        await chan.send(embed=embed)
    
    async def muted_list(self, ctx):
        muted = ctx.guild.get_role(utils.MUTED)
        if len(muted.members) > 0:
            embed=discord.Embed(title='Muted Members', description=f'Currently have **{len(muted.members)}** muted members.\n\u200b\n{chr(10).join(map(str, muted.members))}', color=utils.GCOLOR, timestamp=utils.TS)
            await ctx.send(embed=embed)
        else:
            embed2=discord.Embed(description=f'{utils.ERRCHAR} **{ctx.author.name}**, no one is currently muted.', color=utils.ERRCOLOR)
            await ctx.send(embed=embed2)

    
    async def mod_err_noreason(self, ctx):
        embed=discord.Embed(description=f'{utils.ERRCHAR} **{ctx.author.name}**, please provide a reason.', color=utils.ERRCOLOR)
        await ctx.send(embed=embed)

    async def mod_err_author(self, ctx):
        embed=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, you can't {ctx.command.name} yourself.", color=utils.ERRCOLOR)
        await ctx.send(embed=embed)

    async def mod_err_nomember(self, ctx):
        embed=discord.Embed(description=f'{utils.ERRCHAR} **{ctx.author.name}**, please provide a member / user.', color=utils.ERRCOLOR)
        await ctx.send(embed=embed)

    async def mod_err_hierarchy(self, ctx):
        embed=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, you can't {ctx.command.name} a staff / someone who's higher than you.", color=utils.ERRCOLOR)
        await ctx.send(embed=embed)
 
    async def mod_err_unmute(self, ctx):
        embed=discord.Embed(description=f'{utils.ERRCHAR} **{ctx.author.name}**, that member is already not muted.', color=utils.ERRCOLOR)
        await ctx.send(embed=embed)

    async def mod_err_mute(self, ctx):
        embed=discord.Embed(description=f'{utils.ERRCHAR} **{ctx.author.name}**, that member is already muted.', color=utils.ERRCOLOR)
        await ctx.send(embed=embed)

    async def mod_err_purgeamount(self, ctx):
        embed=discord.Embed(description=f'{utils.ERRCHAR} **{ctx.author.name}**, please provide an amount of messages to purge.', color=utils.ERRCOLOR)
        await ctx.send(embed=embed)

    async def mod_err_purgelimit(self, ctx):
        embed=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, you can't purge more than 100 messages.", color=utils.ERRCOLOR)
        await ctx.send(embed=embed)
    
    async def mod_err_purgebadarg(self, ctx):
        embed=discord.Embed(description=f'{utils.ERRCHAR} **{ctx.author.name}**, please provide a correct amount.', color=utils.ERRCOLOR)
        await ctx.send(embed=embed)

    async def mod_err_unban(self, ctx):
        embed=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, couldn't find a user in the banned members list.", color=utils.ERRCOLOR)
        await ctx.send(embed=embed)


    
    # mod dms
    async def ban_dm(self, ctx, member, reason):
        embed=discord.Embed(title=f'{member.name}, you have been banned from {ctx.guild.name}.', description=f'Hello **{member.name}**, you are able to appeal your ban after 3-7 days using the Ban Appeal form by using the link below (if you believe you were wrongfully banned).', color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name=member, icon_url=member.avatar.url)
        embed.add_field(name='Reasoning for Ban', value=reason, inline=False)
        embed.add_field(name='Ban Appeal Form', value='[Click Here](https://forms.gle/i8PE2uAYQMJwEYeUA)', inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_image(url='https://i.imgur.com/PoGdjWW.jpg')
        embed.set_footer(text='Grizzly', icon_url='https://i.imgur.com/acZwtDC.jpg')
        await member.send(embed=embed)
    
    async def kick_dm(self, ctx, member, reason):
        embed=discord.Embed(title=f'{member.name}, you have been kicked from {ctx.guild.name}.', description=f'Hello **{member.name}**, you have been kicked from {ctx.guild.name}. Please abide by the rules next time!', color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name=member, icon_url=member.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name='Reasoning for Kick', value=reason, inline=False)
        embed.set_footer(text='Grizzly', icon_url='https://i.imgur.com/acZwtDC.jpg')
        await member.send(embed=embed)

    async def warn_dm(self, ctx, member):
        embed=discord.Embed(description=f'Hello **{member.name}**, you have been warned in {ctx.guild.name}. Please abide by the rules next time and respect the members. Thank you!\nYou can see all the server rules by clicking on [this link.](https://discord.com/channels/749099324620669030/749099325098950716/830248577481572383)', color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name=f"{member.name}, you have been warned.", icon_url=member.avatar.url)
        await member.send(embed=embed)

    
    # color embeds
    async def color_err_nocolor(self, ctx):
        embed=discord.Embed(description=f'{utils.ERRCHAR} **{ctx.author.name}**, please provide a color.', color=utils.ERRCOLOR)
        await ctx.send(embed=embed)
    
    async def color_err_norole(self, ctx):
        embed=discord.Embed(description=f'{utils.ERRCHAR} **{ctx.author.name}**, please provide a role.', color=utils.ERRCOLOR)
        await ctx.send(embed=embed)
    
    async def color_err_badarg(self, ctx):
        embed=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, couldn't find a role or color.", color=utils.ERRCOLOR)
        await ctx.send(embed=embed)
    
    async def color_ok(self, ctx, role, color):
        embed=discord.Embed(title=f"{utils.OKCHAR} Successfully changed the color.", description=f"Changed **{role}**'s color to `{color}`.\n<-- This embed's color is the role's new color.", color=color, timestamp=utils.TS)
        await ctx.send(embed=embed)
    

    # dev embeds
    async def dev_help(self, ctx):
        embed = discord.Embed(description=f"written in python! made by `{ctx.author}` ♡", color=utils.GCOLOR)
        embed.set_author(name="developer commands :3", url="https://github.com/ikigai3333/grizzly-bot", icon_url=self.bot.user.avatar.url)
        embed.add_field(name="cogs", value="load, unload, reload, reloadall, listcogs, listcmds", inline=False)
        embed.add_field(name="misc", value="botinfo, rawuserinfo, source, nick", inline=False)
        await ctx.send(embed=embed)

    async def dev_listcogs(self, ctx):
        embed=discord.Embed(description=f'currently have `{len(self.bot.cogs)}` cogs!\n\u200b\n{chr(10).join(map(str, [cog for cog in self.bot.cogs]))}', color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name='all cogs :3', icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)
    
    async def dev_listcmds(self, ctx):
        embed=discord.Embed(description=f'currently have `{len(self.bot.commands)}` commands!\n\u200b\n{chr(10).join(map(str, [cmd for cmd in self.bot.commands]))}', color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name='all commands :3', icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    async def dev_botinfo(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        botinfo = f"""
        Written by `{ctx.author}` with only `{self.bot.amount_of_lines}` lines! ♡
        Grizzly's current version is `{self.bot.current_version}`.

        **__bot stuff__**
        Grizzly is currently in `{len(self.bot.guilds)}` servers.
        Grizzly can currently see `{len(self.bot.users)}` users.
        Grizzly currently has the `Member` and `Presence` intents enabled.
        Grizzly currently has `{len(self.bot.cogs)}` different cogs.
        Grizzly currently has `{len(self.bot.commands)}` different commands.

        **__server-side stuff__**
        Grizzly is currently running on OS `{platform.system()} {platform.release()}`.
        Grizzly currently has `%{psutil.cpu_percent()}` of CPU and `%{psutil.virtual_memory()[2]}` of RAM usage.
        Grizzly's current websocket latency is `{round(self.bot.latency * 1000)}ms`.
        Grizzly's uptime: `{days}` days, `{hours}` hrs, `{minutes}` mins and `{seconds}` secs.

        **__other stuff__**
        Grizzly is running on [Python](https://www.python.org) version `{platform.python_version()}`.
        Grizzly is running on [discord.py](https://github.com/Rapptz/discord.py) version `{discord.__version__}`.
        Grizzly is running on [jishaku](https://github.com/Gorialis/jishaku) version `{jishaku.__version__}`.
        Grizzly's used APIs can be found [here.](https://github.com/ikigai3333/grizzly-bot/blob/main/apis.txt)
        Grizzly's source code can be found [here.](https://github.com/ikigai3333/grizzly-bot)
        """
        embed=discord.Embed(description=botinfo, color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name="bot info :3", url="https://github.com/ikigai3333/grizzly-bot", icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    async def dev_rawuserinfo(self, ctx, data):
        embed=discord.Embed(description=f"**ID:** `{data['id']}`\n**Username:** `{data['username']}`\n**Discriminator:** `{data['discriminator']}`\n**Avatar:** `{data['avatar']}`\n**Banner:** `{data['banner']}`\n**Banner Color:** `{data['banner_color']}`\n**Accent Color:** `{data['accent_color']}`\n**Public Flags:** `{data['public_flags']}`", color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name='advanced user info wowowowo', icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)
    

    #help embeds
    async def help_main(self, ctx):
        embed=discord.Embed(description='All the available commands for Grizzly.\nTo see more info about a specific command, use the command `.help <command>`.', color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name=f'Grizzly Help', url='https://github.com/ikigai3333/grizzly-bot', icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name='Fun commands', value='avatar, banner, userinfo, translate, bored, genderize, ping, roll', inline=False)
        embed.add_field(name='Random image commands', value='miku, cat, dog, panda, duck', inline=False)
        embed.set_footer(text="if you're a staff, see the .modhelp command!")
        await ctx.send(embed=embed)

    async def help_mod(self, ctx):
        embed=discord.Embed(description='All the available staff-only commands for Grizzly.\nTo see more info about a specific command, use the command `.modhelp <command>`.', color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name=f'Grizzly Moderation Help', url='https://github.com/ikigai3333/grizzly-bot', icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name='Commands list', value='ban, unban, unbanid, kick, warn, mute, muted, unmute, purge, color, snipe, esnipe')
        await ctx.send(embed=embed)

    async def help_embeds(self, ctx, command):
        getcmd = self.bot.get_command(command)
        if getcmd.aliases:
            alias = f"({''.join(getcmd.aliases)})"
        else:
            alias = ''
        embed=discord.Embed(description=f'{getcmd.description}\n**Usage:** {getcmd.usage}', color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name=f'{getcmd.name} {alias}', icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)

    
    #misc embeds
    async def avatar_embed(self, ctx, member):
        embed=discord.Embed(color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name=member, icon_url=member.avatar.url)
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    async def userinfo_embed(self, ctx, member):

        roles = [role for role in member.roles[1:]]
        roles.reverse()
        rolecount = len(roles)
        membercreatedat = f"{discord.utils.format_dt(member.created_at, 'F')}, {discord.utils.format_dt(member.created_at, 'R')}"
        memberjoinedat = f"{discord.utils.format_dt(member.joined_at, 'F')}, {discord.utils.format_dt(member.joined_at, 'R')}"
        permslist = []
        perms = ctx.channel.permissions_for(member)
        for name, value in perms:
            name = name.replace('_', ' ').replace('guild', 'server').title()
            if value:
                permslist.append(name)

        embed=discord.Embed(description=member.mention, color=member.color, timestamp=utils.TS)
        embed.set_author(name=member, icon_url=member.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name='ID', value=member.id)
        embed.add_field(name='Color', value=member.color)
        embed.add_field(name='Server Joined At', value=memberjoinedat, inline=False)
        embed.add_field(name='Account Created At', value=membercreatedat, inline=False)
        if rolecount > 0:
            embed.add_field(name=f'Roles ({rolecount})', value=', '.join(([role.mention for role in roles])), inline=False)
        else:
            embed.add_field(name='Roles', value='This member currently has no roles.', inline=False)
        embed.add_field(name='Permissions', value=', '.join(permslist), inline=False)
        if member == ctx.guild.owner:
            embed.add_field(name='Also Known As', value='Server Owner', inline=False)
        elif member.guild_permissions.administrator:
            embed.add_field(name='Also Known As', value='Server Administrator', inline=False)
        else:
            pass
        await ctx.send(embed=embed)
    
    async def translate_err_nomsg(self, ctx):
        embed=discord.Embed(description=f'{utils.ERRCHAR} **{ctx.author.name}**, please provide a message to translate!', color=utils.ERRCOLOR)
        await ctx.send(embed=embed)
    
    async def translate_embed(self, ctx, src, dest, ret):
        embed=discord.Embed(color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name='translator', icon_url=ctx.author.avatar.url)
        embed.add_field(name=f'From {src}', value=ret.origin, inline=False)
        embed.add_field(name=f'To {dest}', value=ret.text, inline=False)
        await ctx.send(embed=embed)
    
    async def snipe_err(self, ctx):
        embed=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, there isn't any deleted message recently.", color=utils.ERRCOLOR)
        await ctx.send(embed=embed)
    
    async def snipe_embed(self, ctx, contents, author, time):
        embed=discord.Embed(description=contents, color=utils.GCOLOR, timestamp=time)
        embed.set_author(name=author, icon_url=author.avatar.url)
        await ctx.send(embed=embed)
    
    async def esnipe_err(self, ctx):
        embed6=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, there isn't any edited message recently.", color=utils.ERRCOLOR)
        await ctx.send(embed=embed6)
    
    async def esnipe_embed(self, ctx, before, after, author, time):
        embed5=discord.Embed(color=utils.GCOLOR, timestamp=time)
        embed5.set_author(name=author, icon_url=author.avatar.url)
        embed5.add_field(name='Before', value=before, inline=False)
        embed5.add_field(name='After', value=after, inline=False)
        await ctx.send(embed=embed5)
    
    async def gender_err(self, ctx):
        embed6=discord.Embed(description=f'{utils.ERRCHAR} **{ctx.author.name}**, please provide a name to genderize!', color=utils.ERRCOLOR)
        await ctx.send(embed=embed6)
    
    async def err_memberbadarg(self, ctx):
        embed=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, couldn't find a member / user.", color=utils.ERRCOLOR)
        await ctx.send(embed=embed)

    
    async def botsession(self, url, headers=None):
        async with aiohttp.ClientSession(headers=headers) as s:
            async with s.get(url) as r:
                data = await r.json(content_type=None)
                return data
    
    async def banner(self, ctx, member):
        authorization = f'Bot {utils.GRIZZTOKEN}'
        headerss = {
            "Authorization": authorization
        }
        data = await self.botsession(f'https://discord.com/api/v9/users/{member.id}', headers=headerss)
        bannerhash = data['banner']

        if bannerhash is None:
            embed=discord.Embed(description=f"{utils.ERRCHAR} **{ctx.author.name}**, this user doesn't have a banner.", color=utils.ERRCOLOR)
            await ctx.send(embed=embed)
            return

        bannerformat = 'gif' if bannerhash.startswith('a_') else 'png'

        embed=discord.Embed(color=utils.GCOLOR, timestamp=utils.TS)
        embed.set_author(name=member, icon_url=member.avatar.url)
        embed.set_image(url=f"https://images.discordapp.net/banners/{member.id}/{bannerhash}.{bannerformat}?size=4096")
        await ctx.send(embed=embed)