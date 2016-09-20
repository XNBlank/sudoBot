from discord.ext import commands
import discord.utils

# This was borrowed from Danny's RoboDanny. https://github.com/Rapptz/RoboDanny

def is_owner_check(message):
    return message.author.id == '68847303431041024'

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))

def check_permissions(ctx, perms):
    msg = ctx.message
    if is_owner_check(msg):
        return True

    ch = msg.channel
    author = msg.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())

def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True

    ch = ctx.message.channel
    author = ctx.message.author
    if ch.is_private:
        return False

    role = discord.utils.find(check, author.roles)
    return role is not None

def mod_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name in ('Moderator', 'Admin'), **perms)

    return commands.check(predicate)

def admin_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name in ('Moderator', 'Admin'), **perms)

    return commands.check(predicate)
