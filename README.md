# sudoBot
A Discord bot written in Python using Discord-Py Rewrite

## Getting Started

These are needed to be able to run **sudoBot**.

- [Python 3.5](https://www.python.org/)
- [Discord.py[Rewrite]](https://github.com/Rapptz/discord.py/tree/rewrite)
- [Pillow](https://github.com/python-pillow/Pillow)
- [A unicode font like Noto Sans CJK (or a font of your choice)](https://www.google.com/get/noto/help/cjk/)

## Setup

Edit `config.sample.json` to your liking, then save it as `config.json`.

Place your selected font in `/data/fonts/` and be sure to link it in the config.

Once you're ready just run `python main.py` in the active directory to start the bot.

## Cogs

**sudoBot** has different modules that you can enable / disable. The current 'modules' available are : 

- Profile : General commands used within a server. 
- Roles : Commands that are fun for users to play with, and serve nothing other than lighthearted spammy goodness.
- Admin : Administrative and Moderative commands.

Sudobot has been updated to be easily configurable and will allow you to load your own modules.

## Commands
```php
Profile:
  profile     Profile command ( see 'sudo help profile' for more info )
Admin:
  reload      Reload a module
  load        Load a module
  unload      Unload a module
  reloadconf  Reload the configuration file ( also reloads all active modules )
Roles:
  joindistro  Add yourself to a joinable user role.
  leavedistro Remove yourself to a joinable user role.
  listdistro  List available joinable user roles.
​No Category:
  help        Shows this message.
  source      Post a link to the bot source code.
  uptime      Displays bot uptime.
```
