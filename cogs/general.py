import discord;
from discord.ext import commands;
import aiohttp;
import json;

class General:
    """ General commands from sudobotPy. """

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
        """Leave a distribution role that is currently assigned to you.
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

    @commands.command(pass_context=True)
    async def pacman(self, ctx, cmd=None, *, query=None):
        """Pacman commands.
        ```
        ```tex
        Commands :
        # -Ss [query] > searches the arch and aur repositories."""
        if cmd == '-Ss':

            if query is None:
                return await self.bot.say('Invalid amount of arguments passed.');

            print('Searching for {0} in Arch repositories and the AUR.'.format(query));

            await self.bot.say('Searching for {0} in Arch repositories and the AUR.'.format(query));

            pkgs = [['Name','Repo','Arch']];
            pkgsinfos = [['Name','Repo','Arch','Version','Description','URL']];

            async with aiohttp.get('https://www.archlinux.org/packages/search/json/?q={0}'.format(query)) as r:
                ar = await r.json();
                ar = ar['results'];
                print(len(ar));
                for count, res in enumerate(ar):
                    if count < 15:
                        if not res['pkgname'] in pkgs and not res['arch'] in pkgs:
                            pkgs.append([res['pkgname'],res['repo'],res['arch']]);
                            pkgsinfos.append([res['pkgname'],res['repo'],res['arch'],res['pkgver']+"-"+res['pkgrel'],res['pkgdesc'],res['url']]);
                        else:
                            count -= 1;

            async with aiohttp.get('http://aur4.archlinux.org/rpc.php?type=search&arg={0}'.format(query)) as u:
                au = await u.json();
                au = au['results'];
                print(len(au));
                for count, res in enumerate(au):
                    if count < 10:
                        if not res['Name'] in pkgs:
                            pkgs.append([res['Name'],'AUR','any']);
                            pkgsinfos.append([res['Name'],'AUR','any',res['Version'],res['Description'],res['URL']]);
                        else:
                            count -= 1;

                print(pkgs);

                if(len(pkgs) > 1):
                    result = '```tex\n';
                    for cnt, i in enumerate(pkgs):
                        if cnt < 25:
                            if cnt == 0:
                                result += '$ ' + 'Repo : ' + i[1] + ' | Arch : ' + i[2] + ' | Name : ' + i[0] + '$\n';
                            else:
                                result += '# ' + 'Repo : ' + i[1] + ' | Arch : ' + i[2] + ' | Name : ' + i[0] + '\n';

                    await self.bot.say('Reply with the name of one of the following package names and architecture (i686 or x86_64) within 20 seconds to get more information.');
                    await self.bot.say(result + '\n```');

                    def reply_check(m):
                        print('Content of m : ' + m);
                        m = m.split();
                        if len(m) < 2:
                            m.append('x86_64');
                        print(m[0] + ' / ' + m[1]);
                        if m[1] != 'i686' and m[1] != 'x86_64':
                            m[1] = 'x86_64';
                        for j in pkgs:
                            if m[0] in j[0]:
                                return [True,m[1],m[0]];

                    userReply = await self.bot.wait_for_message(timeout=20.0, author= ctx.message.author);

                    try:
                        replyMatch = reply_check(userReply.content);
                        print(replyMatch);
                    except Exception as error:
                        print(error);
                        print('Most likely a time-out.');

                    if userReply is None:
                        await self.bot.say('Timed out.');
                        return;
                    elif replyMatch[0] == True:
                        for j in pkgsinfos:
                            print('Checking...');

                            if replyMatch[2] in j:
                                print('Found package!');
                                print(j);
                                pName = replyMatch[2];
                                if 'AUR' in j:
                                    print('IS IN AUR');
                                    pVersion = j[3];
                                    pDescription = j[4];
                                    pSourceURL = j[5];
                                    pURL = 'https://aur.archlinux.org/packages/' + pName;

                                    await self.bot.say('Info on : {0}\n```tex\n# Package Name : {0}\n# Version : {1}\n# Description : {2}\n# Source : {3}\n# AUR : {4}```'.format(pName, pVersion, pDescription, pSourceURL, pURL));
                                    return;
                                else:
                                    print('IS IN ARCH REPO');
                                    pVersion = j[3];
                                    pDescription = j[4];
                                    pArch = replyMatch[1];
                                    pRepo = j[1];
                                    pSourceURL = j[5];

                                    await self.bot.say('Info on : {0}\n```tex\n# Package Name : {0}\n# Version : {1}\n# Description : {2}\n# Arch : {3}\n# Repo : {4}\n# Source : {5}```'.format(pName, pVersion, pDescription, pArch, pRepo, pSourceURL));
                                    return;
                    else:
                        return await self.bot.say('Previous search was exited.');

                else:
                    return await self.bot.say('No results found.');
        elif cmd != "-Ss" or cmd == None:
            return await self.bot.say('Invalid arguments passed.');



    @commands.command(description='Return a link to the source code.')
    async def source(self):
        """Post a link to the bot source code."""
        source = "https://github.com/XNBlank/sudoBot";
        await self.bot.say(source);
