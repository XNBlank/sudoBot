import discord;
from discord.ext import commands;
import textwrap;
from PIL import Image;
from PIL import ImageDraw;
from PIL import ImageFont;
import asyncio, aiohttp, io, time, imghdr, os, json;

class Fun:
    """
    Commands that are used for fun.
    """

    def __init__(self, bot, config):
        self.bot = bot;
        self.config = config;

    @commands.group(pass_context=True)
    async def cow(self, ctx):
        """A speaking/thinking cow"""
        print(ctx.message.content);
        if ctx.invoked_subcommand is None:
            return await self.bot.say('Invalid amount of arguments passed.');

    @cow.command()
    async def think(self, *, message : str):
        cow = self.build_box(message, 40) + self.build_thinkcow();

        return await self.bot.say('```txt\n{0}```'.format(cow));

    @cow.command()
    async def say(self, *, message : str):
        cow = self.build_box(message, 40) + self.build_saycow();

        return await self.bot.say('```txt\n{0}```'.format(cow));

    @commands.command(pass_context=True)
    async def profile(self, ctx, *, user : discord.Member):
        """Get an information card on a user in this server."""

        if ctx.invoked_subcommand is None:

            _name = user.name;
            _id = user.id;
            _avatar = user.avatar_url;
            _def_avatar = user.default_avatar_url;
            _created = user.created_at;
            _nick = user.display_name;
            _discrm = user.discriminator;
            _roles = user.roles;

            _roleImages = {};

            for idy, ii in enumerate(_roles):
                try:
                    _roleImages[ii.name] = Image.open('data/images/distros/small/{0}.png'.format(ii.name.lower()));
                except:
                    print('No role icon for ' + ii.name);


            if(_avatar == ''):
                async with aiohttp.get(_def_avatar) as r:
                    image = await r.content.read();
            else:
                async with aiohttp.get(_avatar) as r:
                    image = await r.content.read();
            with open('data/users/avatars/{0}.jpg'.format(user.id),'wb') as f:
                f.write(image);

            checked = False;

            while checked == False:
                checks = 0;
                isImage = imghdr.what('data/users/avatars/{0}.jpg'.format(user.id));
                print(isImage);

                if checks > 4:
                    checked = True;

                if isImage != 'None':
                    checked = True;
                else:
                    checks += 1;

            av = Image.open('data/users/avatars/{0}.jpg'.format(user.id));
            userAvatar = av.resize((128,128), resample=Image.BILINEAR).convert('RGBA');

            print(userAvatar.mode);

            try:
                bg = Image.open('data/users/backgrounds/{0}.jpg'.format(user.id));
            except:
                try:
                    bg = Image.open('data/users/backgrounds/{0}.png'.format(user.id));
                except:
                    print('No user background found. Using default.');
                    bg = Image.open('data/images/background_default.png');

            fontFace = 'data/fonts/noto.ttf';
            fontFace_bold = 'data/fonts/noto_bold.ttf';
            fontsize = 18;
            headersize = 32;

            headerfont = ImageFont.truetype(fontFace_bold, headersize);
            font = ImageFont.truetype(fontFace, fontsize);
            desc_font = ImageFont.truetype(fontFace, 12);
            font_bold = ImageFont.truetype(fontFace_bold, fontsize);

            ### Card Background ###

            cardbg = Image.new('RGBA', (800, 500), (255, 255, 255, 255));
            d = ImageDraw.Draw(cardbg);

            # Everything here is layered.
            d.rectangle([(0,0),(800,500)], fill=(255,255,255,255));
            cardbg.paste(bg, (0,0)); # User wallpaper

            ### Card Foreground ###

            cardfg = Image.new('RGBA', (800, 500), (255,255,255,0));
            dd = ImageDraw.Draw(cardfg);

            # Info Box Top
            dd.rectangle([(200,60),(740,191)], fill=(255,255,255,224));
            dd.rectangle([(200,60),(740,134)], fill=(255,255,255,255));

            # Avatar box
            dd.rectangle([(60,60),(191,191)], fill=(80,80,80, 255));
            cardfg.paste(userAvatar, (62,62));

            # Profile Information
            dd.text((210, 64), _nick, fill=(74, 144, 226, 255), font=headerfont);
            dd.text((210, 106), '@' + _name + '#' + _discrm, fill=(74, 144, 226, 255), font=font);

            # Roles
            for idy, ii in enumerate(_roleImages):

                startx = int((270 - (30 * len(_roleImages))) / 2);

                cardfg.paste(_roleImages[ii], (337 + startx + (30 * idy),152), _roleImages[ii]);


            #Info Box Bottom
            dd.rectangle([(60,200),(740,450)], fill=(255,255,255,224));

            _answers = None;
            _questions = self.config["profile_questions"];

            try:
                with open('data/users/profiles/{0}.dat'.format(_id)) as f:
                    _answers = json.load(f);

                print(_answers);
            except Exception as error:
                print(error);
                print('User doesn\'t have a profile.');

            if (_answers != None):
                for key, quest in zip(sorted(_answers),_questions):
                    print('{0} {1}:{2}'.format(key,quest,_answers[key]));
                    if(int(key) < 5):
                        dd.text((80, 260 + ((int(key)-1) * 48)), textwrap.fill(quest,45) + "\n" + textwrap.fill(_answers[key],45), fill=(74, 144, 226, 255), font=desc_font);
                    else:
                        dd.text((410, 260 + ((int(key)-6) * 48)), textwrap.fill(quest,45) + "\n" + textwrap.fill(_answers[key],45), fill=(74, 144, 226, 255), font=desc_font);



            #cardfg = Image.alpha_composite(cardfg,userAvatar);

            card = Image.new('RGBA', (800, 500), (255,255,255,255));
            card = Image.alpha_composite(card,cardbg);
            card = Image.alpha_composite(card,cardfg);


            s = 'data/users/cards/{0}.png'.format(user.id);
            card.save(s, 'png');

            with open('data/users/cards/{0}.png'.format(user.id), 'rb') as g:
                return await self.bot.send_file(ctx.message.channel, g);

    @commands.command(pass_context=True)
    async def setprofilebg(self, ctx, *, url=""):
        """Set a profile card background image.

        Can either be a link to an image or an attachment."""
        try:
            _background = ctx.message.attachments[0]['url'];
        except:
            _background = url;

            if (_background == ""):
                return await self.bot.say('```Image or URL not found.```');

        print(_background);


        _user = ctx.message.author;

        async with aiohttp.get(_background) as r:
            image = await r.content.read();

        with open('data/users/backgrounds/{0}.png'.format(_user.id),'wb') as f:
            f.write(image);

            isImage = imghdr.what('data/users/backgrounds/{0}.png'.format(_user.id));
            print(isImage);

            if(isImage == 'png' or isImage == 'jpeg'):
                return await self.bot.say('```Successfully set profile wallpaper```');
            else:
                f.close();
                os.remove('data/users/backgrounds/{0}.png'.format(_user.id));
                return await self.bot.say('```Something went wrong when setting your wallpaper. Perhaps the file you sent wasn\'t an image?```');


    @commands.command(pass_context=True)
    async def profilesetup(self, ctx):
        """Setup your profile card"""

        questions = self.config["profile_questions"];
        answers = {};

        await self.bot.send_message(ctx.message.author, 'Hello! I\'m here to help you set up your profile. I will ask you a few questions that you may answer. If you don\'t want to answer, you may reply with `skip` to pass the question.');

        for idx, i in enumerate(questions):
            await self.bot.send_message(ctx.message.author, i);
            _answer = await self.bot.wait_for_message(timeout=30.0, author=ctx.message.author);

            if(_answer == None):
                return await self.bot.send_message(ctx.message.author, 'Sorry. You seemed to have timed out. Send the command again to restart the setup process.');
            elif(_answer.content == 'skip'):
                answers[idx] = 'N/A';
            else:
                answers[idx] = _answer.content;

            print(answers[idx]);
            print(answers);

        with open('data/users/profiles/{0}.dat'.format(ctx.message.author.id), 'w', encoding='utf8') as f:
            json.dump(answers, f);

        return await self.bot.send_message(ctx.message.author, 'You have completed the setup process.');

    # Cowsay code used from https://github.com/jcn/cowsay-py

    def build_saycow(self):
        return """
         \   ^__^
          \  (oo)\_______
             (__)\       )\/\\
                 ||----w |
                 ||     ||
        """;

    def build_thinkcow(self):
        return """
         o   ^__^
          o  (oo)\_______
             (__)\       )\/\\
                 ||----w |
                 ||     ||
        """;

    def build_box(self, str, length=40):
        bubble = [];

        lines = self.normalize_text(str, length);

        bordersize = len(lines[0]);

        bubble.append("  "  + "_" * bordersize);

        for index, line in enumerate(lines):
            border = self.get_border(lines, index);

            bubble.append("%s %s %s" % (border[0], line, border[1]));

        bubble.append("  " + "-" * bordersize);

        return "\n".join(bubble);

    def normalize_text(self, str, length):
        lines  = textwrap.wrap(str, length)
        maxlen = len(max(lines, key=len))
        return [ line.ljust(maxlen) for line in lines ]

    def get_border(self, lines, index):
        if len(lines) < 2:
            return [ "<", ">" ];

        elif index == 0:
            return [ "/", "\\" ];

        elif index == len(lines) - 1:
            return [ "\\", "/" ];

        else:
            return [ "|", "|" ];
