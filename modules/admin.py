import discord
from discord.ext import commands
import json

class Admin:
    """
    Admin commands
    """

    conf = {}

    async def is_owner(ctx):
        global conf
        return ctx.message.author.id in conf["owner_ids"]

    def __init__(self, client, config):
        self.client = client
        self.config = config
        global conf
        conf = config

    @commands.command(hidden=True, pass_context=True)
    @commands.check(is_owner)
    async def load(self, ctx, extension_name : str):
        """Loads an extension."""
        try:
            self.client.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            raise Exception(e)
            return
        await ctx.send("{} loaded.".format(extension_name))

    @load.error
    async def load_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("{} is not in the sudoers file. This incident will be reported.".format(ctx.author.display_name))

    @commands.command(hidden=True, pass_context=True)
    @commands.check(is_owner)
    async def reload(self, ctx, extension_name : str):
        """Reloads an extension."""
        try:
            self.client.unload_extension(extension_name)
            self.client.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            raise Exception(e)
            return
        await ctx.send("{} reloaded.".format(extension_name))

    @reload.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("{} is not in the sudoers file. This incident will be reported.".format(ctx.author.display_name))

    @commands.command(hidden=True, pass_context=True)
    @commands.check(is_owner)
    async def reloadconf(self, ctx):
        """Reloads the config."""
        try:
            for module in self.config['modules']:
                try:
                    if module != 'admin':
                        self.client.unload_extension("modules." + module)
                except Exception as e:
                    raise Exception(e)

            with open('./config.json', 'r') as cjson:
                self.client.config = json.load(cjson)
                self.config = self.client.config
                global conf
                conf = self.config

            for module in self.config['modules']:
                try:
                    if module != 'admin':
                        self.client.load_extension("modules." + module)
                except Exception as e:
                    raise Exception(e)

        except (AttributeError, ImportError) as e:
            raise Exception(e)
            return
        await ctx.send("config reloaded.")

    @reloadconf.error
    async def reloadconf_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("{} is not in the sudoers file. This incident will be reported.".format(ctx.author.display_name))

    @commands.command(hidden=True, pass_context=True)
    @commands.check(is_owner)
    async def unload(self, ctx, extension_name : str):
        """Unloads an extension."""
        if extension_name.lower() == 'modules.admin':
            return await ctx.send("Cannot unload essential module : {}".format(extension_name))
        self.client.unload_extension(extension_name)
        await ctx.send("{} unloaded.".format(extension_name))

    @unload.error
    async def unload_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("{} is not in the sudoers file. This incident will be reported.".format(ctx.author.display_name))

def setup(client):
    client.add_cog(Admin(client, client.config))