import discord
from discord.ext import commands
import json

class Roles:
    """
    Role relaated Commands
    """

    def __init__(self, client, config):
        self.client = client
        self.config = config

    @commands.command(pass_context=True)
    async def listdistro(self, ctx):
        """List available joinable user roles."""
        _rolesList = '\n'.join(map(str, self.config["user_roles"]))

        return await ctx.send('```List of available roles\n' + _rolesList + '\n```')

    @commands.command(pass_context=True)
    async def joindistro(self, ctx, *, distro : str):
        """Add yourself to a joinable user role."""
        server = ctx.message.guild
        member = ctx.message.author

        if distro.lower() == 'redhat':
            distro = 'Red Hat'

        roles = self.config["user_roles"]

        serverRoles = []
        memberRoles = []

        for _id, role in enumerate(server.roles):
            serverRoles.append(role.name)

        for _id, role in enumerate(member.roles):
            memberRoles.append(role.name)

        if distro.lower() in map(str.lower, serverRoles):
            if distro.lower() in map(str.lower, roles):
                if distro.lower() in map(str.lower, memberRoles):
                    return await ctx.send("You're already in that role.")
                else:
                    try:
                        lowarr = [item.lower() for item in serverRoles]
                        index = lowarr.index(distro.lower())
                        newrole = discord.utils.get(ctx.message.guild.roles, name=serverRoles[index])
                        await member.add_roles(newrole, reason="Added by user command.")
                        return await ctx.send("Added {} to group {}.".format(member.display_name, newrole.name))
                    except Exception as e:
                        raise Exception(e)
                        return
            else:
                return await ctx.send("That role doesn't exist.")
        else:
            return await ctx.send("That role doesn't exist.")


    @commands.command(pass_context=True)
    async def distrostats(self, ctx, *, rolename : str=None):
        """Show role statistics"""
        server = ctx.message.guild
        roles = self.config["user_roles"]
        emotes = {}

        serverRoles = []
        for _id, role in enumerate(server.roles):
            serverRoles.append(role.name)

        for _id, emote in enumerate(server.emojis):
            name = emote.name
            name.replace(" ","")
            emotes[str(name)] = emote.url

        role = rolename
        if ( role != None ):
            if ( role.lower() in map(str.lower, roles) ):
                lowarr = [item.lower() for item in serverRoles]
                index = lowarr.index(role.lower())
                thisrole = discord.utils.get(ctx.message.guild.roles, name=serverRoles[index])
                if ( thisrole != None ):
                    try:
                        image = emotes[thisrole.name.lower()]
                    except:
                        image = ''
                    embed = discord.Embed(title=thisrole.name, color = thisrole.colour)
                    embed.set_thumbnail(url=image)
                    embed.add_field(name = "Member Count", value = "{}".format(len(thisrole.members), inline=True))
                    embed.add_field(name = "Color (RGB)", value = "({},{},{})".format(thisrole.colour.r, thisrole.colour.g, thisrole.colour.b))
                    return await ctx.send(embed = embed) 
            else:
                return await ctx.send("That role doesn't exist or is not a public role.")
        else:
            stats = []
            string = ""
            for role in roles:
                lowarr = [item.lower() for item in serverRoles]
                index = lowarr.index(role.lower())
                thisrole = discord.utils.get(ctx.message.guild.roles, name=serverRoles[index])
                if ( thisrole != None ):
                    stats.append(thisrole)
            stats.sort(key=lambda x: len(x.members), reverse=True)
            embed = discord.Embed(title="Distro Statistics")
            for role in stats:
                try:
                    image = emotes[role.name.lower()]
                except:
                    image = ''
                embed.add_field(name = "{}".format(role.name), value = "{}".format(len(role.members)), inline=False)

            return await ctx.send(embed = embed)

    @commands.command(pass_context=True)
    async def leavedistro(self, ctx, *, distro : str):
        """Remove yourself to a joinable user role."""
        server = ctx.message.guild
        member = ctx.message.author

        if distro.lower() == 'redhat':
            distro = 'Red Hat'

        roles = self.config["user_roles"]

        serverRoles = []
        memberRoles = []

        for _id, role in enumerate(server.roles):
            serverRoles.append(role.name)

        for _id, role in enumerate(member.roles):
            memberRoles.append(role.name)

        if distro.lower() in map(str.lower, serverRoles):
            if distro.lower() in map(str.lower, roles):
                if distro.lower() in map(str.lower, memberRoles):
                    try:
                        lowarr = [item.lower() for item in serverRoles]
                        index = lowarr.index(distro.lower())
                        deletedrole = discord.utils.get(ctx.message.guild.roles, name=serverRoles[index])
                        await member.remove_roles(deletedrole, reason="Removed by user command.")
                        return await ctx.send("Removed {} from group {}.".format(member.display_name, deletedrole.name))
                    except Exception as e:
                        raise Exception(e)
                        return
                else:
                    return await ctx.send("You're not in that role.")
            else:
                return await ctx.send("That role doesn't exist.")
        else:
            return await ctx.send("That role doesn't exist.")

def setup(client):
    client.add_cog(Roles(client, client.config))
