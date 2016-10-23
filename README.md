# sudoBot
A Discord bot written in Python

## Getting Started

These are needed to be able to run **sudobot**.

- [Python 3.5](https://www.python.org/)
- [Discord.py](https://github.com/Rapptz/discord.py)
- [Pillow](https://github.com/python-pillow/Pillow)

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
  cow          A speaking/thinking cow
  profile      Get an information card on a user in this server.
  profilesetup Setup your profile card
  setprofilebg Set a profile card background image.
General:
  joindistro   Join one of the many distribution roles available.
  listdistro   List available user distro roles.
  leavedistro  Leave a distribution role that is currently assigned to you.
  pacman       Pacman commands.
  source       Post a link to the bot source code.
Mod:
  kick         Kicks a member from the server.
  ban          Bans a member from the server.
  prune        Prunes bot messages.
Misc:
  uptime       Check bot uptime.
  help         Shows this message.
```
