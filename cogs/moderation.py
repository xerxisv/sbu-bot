import datetime

import discord
import humanfriendly
from discord.ext import commands

from utils.config.config import ConfigHandler
from utils.error_utils import log_error

config = ConfigHandler().get_config()


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(config['mod_role_id'])
    async def ban(self, ctx: commands.Context, user: discord.User, *, reason=None):
        if ctx.guild.get_member(user.id):
            try:  # DM user if banning was successful
                await user.send("You have been banned from SBU for " + str(reason))
                await user.send(r"Appeal at https://discord.gg/mn6kJrJuVB")
            except discord.HTTPException:
                await ctx.send("User cannot be dmed")
            except Exception as exception:
                await log_error(ctx, exception)

        try:  # Check for any permission errors
            await ctx.guild.ban(user=user, delete_message_days=0, reason=reason)
        except discord.Forbidden:
            embed = discord.Embed(
                title='Error',
                description='Bot does not have permission to ban this member.',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        # Send to action log
        channel = ctx.guild.get_channel(config['moderation']['action_log_channel_id'])
        author = ctx.message.author.id

        message = f"Moderator: <@{author}> \n User: <@{user.id}> | {user} \n Action: Ban \n Reason: {reason}"
        await channel.send(message)

        # Send confirmation
        embed = discord.Embed(
            description=f"Moderator: <@{author}> \nUser: {user} "
                        f"\nAction: Ban \nReason: {reason}",
            color=config['colors']['secondary']
        )
        await ctx.reply(embed=embed)

    @ban.error
    async def ban_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+ban <@mention | ID> [reason]`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_role(config['mod_role_id'])
    async def unban(self, ctx: commands.Context, user: discord.User, *, reason=None):
        try:
            await ctx.guild.unban(user=user, reason=reason)
        except discord.HTTPException:
            embed = discord.Embed(
                title='Error',
                description="Bot does not have permission to unban this member.",
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        message = f"Moderator: <@{ctx.author.id}> \n User: <@{user.id}> | {user} \n Action: unban \n Reason: {reason}"
        await ctx.guild.get_channel(config['moderation']['action_log_channel_id']).send(message)
        embed = discord.Embed(
            description=f"Moderator: <@{ctx.author.id}> \nUser: {user} "
                        f"\nAction: unban \nReason: {reason}",
            color=config['colors']['secondary']
        )
        await ctx.send(embed=embed)

    @unban.error
    async def unban_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+unban <@mention | ID> [reason]`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_role(config['jr_mod_role_id'])
    async def mute(self, ctx: commands.Context, member: discord.Member, timespan: str, *, reason: str = None):
        # Convert time inputted to seconds
        try:
            timespan = humanfriendly.parse_timespan(timespan)
        except humanfriendly.InvalidTimespan:
            raise commands.BadArgument

        if timespan > (28 * 86400):
            embed = discord.Embed(
                title='Error',
                description='Max mute duration is 28 days',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        if member.get_role(config['jr_mod_role_id']) and member.id != ctx.author.id:
            embed = discord.Embed(
                title='Error',
                description='You cannot mute other staff members',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        duration = datetime.timedelta(seconds=timespan)

        await member.timeout_for(duration=duration, reason=reason)
        await ctx.reply(f"{member.mention} has been muted for {duration} | Reason {reason}")

        await ctx.guild.get_channel(config['moderation']['action_log_channel_id']).send(
            f"Moderator: <@{ctx.message.author.id}> \n"
            f"User: <@{member.id}> \n"
            f"Action: Mute \n"
            f"Duration: {duration} \n"
            f"Reason: {reason}")

        await member.send("You have been muted in Skyblock University.\n\n"
                          "If you would like to appeal your mute, please DM <@575252669443211264>")

    @mute.error
    async def mute_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+mute <@mention | ID> <time> <reason>`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_role(config['jr_mod_role_id'])
    async def unmute(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        await member.remove_timeout(reason=reason)
        await ctx.send(f"{member.mention} has been unmuted.")

        await ctx.guild \
            .get_channel(config['moderation']['action_log_channel_id']) \
            .send(f"Moderator: {ctx.message.author.mention} \n"
                  f"User: {member.mention} \n"
                  f"Action: Unmute \n"
                  f"Reason: {reason}")

    @unmute.error
    async def unmute_error(self, ctx, exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+unmute <@mention | ID> [reason]`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if is_warn(message.content):
            await handle_warn(message)


async def handle_warn(message: discord.Message):
    if message.author.get_role(config['jr_mod_role_id']) is None:
        return
    # Split the message on every space character
    split_msg = message.content.split(' ')
    # If the message is less than 2 words long then it's an invalid warn command, return
    if len(split_msg) < 3:
        return

    # Else remove the discord formatting characters from the mention
    user_id = split_msg[1].replace('<', '').replace('@', '').replace('>', '')

    # And check if it was indeed a mention
    if not user_id.isnumeric():
        return

    # Fetch the member with the specified ID
    member: discord.Member = message.guild.get_member(int(user_id))

    if member is None or member.get_role(config['jr_mod_role_id']) is not None:
        return

    await message.guild.get_channel(config['moderation']['action_log_channel_id']).send(
        f"Moderator: {message.author.mention} \n"
        f"User: {member.mention} \n"
        f"Action: Warn \n"
        f"Reason: {' '.join(split_msg[2:])}")

    await message.channel.send("Log created")


def is_warn(message: str):
    return message.startswith("!warn")


def setup(bot):
    bot.add_cog(Moderation(bot))
