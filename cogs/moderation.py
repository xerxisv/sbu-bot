import datetime

import discord
import humanfriendly
from discord.ext import commands

from utils.constants import JR_MOD_ROLE_ID, MODERATOR_ROLE_ID, MOD_ACTION_LOG_CHANNEL_ID
from utils.error_utils import log_error


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(MODERATOR_ROLE_ID)
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
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        # Send to action log
        channel = ctx.guild.get_channel(MOD_ACTION_LOG_CHANNEL_ID)
        author = ctx.message.author.id

        message = f"Moderator: <@{author}> \n User: <@{user.id}> | {user} \n Action: Ban \n Reason: {reason}"
        await channel.send(message)

        # Send confirmation
        embed = discord.Embed(description=f"Moderator: <@{author}> \nUser: {user} "
                                          f"\nAction: Ban \nReason: {reason}")
        await ctx.reply(embed=embed)
        # channel = self.bot.get_channel(946591422616838264)
        # await channel.send(f"Ban command ran by <@{author}> banning <@{user.id}>")

    @ban.error
    async def ban_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+ban <@mention | ID> [reason]`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def unban(self, ctx: commands.Context, user: discord.User, *, reason=None):
        try:
            await ctx.guild.unban(user=user, reason=reason)
        except discord.HTTPException:
            embed = discord.Embed(
                title='Error',
                description="Bot does not have permission to unban this member.",
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        message = f"Moderator: <@{ctx.author.id}> \n User: <@{user.id}> | {user} \n Action: unban \n Reason: {reason}"
        await ctx.guild.get_channel(MOD_ACTION_LOG_CHANNEL_ID).send(message)
        embed = discord.Embed(description=f"Moderator: <@{ctx.author.id}> \nUser: {user} "
                                          f"\nAction: unban \nReason: {reason}")
        await ctx.send(embed=embed)
        # channel = self.bot.get_channel(946591422616838264)
        # await channel.send(f"Unban command ran by <@{ctx.author.id}> unbanning <@{member.id}>")

    @unban.error
    async def unban_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+unban <@mention | ID> [reason]`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_role(JR_MOD_ROLE_ID)
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
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        if member.get_role(JR_MOD_ROLE_ID) and member.id != ctx.author.id:
            embed = discord.Embed(
                title='Error',
                description='You cannot mute other staff members',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        duration = datetime.timedelta(seconds=timespan)

        await member.timeout_for(duration=duration, reason=reason)
        await ctx.reply(f"{member.mention} has been muted for {duration} | Reason {reason}")

        await ctx.guild.get_channel(MOD_ACTION_LOG_CHANNEL_ID).send(
            f"Moderator: <@{ctx.message.author.id}> \n"
            f"User: <@{member.id}> \n"
            f"Action: Mute \n"
            f"Duration: {duration} \n"
            f"Reason: {reason}")

        await member.send("You have been muted in Skyblock University.\n\n"
                          "If you would like to appeal your mute, please create a ticket using <@575252669443211264>")

    @mute.error
    async def mute_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+mute <@mention | ID> <time> <reason>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_role(JR_MOD_ROLE_ID)
    async def unmute(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        await member.remove_timeout(reason=reason)
        await ctx.send(f"{member.mention} has been unmuted.")

        await ctx.guild \
            .get_channel(MOD_ACTION_LOG_CHANNEL_ID) \
            .send(f"Moderator: {ctx.message.author.mention} \n"
                  f"User: {member.mention} \n"
                  f"Action: Unmute \n"
                  f"Reason: {reason}")

    @unmute.error
    async def check_error(self, ctx, exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+unmute <@mention | ID> [reason]`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
