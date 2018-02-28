import discord
from discord.ext import commands
import asyncio
import json
import datetime
import logging
import re

with open('./config.json', 'r') as cjson:
    config = json.load(cjson)

desc = ''' '''
prefix = config["prefix_settings"]["prefix"]
modules = config["modules"]

if config["prefix_settings"]["use_space"] == True:
    prefix = prefix + ' '

client = commands.Bot(command_prefix=prefix, description=desc)
client.config = config
start_time = datetime.datetime.now()

#Convert uptime to a string.
def timedelta_str(dt):
    days = dt.days
    hours, r = divmod(dt.seconds, 3600)
    minutes, sec = divmod(r, 60)

    if minutes == 1 and sec == 1:
        return '{0} days, {1} hours, {2} minute and {3} second.'.format(days,hours,minutes,sec)
    elif minutes > 1 and sec == 1:
        return '{0} days, {1} hours, {2} minutes and {3} second.'.format(days,hours,minutes,sec)
    elif minutes == 1 and sec > 1:
        return '{0} days, {1} hours, {2} minute and {3} seconds.'.format(days,hours,minutes,sec)
    else:
        return '{0} days, {1} hours, {2} minutes and {3} seconds.'.format(days,hours,minutes,sec)

@client.event
async def on_command_error(ctx, exception):
    logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.error(str(exception))
    if re.match(r'^The check functions for command.*', str(exception)) is None:
        await ctx.send(str(exception))

@client.event
async def on_error(event, *args, **kwargs):
    logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.error(event + " -> " + str(args) + " " + str(kwargs))



@client.event
async def on_ready():
    print('Successfully logged in.')
    print('Username -> ' + client.user.name)
    print('ID -> ' + str(client.user.id))
    print('Admin Users -> ' + str(config['owner_ids']))
    print('Command prefix -> ' + prefix)
    
@client.command()
async def uptime(ctx):
    """Displays bot uptime."""
    global start_time
    await ctx.send(timedelta_str(datetime.datetime.now() - start_time))

@client.command()
async def source(ctx):
    """Post a link to the bot source code."""
    source = "https://github.com/XNBlank/sudoBot"
    await ctx.send(source)

def ready(client, config):
    for module in modules:
        try:
            client.load_extension("modules." + module)
        except Exception as e:
            raise Exception(e)


ready(client, config)

client.run(config["token"])