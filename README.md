# sudoBot
A Discord bot written in Python

## Getting Started

These are needed to be able to run **sudobot**.

- [Python 3.5](https://www.python.org/)
- [Discord.py](https://github.com/Rapptz/discord.py)

## Setup

Edit `config.sample.json` to your liking, then save it as `config.json`.

Once you're ready just run `python bot.py` in the active directory to start the bot.

## Cogs

**Sudobot** has different modules that you can enable / disable. The current 'cogs' available are : 

- General : General commands used within a server. 
- Fun : Commands that are fun for users to play with, and serve nothing other than lighthearted spammy goodness.
- Mod : Administrative and Moderative commands.

Currently, the only way to enable / disable these are through `config.json` but this will change in the future.

## Commands
```php
Fun:
  cow         A speaking/thinking cow
General:
  leavedistro Leave a distribution role that is currently assigned to you.
  pacman      Pacman commands.
  joindistro  Join one of the many distribution roles available.
  source      Post a link to the bot source code.
Mod:
  prune       Prunes bot messages.
  ban         Bans a member from the server.
  kick        Kicks a member from the server.
Misc:
  uptime      Check bot uptime.
  help        Shows this message.
```
