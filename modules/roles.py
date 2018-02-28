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
            serverRoles.append(role.name.lower())

        for _id, role in enumerate(member.roles):
            memberRoles.append(role.name.lower())

        if distro.lower() in serverRoles:
            if distro.lower() in roles:
                if distro.lower() in memberRoles:
                    return await ctx.send("You're already in that role.")
                else:
                    try:
                        newrole = discord.utils.get(ctx.message.guild.roles, name=distro.title())
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
            serverRoles.append(role.name.lower())

        for _id, role in enumerate(member.roles):
            memberRoles.append(role.name.lower())

        if distro.lower() in serverRoles:
            if distro.lower() in roles:
                if distro.lower() in memberRoles:
                    try:
                        deletedrole = discord.utils.get(ctx.message.guild.roles, name=distro.title())
                        await member.remove_roles(newrole, reason="Removed by user command.")
                        return await ctx.send("Removed {} from group {}.".format(member.display_name, newrole.name))
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
