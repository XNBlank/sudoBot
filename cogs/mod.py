import discord
from discord.ext import commands
from .init import checks
import json
import os.path
import asyncio
import sys

class Mod:
    """ Moderative Commands """

    def __init__(self, bot, config, thread=None):
        self.bot = bot
        self.config = config
        self.thr = thread

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.Member, *, reason = None):
        """Kicks a member from the server.
        In order for this to work, the bot must have Kick Member permissions.
        To use this command you must have Kick Members permission or have the Admin role.
        """

        channels = self.bot.get_all_channels()
        moderator = ctx.message.author
        mod_role = None
        roles = ctx.message.server.roles

        print(channels)

        if(reason == None):

            for idx, i in enumerate(roles):
                role = i.name
                if(role == self.config['mod_role']):
                    mod_role = i

            reason = 'Reason not given. {0} feel free to edit this message to put a reason.'.format(mod_role.mention)

        log_chan = self.config['log_channel']
        chan_id = 0

        for i in channels:
            if log_chan in i.name:
                chan_id = i
                print('Channel Name is ' + chan_id.name)

        try:
            await self.bot.kick(user)
        except discord.Forbidden:
            await self.bot.say('The bot does not have permissions to kick members.')
        else:
            await self.bot.send_message(chan_id, 'User **{0} : {1}** was kicked for reason :\n***{2}***\nKicked by : **{3}**'.format(user.name, user.id, reason, moderator.name))

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(ban_members=True)
    async def ban(self, ctx, user : discord.Member, *, reason = None):
        """Bans a member from the server.
        In order for this to work, the bot must have Ban Member permissions.
        To use this command you must have Ban Members permission or have the Admin role.
        """

        channels = self.bot.get_all_channels()
        moderator = ctx.message.author
        mod_role = None
        roles = ctx.message.server.roles

        print(channels)

        if(reason == None):

            for idx, i in enumerate(roles):
                role = i.name
                if(role == self.config['mod_role']):
                    mod_role = i

            reason = 'Reason not given. {0} feel free to edit this message to put a reason.'.format(mod_role.mention)

        log_chan = self.config['log_channel']
        chan_id = 0

        for i in channels:
            if log_chan in i.name:
                chan_id = i
                print('Channel Name is ' + chan_id.name)

        try:
            await self.bot.ban(user)
        except discord.Forbidden:
            await self.bot.say('The bot does not have permissions to ban members.')
        else:
            await self.bot.send_message(chan_id, 'User **{0} : {1}** was banned for reason :\n***{2}***\nBanned by : **{3}**'.format(user.name, user.id, reason, moderator.name))


    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_messages=True)
    async def prune(self, ctx, amount : int = 50):
        """Prunes bot messages.
        In order for this to work, the bot must have Manage Messages permissions.
        To use the command you must have Manage Messages permissions or have the Admin role.
        """

        channel = ctx.message.channel

        calls = 0
        async for msg in self.bot.logs_from(channel, limit=amount, before=ctx.message):
            if calls and calls % 5 == 0:
                await asyncio.sleep(1.5)

            if msg.author == self.bot.user:
                await self.bot.delete_message(msg)
                calls += 1
        if calls == 1:
            await self.bot.say('`Pruned {0} message.`'.format(calls))
        else:
            await self.bot.say('`Pruned {0} messages.`'.format(calls))

    
    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(ban_members=True)
    async def warn(self, ctx, user : discord.Member, points : int, *, reason = None):
        """Warns a member from the server.
        In order for this to work, the bot must have Ban Member permissions.
        To use this command you must have Ban Members permission or have the Admin role.
        """

        channels = self.bot.get_all_channels()
        moderator = ctx.message.author
        mod_role = None
        roles = ctx.message.server.roles

        warnCount = 0

        if(reason == None):

            for idx, i in enumerate(roles):
                role = i.name
                if(role == self.config['mod_role']):
                    mod_role = i

            reason = 'Reason not given. {0} feel free to edit this message to put a reason.'.format(mod_role.mention)

        dataFile = 'data/warns/warns.dat'
        data = {}

        print(os.path.isfile(dataFile))

        if(os.path.isfile(dataFile)):
            with open(dataFile, 'r', encoding='utf8') as f:
                data = json.load(f)
                print(data)
                print('closed')
            
            if(user.id not in data):
                data['{0}'.format(user.id)] = '{0}'.format(points)
                warnCount = points
            else:
                warnCount = data["{0}".format(user.id)]
                data["{0}".format(user.id)] = int(warnCount) + points
                warnCount = data["{0}".format(user.id)]
            
            with open(dataFile, 'w', encoding='utf8') as f:
                f.write(json.dumps(data))
                print('written')

        else:
            data = {
                "{0}".format(user.id) : "{0}".format(points)
            }

            data["{0}".format(user.id)] = warnCount
            warnCount = points
            
            async with open(dataFile, 'w', encoding='utf8') as f:
                f.write(json.dumps(data))
                print('written')
                f.close()

            print(data)

        # print(channels)

        log_chan = self.config['log_channel']
        chan_id = 0

        for i in channels:
            if log_chan in i.name:
                chan_id = i
                # print('Channel Name is ' + chan_id.name)
        
        print(warnCount)

        try:
            if(int(warnCount) >= 1000):
                print("Banned!")
                await self.bot.ban(user)
                await self.bot.send_message(chan_id, 'User **{0} : {1}** was banned for reason :\n***{2}***\nBanned by : **{3}**'.format(user.name, user.id, "Exceeding warning points. (1000)", moderator.name))
            elif(int(warnCount) > 800 and int(warnCount) < 1000):
                await self.bot.kick(user)
                await self.bot.send_message(chan_id, 'User **{0} : {1}** was kicked for reason :\n***{2}***\nKicked by : **{3}**'.format(user.name, user.id, "Exceeding warning points. (600)", moderator.name))
            else:
                print("warned")
        except discord.Forbidden:
            await self.bot.say('The bot does not have permissions to ban members.')
        else:
            print("send messages")
            if(int(warnCount) >= 1000):
                await self.bot.send_message(chan_id, 'User **{0} : {1}** was banned for reason :\n***Exceeding warning points.***\nBanned by : **{2}**'.format(user.name, user.id, moderator.name))
            elif(int(warnCount) > 800 and int(warnCount) < 1000):
                await self.bot.kick(user)
                await self.bot.send_message(chan_id, 'User **{0} : {1}** was kicked for reason :\n***{2}***\nKicked by : **{3}**'.format(user.name, user.id, "Exceeding warning points. (600)", moderator.name))
            else:
                await self.bot.send_message(chan_id, 'User **{0} : {1}** was warned for reason :\n***{2}***\nWarned by : **{3}**\nWarning Points : **{4}**'.format(user.name, user.id, reason, moderator.name, warnCount))


    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(ban_members=True)
    async def liftwarn(self, ctx, user : discord.Member, points : int):
        """Lifts X amount of Warning points from a member in the server.
        In order for this to work, the bot must have Ban Member permissions.
        To use this command you must have Ban Members permission or have the Admin role.
        """

        channels = self.bot.get_all_channels()
        moderator = ctx.message.author
        warnCount = 0
        dataFile = 'data/warns/warns.dat'
        data = {}

        with open(dataFile, 'r', encoding='utf8') as f:
            data = json.load(f)
            print(data)
            print('closed')
            f.close()

        log_chan = self.config['log_channel']
        chan_id = 0

        for i in channels:
            if log_chan in i.name:
                chan_id = i

        if(user.id not in data or int(data["{0}".format(user.id)] == 0)):
            await self.bot.send_message(ctx.message.channel, 'That user doesn\'t have any warning points.')
        else:
            warnCount = data["{0}".format(user.id)]
            data["{0}".format(user.id)] = int(warnCount) - points
            warnCount = data["{0}".format(user.id)]

            with open(dataFile, 'w', encoding='utf8') as f:
                f.write(json.dumps(data))
                print('written')
                f.close()

            await self.bot.send_message(chan_id, 'User **{0} : {1}** was lifted {2} warning points.\nAction by : **{3}**\nRemaining Warning Points : **{4}**'.format(user.name, user.id, points, moderator.name, warnCount))


