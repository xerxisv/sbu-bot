import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import re


class Raid(commands.Cog, name="raid command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['raid'])
    @commands.has_role("Junior Administrator")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def crisis(self, ctx):
        lockdown_channels = ["general-chat", "irl-help", "birthdays", "masters-general"
            , "sb-masters-bridge", "masters-bot-commands", "masters-general"
            , "bot-commands", "verify", "count-to-59mil", "sb-uni-bridge"
            , "alpha-psi-bridge", "kappa-eta-bridge", "delta-omega-bridge"
            , "lambda-pi-bridge", "theta-tau-bridge", "rho-xi-bridge"
            , "skyblock-help-1", "skyblock-help-2", "crafting-and-reforge-assistance"
            , "essence-trading", "item-lending", "trades-and-auctions", "rep-commands"
            , "self-advertising", "smp-chat", "community-bulletin-board", "party-finder", "anime-and-manga",
                             "server-donor-chat", "staff-chat"]
        await ctx.send(":lock: Crisis mode activated. Putting channels under lockdown.")
        length = 0
        for channel in ctx.guild.channels:
            if channel.name in lockdown_channels:
                length = length + 1
                if ctx.guild.default_role not in channel.overwrites:
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
                    }
                    await channel.edit(overwrites=overwrites)
                elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[
                    ctx.guild.default_role].send_messages is None:
                    overwrites = channel.overwrites[ctx.guild.default_role]
                    overwrites.send_messages = False
                    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)

        await ctx.send(f":lock: Lockdown completed, {length} channels locked.")
        channel = get(ctx.guild.channels, name="mod-action-log")
        author = str(ctx.message.author.id)
        log1 = discord.Embed(
            title='Moderation Log',
            description='',
            colour=discord.Colour.light_gray()
        )
        log1.set_footer(text='mhm SBU bot')
        log1.add_field(name="Moderator", value="<@" + author + ">", inline=True)
        log1.add_field(name="Action", value='Server lockdown', inline=False)
        await channel.send(embed=log1)
        channel = get(ctx.guild.channels, name="admin-chat")
        raidmode = discord.Embed(
            title='Raid Mode Information',
            description='Administration information for SBU CRISIS Mode',
            colour=discord.Colour.red()
        )
        raidmode.set_footer(text='WEEWOO CRISIS MODE')
        raidmode.add_field(name="Command ran by", value=f":lock: <@{author}>", inline=False)
        raidmode.add_field(name="How many channels locked", value=f"{length}", inline=False)
        await channel.send(embed=raidmode)

    @crisis.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Insufficient Permissions")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    @commands.command(aliases=['raidend'])
    @commands.has_role("Administrator")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def crisisend(self, ctx):
        lockdown_channels = ["general-chat", "irl-help", "birthdays", "masters-general"
            , "sb-masters-bridge", "masters-bot-commands", "masters-general"
            , "bot-commands", "verify", "count-to-59mil", "sb-uni-bridge"
            , "alpha-psi-bridge", "kappa-eta-bridge", "delta-omega-bridge"
            , "lambda-pi-bridge", "theta-tau-bridge", "rho-xi-bridge"
            , "skyblock-help-1", "skyblock-help-2", "crafting-and-reforge-assistance"
            , "essence-trading", "item-lending", "trades-and-auctions", "rep-commands"
            , "self-advertising", "smp-chat", "community-bulletin-board", "party-finder", "anime-and-manga",
                             "server-donor-chat", "staff-chat"]
        await ctx.send(":unlock: Crisis mode ended. Removing channels from under lockdown.")
        length = 0
        for channel in ctx.guild.channels:
            if channel.name in lockdown_channels:
                if ctx.guild.default_role not in channel.overwrites:
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(send_messages=None)
                    }
                    await channel.edit(overwrites=overwrites)
                elif channel.overwrites[ctx.guild.default_role].send_messages == False:
                    overwrites = channel.overwrites[ctx.guild.default_role]
                    overwrites.send_messages = None
                    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
        await ctx.send(f":unlock: Lockdown end completed, {length} channels unlocked.")
        channel = get(ctx.guild.channels, name="mod-action-log")
        author = str(ctx.message.author.id)
        log1 = discord.Embed(
            title='Moderation Log',
            description='',
            colour=discord.Colour.light_gray()
        )
        log1.set_footer(text='mhm SBU bot')
        log1.add_field(name="Moderator", value="<@" + author + ">", inline=True)
        log1.add_field(name="Action", value='Server lockdown Remove', inline=False)
        await channel.send(embed=log1)
        channel = get(ctx.guild.channels, name="admin-chat")
        raidmode = discord.Embed(
            title='Raid Mode Information',
            description='Administration information for SBU CRISIS Mode',
            colour=discord.Colour.red()
        )
        raidmode.set_footer(text='WEEWOO CRISIS MODE')
        raidmode.add_field(name="Command ran by", value=f":unlock: <@{author}>", inline=False)
        raidmode.add_field(name="How many channels unlocked", value=f"{length}", inline=False)
        raidmode.add_field(name="Errors unlocking Channels", value=f"None", inline=False)
        await channel.send(embed=raidmode)

    @crisisend.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Insufficient Permissions")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    @commands.command()
    @commands.has_role("Junior Administrator")
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def lock(self, ctx, channel=None):
        if channel:
            channel = re.findall(r'\d+', channel)  # Get only numbers from channel
            channel = self.bot.get_channel(int(channel[0]))
        else:
            channel = ctx.channel

        if channel:
            await channel.edit(name=f"🔒-{channel.name}")
            perms = channel.overwrites_for(ctx.guild.default_role)
            perms.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=perms)

            embed = discord.Embed(
                description=f"<#{channel.id}> Locked Successfully", color=0x2fa737)  # Green
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"Channel Not Found", color=discord.Colour.red())
            await ctx.channel.send(embed=embed)

    @lock.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Insufficient Permissions")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    @commands.command()
    @commands.has_role("Junior Administrator")
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def unlock(self, ctx, channel=None):
        if channel:
            channel = re.findall(r'\d+', channel)  # Get only numbers from channel
            channel = self.bot.get_channel(int(channel[0]))
        else:
            channel = ctx.channel

        if channel:
            await channel.edit(name=channel.name.replace("🔒-", "", 1))

            perms = channel.overwrites_for(ctx.guild.default_role)
            perms.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=perms)

            embed = discord.Embed(
                description=f"<#{channel.id}> Unlocked Successfully", color=0x2fa737)  # Green
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"Channel Not Found", color=discord.Colour.red())
            await ctx.channel.send(embed=embed)

    @unlock.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Insufficient Permissions")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)


def setup(bot):
    bot.add_cog(Raid(bot))
