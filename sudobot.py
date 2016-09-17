import discord;
from discord.ext import commands;
import asyncio;

description = '''sudobotPy written in Python.

Owned by Blank.'''
bot = commands.Bot(command_prefix='sudopy ', description=description)

@bot.event
async def on_ready():
    print('Logged in as ');
    print(bot.user.name);
    print(bot.user.id);
    print('-------------');

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined.""";
    await bot.say('```{0.name} joined in {0.joined_at}```'.format(member));

bot.run('token');
