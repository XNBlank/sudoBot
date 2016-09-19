import discord;
from discord.ext import commands;
import aiohttp;
import json;
import sys;
import subprocess;

class General:
    """
    General commands from sudobotPy.
    """

    def __init__(self, bot, config):
        self.bot = bot;
        self.config = config;

    @commands.command(pass_context=True)
    async def joindistro(self, ctx, *, distro : str):
        """Join one of the many distribution roles available.
        ```
        ```tex
        # Gentoo
        # Mint
        # Void
        # Manjaro
        # Arch
        # Fedora
        # Debian
        # Ubuntu
        # BSD
        # RedHat
        # ElementaryOS
        # Windows
        # MacOSX
        """
        _server = ctx.message.server;
        _member = ctx.message.author;

        _roles = self.config["user_roles"];
        _serverRoles = _server.roles;
        _userRoles = _member.roles;

        for idx, i in enumerate(_serverRoles):
            _distro = i.name.lower();

            if distro.lower() == _distro:
                for idy, ii in enumerate(_roles):
                    _joindistro = ii.lower();

                    if distro.lower() == _joindistro:
                        for idz, iii in enumerate(_userRoles):

                            _userdistro = str(iii).lower();
                            if distro.lower() == _userdistro:
                                return await self.bot.say('You\'re already in that role.');
                            elif idz >= len(_userRoles)-1:
                                try:
                                    await self.bot.add_roles(_member, i);
                                    print('Added user to role');
                                    return await self.bot.say('Added ' + _member.name + ' to ' + i.name);
                                except Exception as error:
                                    return await self.bot.say('```Error : ' + str(error) + '```');
                    elif idy >= len(_roles)-1:
                        return await self.bot.say('You\'re not allowed to inherit that role.');
            elif idx >= len(_serverRoles)-1:
                return await self.bot.say('That role doesn\'t exist');

    @commands.command(pass_context=True)
    async def leavedistro(self, ctx, *, distro : str):
        """Leave a distribution role that is currently assigned to you."""
        _server = ctx.message.server;
        _member = ctx.message.author;
        _roles = self.config["user_roles"];
        _userRoles = _member.roles;

        for idx, i in enumerate(_userRoles):
            _distro = i.name.lower();

            if distro.lower() == _distro:
                for idy, ii in enumerate(_roles):
                    _checkroles = ii.lower();

                    if distro.lower() == _checkroles.lower():

                        try:
                            await self.bot.remove_roles(_member, i);
                            print('Removed user from role.');
                            return await self.bot.say('Removed ' + _member.name + ' from ' + i.name);
                        except Exception as error:
                            return await self.bot.say('```Error : ' + str(error) + '```');
            elif idx >= len(_roles)-1:
                return await self.bot.say('You\'re not in that role.');

    @commands.command()
    async def findpkg(self, *, query : str):
        """Prints out packages from the arch repo and aur."""
        print('Searching for {0} in Arch repositories and the AUR.'.format(query));

        pkgs = [];

        async with aiohttp.get('https://www.archlinux.org/packages/search/json/?q={0}'.format(query)) as r:
            ar = r.json()['results'];
            for res in ar:
                pkgs.append(res['pkgname']);

#        async with aiohttp.get('http://aur4.archlinux.org/rpc.php?type=search&arg={0}'.format(query)) as u:
#            au = u.json()['results'];
#            for res in au:
#                pkgs.append(['AUR', res['Name'], 'any', res['Version'], res['Description']]);

            if(len(pkgs) > 1):
                await self.bot.say('Reply with the name of one of the following package names within 30 seconds to get more information.');
                
            else:
                return await self.bot.say('No results found.');



    @commands.command(description='Return a link to the source code.')
    async def source(self):
        """Post a link to the bot source code."""
        source = "https://github.com/XNBlank/sudoBot";
        await self.bot.say(source);
