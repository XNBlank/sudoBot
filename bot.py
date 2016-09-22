# General imports
import discord;
from discord.ext import commands;
import asyncio;
import json;
import datetime;

# Import Modules
import cogs.general;
import cogs.fun;
import cogs.mod;

# Load the config file and assign it to a variable.
with open('config.json', 'r') as c_json:
    config = json.load(c_json);

description = '''sudobotPy is written in Python. Version 0.1''';

# Assign the prefix.
prefix = config["prefix_settings"]["prefix"];

# Check if prefix includes a spacer (example : sudo <command> instead of sudo<command>)
if config["prefix_settings"]["use_space"] == True:
    prefix = prefix + ' ';

# Create bot
bot = commands.Bot(command_prefix=prefix, description=description);

# Create variable for time of startup.
startupTime = datetime.datetime.now()


@bot.event
async def on_ready():
    print('Logged in as ');
    print(bot.user.name);
    print(bot.user.id);
    print('Bot prefix is set to ' + prefix);
    print('-------------');
    await bot.change_status(game=discord.Game(name='with systemd'));

@bot.command()
async def uptime():
    """Check bot uptime."""
    global startupTime;
    await bot.say(timedelta_str(datetime.datetime.now() - startupTime));

# Convert uptime to a string.
def timedelta_str(dt):
    days = dt.days;
    hours, r = divmod(dt.seconds, 3600);
    minutes, sec = divmod(r, 60);

    if minutes == 1 and sec == 1:
        return '{0} days, {1} hours, {2} minute and {3} second.'.format(days,hours,minutes,sec);
    elif minutes > 1 and sec == 1:
        return '{0} days, {1} hours, {2} minutes and {3} second.'.format(days,hours,minutes,sec);
    elif minutes == 1 and sec > 1:
        return '{0} days, {1} hours, {2} minute and {3} seconds.'.format(days,hours,minutes,sec);
    else:
        return '{0} days, {1} hours, {2} minutes and {3} seconds.'.format(days,hours,minutes,sec);

def ready(bot, config):
    if config['modules']['general'] == True:
        bot.add_cog(cogs.general.General(bot, config));
    if config['modules']['fun'] == True:
        bot.add_cog(cogs.fun.Fun(bot, config));
    if config['modules']['mod'] == True:
        bot.add_cog(cogs.mod.Mod(bot, config));

ready(bot, config);

bot.run(config['token']);
