# TODO create command that adds channels to crisis
import discord
from discord.ext import commands

from utils.constants import CRISIS_IGNORED_CATEGORIES, CRISIS_IGNORED_ROLES, CRISIS_REMOVE_VIEW_PERMS_CHANNELS, \
    EVERYONE_ROLE_ID, JR_ADMIN_ROLE_ID, SBU_ERROR, SBU_GOLD, SBU_PURPLE, SBU_SUCCESS

CHANNEL_CHANGES: dict[int, list[int]] = {}
TICKET_CHANNEL_CHANGES: dict[int, list[int]] = {}

errors: list[tuple[str, str]] = []
locked_channels = []

is_crisis_active = False
is_crisis_loading = False


async def secure_everyone_role(everyone_role: discord.Role):
    everyone_perms = everyone_role.permissions

    # remove message perms from @everyone
    everyone_perms.update(send_messages=False, send_messages_in_threads=False, connect=False)
    await everyone_role.edit(permissions=everyone_perms)


async def restore_everyone_role(ctx: commands.Context):
    # Restore everyone role
    try:
        everyone_perms = ctx.guild.get_role(EVERYONE_ROLE_ID).permissions
        everyone_perms.update(send_messages=True, send_messages_in_threads=True, connect=True)

        await ctx.guild.get_role(EVERYONE_ROLE_ID).edit(permissions=everyone_perms)
    except discord.HTTPException as exception:
        errors.append((exception.text, '`@everyone`'))


async def secure_ticket_channels(ctx: commands.Context, everyone_role: discord.Role):
    # remove viewing perms from ticket creation channels
    for channel_id in CRISIS_REMOVE_VIEW_PERMS_CHANNELS:
        try:
            channel: discord.TextChannel = ctx.guild.get_channel(channel_id)
            overwrites = channel.overwrites
        except AttributeError as exception:
            errors.append((exception.name, channel_id))
            continue

        TICKET_CHANNEL_CHANGES[channel_id] = []

        if overwrites[everyone_role].view_channel is not False:
            overwrites[everyone_role].update(view_channel=False)  # Remove viewing perms from everyone
            TICKET_CHANNEL_CHANGES[channel_id].append(EVERYONE_ROLE_ID)

        for role in overwrites:  # Iterate through the channel's overwrites
            if role.id in CRISIS_IGNORED_ROLES:  # Skip any of the ignored roles
                continue
            if overwrites[role].view_channel is not False:
                # Remove viewing perms
                overwrites[role].update(view_channel=False)
                TICKET_CHANNEL_CHANGES[channel_id].append(role.id)

        try:
            await channel.edit(overwrites=overwrites, name=channel.name + '-☆')
        except discord.HTTPException as exception:
            errors.append((exception.text, channel_id))
        else:
            locked_channels.append(channel.id)


async def restore_ticket_channels(ctx: commands.Context):
    # Restore ticket channels
    for channel_id in TICKET_CHANNEL_CHANGES:
        try:
            channel: discord.TextChannel = ctx.guild.get_channel(channel_id)
            overwrites = channel.overwrites

            for role_id in TICKET_CHANNEL_CHANGES[channel_id]:
                role = ctx.guild.get_role(role_id)

                if role is None:
                    continue

                overwrites[role].update(view_channel=True)

            await channel.edit(overwrites=overwrites, name=channel.name.replace('-☆', ''))

        except Exception as exception:
            errors.append((str(exception.__cause__), str(channel_id)))


async def secure_text_channels(ctx: commands.Context):
    # remove post perms overwrites from all channels
    for channel in ctx.guild.channels:
        if (channel.category is not None and channel.category.id in CRISIS_IGNORED_CATEGORIES) or \
                channel.id in CRISIS_REMOVE_VIEW_PERMS_CHANNELS:
            continue

        # flags if the overwrites have been changed
        overwrites_changed = False
        if isinstance(channel, (discord.TextChannel, discord.ForumChannel)):  # if channel is a text channel

            overwrites = channel.overwrites
            CHANNEL_CHANGES[channel.id] = []

            for role in overwrites:  # iterates through all the role/member overwrites
                if role.id in CRISIS_IGNORED_ROLES:  # ignores some default roles
                    continue

                if overwrites[role].send_messages is True:  # if there is any role that forcefully gives speaking perms
                    overwrites_changed = True  # flag the change

                    CHANNEL_CHANGES[channel.id].append(role.id)

                    overwrites[role].update(send_messages=False, send_messages_in_threads=False)

            if not overwrites_changed:  # if no change has been made
                del CHANNEL_CHANGES[channel.id]  # remove channel from changed channels
                continue

            try:  # override channel overwrites
                await channel.edit(overwrites=overwrites, name=channel.name + '-☆')
            except discord.HTTPException as exception:  # if error, add error to errors array
                errors.append((exception.text, str(channel.id)))
            else:  # if no errors, add channel to changed channels array
                locked_channels.append(channel.id)


async def restore_text_channels(ctx: commands.Context):
    # Restore the rest of the channels
    for channel_id in CHANNEL_CHANGES:
        try:
            channel = ctx.guild.get_channel(channel_id)
            overwrites = channel.overwrites

            for _id in CHANNEL_CHANGES[channel_id]:
                obj: discord.Role | discord.Member
                obj = ctx.guild.get_role(_id)
                if obj is None:
                    obj = ctx.guild.get_member(_id)
                overwrites[obj].update(send_messages=True, send_messages_in_threads=True)

            await channel.edit(overwrites=overwrites, name=channel.name.replace('-☆', ''))

        except Exception as exception:
            errors.append((str(exception), str(channel_id)))


class Raid(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name='crisis', aliases=['cannibalism', 'lockdown'])
    @commands.has_role(JR_ADMIN_ROLE_ID)
    async def crisis(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return

        await ctx.trigger_typing()

    @crisis.command(name='start', aliases=['init', 'begin'])
    @commands.cooldown(1, 600, commands.BucketType.guild)
    async def start(self, ctx: commands.Context):

        global is_crisis_active
        global is_crisis_loading

        if is_crisis_active:
            embed = discord.Embed(
                title='',
                description='A crisis is already active.',
                color=SBU_PURPLE
            )
            await ctx.reply(embed=embed)
            return

        embed = discord.Embed(
            title='',
            description='Crisis Initializing <a:loading:978732444998070304>',
            color=SBU_PURPLE
        )
        reply = await ctx.reply(embed=embed)

        # clear possible leftovers
        errors.clear()

        is_crisis_active = True
        is_crisis_loading = True

        everyone_role = ctx.guild.get_role(EVERYONE_ROLE_ID)

        await secure_everyone_role(everyone_role)

        await secure_ticket_channels(ctx, everyone_role)

        await secure_text_channels(ctx)

        embed = discord.Embed(
            title='',
            description='Crisis Initialized',
            color=SBU_SUCCESS
        )
        await reply.edit(embed=embed)
        is_crisis_loading = False

    @crisis.command(name='restore', aliases=['rs', 'rst'])
    async def restore(self, ctx: commands.Context):
        embed = discord.Embed(
            title='',
            description='Restoring Crisis Changes <a:loading:978732444998070304>',
            color=SBU_PURPLE
        )

        reply = await ctx.reply(embed=embed)

        global is_crisis_active
        global is_crisis_loading

        if not is_crisis_active:
            embed = discord.Embed(
                title='Error',
                description='No ongoing crisis',
                color=SBU_ERROR
            )
            await reply.edit(embed=embed)
            return

        if is_crisis_loading:
            embed = discord.Embed(
                title='Error',
                description='A crisis is initializing',
                color=SBU_ERROR
            )
            await reply.edit(embed=embed)
            return

        errors.clear()  # clear possible leftover errors

        await restore_everyone_role(ctx)

        await restore_ticket_channels(ctx)

        await restore_text_channels(ctx)

        embed = discord.Embed(
            title='',
            description='Crisis Restored',
            color=SBU_SUCCESS
        )
        is_crisis_active = False
        await reply.edit(embed=embed)

    @crisis.group(name='show', aliases=['print', 'list'])
    async def show(self, ctx: commands.Context):
        pass

    @show.command(name='changes', aliases=['channels'])
    async def changes(self, ctx: commands.Context):

        channels_string = 'Channels affected: \n'

        if not is_crisis_active:
            channels_string = 'No active crisis'
        elif len(locked_channels) < 1:
            channels_string = 'No channels affected'
        else:
            for index, _id in enumerate(locked_channels):
                if (index % 3) == 0:
                    channels_string += '\n'
                else:
                    channels_string += ' | '
                channels_string += f'<#{_id}>'

        embed = discord.Embed(
            title='Crisis',
            description=channels_string,
            color=SBU_GOLD
        )

        await ctx.reply(embed=embed)

    @show.command(name='errors')
    async def errors(self, ctx: commands.Context):
        errors_string = 'Errors:\n'

        if len(errors) < 1:
            errors_string = 'No errors occurred'
        else:
            for error in errors:
                errors_string += f'- *<#{error[1]}>/<@{error[1]}>*: **{error[0]}**\n'

        embed = discord.Embed(
            title='Crisis',
            description=errors_string,
            color=SBU_GOLD
        )

        await ctx.reply(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Raid(bot))
