import discord
from discord.ext import commands
from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont
import asyncio, aiohttp, io, time, imghdr, os, json, textwrap, re

class Profile:
    """
    Profile card setup and display
    """

    def __init__(self, client, config):
        self.client = client
        self.config = config

    @commands.group(pass_context=True)
    async def profile(self, ctx):
        """Profile command ( see 'sudo help profile' for more info )"""

        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid profile command passed... Send `sudo help profile` for assistance.')


    @profile.command(pass_context=True)
    async def get(self, ctx, user : discord.Member = None):
        """Get a user profile card. Passing no arguments returns requesters card"""
        if user == None:
            user = ctx.message.author

        name = user.name
        userid = user.id
        avatar = user.avatar_url
        def_avatar = user.default_avatar_url
        created = user.created_at
        nick = user.display_name
        discr = user.discriminator
        roles = user.roles

        roleImages = {}

        for x, role in enumerate(roles):
            try:
                roleImages[role.name] = Image.open('data/images/roles/small/{}.png'.format(role.name.lower()))
            except Exception as e:
                next

        if avatar == '':
            async with aiohttp.ClientSession() as session:
                async with session.get(def_avatar) as r:
                    image = await r.content.read()
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar) as r:
                    image = await r.content.read()
        with open('data/users/avatars/{}.png'.format(user.id), 'wb') as f:
            f.write(image)
        
        checked = False

        while checked == False:
            checks = 0
            isImage = imghdr.what('data/users/avatars/{}.png'.format(user.id))

            if checks > 4:
                checked = True
            
            if isImage != 'None':
                checked = True
            else:
                checks += 1
        
        av = Image.open('data/users/avatars/{}.png'.format(user.id))
        userAvatar = av.resize((128,128), resample=Image.BILINEAR).convert('RGBA')
        maxsize = ( 800, 500 )
        try:
            bg = Image.open('data/users/backgrounds/{0}.png'.format(user.id))
            bg_width, bg_height = bg.size

            bg = ImageOps.fit(bg,maxsize)

            # bg.thumbnail( maxsize )
        except Exception as e:
            raise Exception(e)
            bg = Image.open('data/images/background_default.png')

        fontFace = 'data/fonts/{}'.format(self.config['fonts']['normal'])
        fontFace_bold = 'data/fonts/{}'.format(self.config['fonts']['bold'])
        fontSize = 18
        descSize = 12
        headerSize = 32

        header_font = ImageFont.truetype(fontFace_bold, headerSize)
        font = ImageFont.truetype(fontFace, fontSize)
        desc_font = ImageFont.truetype(fontFace, descSize)
        font_bold = font = ImageFont.truetype(fontFace_bold, fontSize)

        cardbg = Image.new('RGBA', (800, 500), (255,255,255,255))
        d = ImageDraw.Draw(cardbg)

        d.rectangle([(0,0), 800,500], fill=(255,255,255,255))
        cardbg.paste(bg, (0,0))

        cardfg = Image.new('RGBA', (800, 500), (255,255,255,0))
        dd = ImageDraw.Draw(cardfg)

        # Info Box Top
        dd.rectangle([(200,60),(740,191)], fill=(255,255,255,224));
        dd.rectangle([(200,60),(740,134)], fill=(255,255,255,255));

        # Avatar box
        dd.rectangle([(60,60),(191,191)], fill=(80,80,80, 255));
        cardfg.paste(userAvatar, (62,62));

        # Profile Information
        dd.text((210, 64), nick, fill=(74, 144, 226, 255), font=header_font);
        dd.text((210, 106), '@' + name + '#' + discr, fill=(74, 144, 226, 255), font=font);

        # Roles
        for idy, ii in enumerate(roleImages):

            startx = int((270 - (30 * len(roleImages))) / 2);

            cardfg.paste(roleImages[ii], (337 + startx + (30 * idy),152), roleImages[ii]);


        #Info Box Bottom
        dd.rectangle([(60,200),(740,450)], fill=(255,255,255,224));

        answers = None;
        questions = self.config["profile_questions"];

        try:
            with open('data/users/profiles/{}.dat'.format(userid)) as f:
                answers = json.load(f);
        except Exception as e:
            pass

        if (answers != None):
            for key, quest in zip(sorted(answers),questions):
                if(int(key) < 5):
                    dd.text((80, 260 + ((int(key)-1) * 48)), textwrap.fill(quest,50) + "\n" + textwrap.fill(answers[key],50), fill=(74, 144, 226, 255), font=desc_font);
                else:
                    dd.text((410, 260 + ((int(key)-6) * 48)), textwrap.fill(quest,50) + "\n" + textwrap.fill(answers[key],50), fill=(74, 144, 226, 255), font=desc_font);


        card = Image.new('RGBA', (800, 500), (255,255,255,255));
        card = Image.alpha_composite(card,cardbg);
        card = Image.alpha_composite(card,cardfg);

        s = 'data/users/cards/{0}.png'.format(user.id);
        card.save(s, 'png');

        with open('data/users/cards/{0}.png'.format(user.id), 'rb') as g:
            return await ctx.message.channel.send(file=discord.File(g));

    @profile.command(pass_context=True)
    async def setup(self, ctx):
        """Set your user profile card."""
        await ctx.send('Sending a PM to setup profile card.')

        questions = self.config["profile_questions"]
        answers = {}

        recipient = ctx.message.author

        await recipient.send("Hello! I'm here to help you set up your profile. I will ask you a few questions that you may answer. If you don't want to answer the question, you may reply with 'skip' to move on.")

        for x, question in enumerate(questions):
            await recipient.send(question)

            def check(m):
                try:
                    return m.channel.recipient.id == recipient.id and m.author.id == recipient.id
                except:
                    return False


            answer = await self.client.wait_for('message', check=check)
            if answer.content.lower() == 'skip':
                answers[x] = 'N/A'
            else:
                answers[x] = answer.content
        
        with open('data/users/profiles/{}.dat'.format(recipient.id), 'w', encoding='utf8') as f:
            json.dump(answers, f)
        
        return await recipient.send('You have completed your profile setup')

    @profile.command(pass_context=True)
    async def wallpaper(self, ctx, *, url=""):
        """Set a profile card background image.

        Can either be a link to an image or an attachment."""
        try:
            background = ctx.message.attachments[0].url
        except:
            background = url

            if (background == ""):
                return await ctx.send('```Image or URL not found.```')

        user = ctx.message.author
        async with aiohttp.ClientSession() as session:
            async with session.get(background) as r:
                image = await r.content.read()

        with open('data/users/backgrounds/{0}.png'.format(user.id),'wb') as f:
            f.write(image)

            isImage = imghdr.what('data/users/backgrounds/{0}.png'.format(user.id))

            if(isImage == 'png' or isImage == 'jpeg' or isImage == 'jpg' or isImage == 'gif'):
                f.close()
                return await ctx.send('```Successfully set profile wallpaper```')
            else:
                f.close()
                os.remove('data/users/backgrounds/{0}.png'.format(user.id))
                return await ctx.send('```Something went wrong when setting your wallpaper. Perhaps the file you sent wasn\'t an image?```')


def setup(client):
    client.add_cog(Profile(client, client.config))
