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
    async def listdistro(self, ctx):
        """List available user distro roles."""
        _rolesList = '\n'.join(map(str, self.config["user_roles"]));

        return await self.bot.say('```List of available roles\n' + _rolesList + '\n```');


    @commands.command(pass_context=True)
    async def joindistro(self, ctx, *, distro=""):
        """Join one of the many distribution roles available."""
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

    @commands.command(pass_context=True, hidden=True)
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
                    if count < 10:
                        if not res['pkgname'] in pkgs:
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
                        if cnt < 20:
                            for _cnt, ii in enumerate(pkgsinfos):
                                if _cnt < 20:
                                    result += '# ' + 'Repo : ' + i[1] + ' | Arch : ' + i[2] + '| Name : ' + i[0] + '\n';
                                    #result += '' + i[1] + '/' + i[0] + ' (' + i[2] + ') \n';

                    await self.bot.say('Reply with the name of one of the following package names within 20 seconds to get more information.');
                    await self.bot.say(result + '\n```');

                    def reply_check(m):
                        print('Content of m : ' + m);
                        if m in pkgs:
                            return True;

                    userReply = await self.bot.wait_for_message(timeout=20.0, author= ctx.message.author);

                    try:
                        replyMatch = reply_check(userReply.content);
                    except Exception as error:
                        print(error);
                        print('Most likely a time-out.');

                    if userReply is None:
                        await self.bot.say('Timed out.');
                        return;
                    elif replyMatch == True:

                        for j in pkgsinfos:
                            print('Ready to send info. Find data.');
                            if userReply.content in j:
                                print('Found package!');
                                print(j);
                                pName = userReply.content;
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
                                    pArch = j[2];
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

    
    @commands.command(pass_context=True, no_pm=True)
    async def warnstatus(self, ctx):
        
        user = ctx.message.author;

        dataFile = 'data/warns/warns.dat';
        data = {};

        with open(dataFile, 'r', encoding='utf8') as f:
            data = json.load(f);
            print(data);
            print('closed');

        if(user.id not in data or int(data["{0}".format(user.id)] == 0)):
            await self.bot.send_message(ctx.message.channel,"You currently have 0 warning points! Good job!");
        else:
            warnCount = data["{0}".format(user.id)];
            await self.bot.send_message(ctx.message.channel,"You currently have {0} warning points.".format(warnCount));