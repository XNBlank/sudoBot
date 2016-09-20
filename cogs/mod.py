import discord;
from discord.ext import commands;
from .init import checks;
import asyncio;

class Mod:
    """ Moderative Commands """

    def __init__(self, bot, config):
        self.bot = bot;
        self.config = config;

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.Member, *, reason : str):
        """Kicks a member from the server.
        In order for this to work, the bot must have Kick Member permissions.
        To use this command you must have Kick Members permission or have the Admin role.
        """

        channels = self.bot.get_all_channels();

        print(channels);

        log_chan = self.config['log_channel'];
        chan_id = 0;

        for i in channels:
            if log_chan in i.name:
                chan_id = i;
                print('Channel Name is ' + chan_id.name);

        try:
            #await self.bot.kick(user);
            print('This would kick.');
        except discord.Forbidden:
            await self.bot.say('The bot does not have permissions to kick members.');
        else:
            await self.bot.send_message(chan_id, 'User **' + user.name + '** was kicked for reason :\n***' + reason + '***.');

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(ban_members=True)
    async def ban(self, ctx, user : discord.Member, *, reason : str):
        """Bans a member from the server.
        In order for this to work, the bot must have Ban Member permissions.
        To use this command you must have Ban Members permission or have the Admin role.
        """

        channels = self.bot.get_all_channels();

        print(channels);

        log_chan = self.config['log_channel'];
        chan_id = 0;

        for i in channels:
            if log_chan in i.name:
                chan_id = i;
                print('Channel Name is ' + chan_id.name);

        try:
            #await self.bot.ban(user);
            print('This would ban.');
        except discord.Forbidden:
            await self.bot.say('The bot does not have permissions to ban members.');
        else:
            await self.bot.send_message(chan_id, 'User **' + user.name + '** was banned for reason :\n***' + reason + '***.');


    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_messages=True)
    async def prune(self, ctx, amount : int = 50):
        """Prunes bot messages.
        In order for this to work, the bot must have Manage Messages permissions.
        To use the command you must have Manage Messages permissions or have the Admin role.
        """

        channel = ctx.message.channel;

        calls = 0;
        async for msg in self.bot.logs_from(channel, limit=amount, before=ctx.message):
            if calls and calls % 5 == 0:
                await asyncio.sleep(1.5);

            if msg.author == self.bot.user:
                await self.bot.delete_message(msg);
                calls += 1;
        if calls == 1:
            await self.bot.say('`Pruned {0} message.`'.format(calls));
        else:
            await self.bot.say('`Pruned {0} messages.`'.format(calls));
