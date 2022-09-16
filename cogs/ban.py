import datetime

import discord
import humanfriendly
from discord.ext import commands
from discord.utils import get


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member, *, reason=None):
        member = member.replace("<", "")
        member = member.replace("@", "")
        member = member.replace(">", "")
        user = await self.bot.get_or_fetch_user(member)
        try:
            await user.send("You have been banned from SBU for " + reason)
            await user.send(r"Appeal at https://discord.gg/mn6kJrJuVB")
        except:
            await ctx.send("User cannot be dmed")
        try:
            await ctx.guild.ban(user=user, delete_message_days=0, reason=reason)
        except:
            embedVar = discord.Embed(description=":x: Bot does not have permission to ban this member.")
            await ctx.reply(embed=embedVar)
            return
        channel = self.bot.get_channel(823938991345893417)
        author = str(ctx.message.author.id)
        message = f"Moderator: <@{author}> \n User: <@{user.id}> | {user} \n Action: Ban \n Reason: {reason}"
        await channel.send(message)
        embedVar = discord.Embed(description=f"Moderator: <@{author}> \nUser: {user} "
                                             f"\nAction: Ban \nReason: {reason}")
        await ctx.send(embed=embedVar)
        channel = self.bot.get_channel(946591422616838264)
        await channel.send(f"Ban command ran by <@{author}> banning <@{user.id}>")

    @ban.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Insufficient Permissions")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member, *, reason=None):
        user = await self.bot.get_or_fetch_user(member)
        author = str(ctx.author.id)
        channel = self.bot.get_channel(823938991345893417)
        try:
            await ctx.guild.unban(user=user, reason=reason)
        except:
            embedVar = discord.Embed(description=":x: Bot does not have permission to unban this member.")
            await ctx.reply(embed=embedVar)
            return
        message = f"Moderator: <@{author}> \n User: <@{user.id}> | {user} \n Action: unban \n Reason: {reason}"
        await channel.send(message)
        embedVar = discord.Embed(description=f"Moderator: <@{author}> \nUser: {user} "
                                             f"\nAction: unban \nReason: {reason}")
        await ctx.send(embed=embedVar)
        channel = self.bot.get_channel(946591422616838264)
        await channel.send(f"Unban command ran by <@{author}> unbanning <@{user.id}>")

    @unban.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Insufficient Permissions")

    @commands.command()
    @commands.has_role("Junior Moderator")
    async def mute(self, ctx, member: discord.Member = None, time=None, *, reason: str):
        time = humanfriendly.parse_timespan(time)
        if member.id == ctx.author.id:
            await ctx.send("You can't mute yourself potato.")
            return
        if member.id in [462940637595959296, 438529479355400194, 397389995113185293, 665885831856128001]:
            await ctx.send("You can't mute bot owners.")
            return
        if reason is None:
            await ctx.send("Please specify a reason `+mute @mention Time Reason`")
            return
        if member is None:
            await ctx.send("Please specify a user to mute `+mute @mention Time Reason`")
            return
        await member.timeout(until=discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)
        conversion = datetime.timedelta(seconds=time)
        await ctx.send(f"{member.mention} has been muted for {conversion} | Reason {reason}")
        channel = self.bot.get_channel(823938991345893417)
        author = str(ctx.message.author.id)
        await channel.send(
            f"Moderator: <@{author}> \n User: <@{member.id}> \n Action: Mute \n Time: {conversion} \n Reason: {reason}")
        await ctx.send("Log created")
        channel = self.bot.get_channel(946591422616838264)
        await channel.send(f"Mute command ran by <@{author}> muting <@{member.id}>")

    @mute.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Insufficient Permissions")

    @mute.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Incorrect syntax `+mute @mention Time Reason`")

    @commands.command()
    @commands.has_role("Junior Moderator")
    async def unmute(self, ctx, member: discord.Member = None, *, reason: str = None):
        await member.timeout(until=None, reason=reason)
        await ctx.send(f"{member.mention} has been unmuted.")
        channel = self.bot.get_channel(823938991345893417)
        author = str(ctx.message.author.id)
        await channel.send(f"Moderator: <@{author}> \n User: <@{member.id}> \n Action: Unmute \n Reason: {reason}")
        await ctx.send("Log created")
        channel = self.bot.get_channel(946591422616838264)
        await channel.send(f"Unmute command ran by <@{author}> unmuting <@{member.id}>")

    @unmute.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Insufficient Permissions")

    @unmute.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Incorrect syntax `+unmute @mention Reason`")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("!warn"):
            role = get(message.guild.roles, name="Junior Moderator")
            if role in message.author.roles:
                try:
                    channel = self.bot.get_channel(823938991345893417)
                    user = str(message.mentions[0].id)
                    content = str(message.content)
                    reason = ' '.join(content.split()[2:])
                    author = str(message.author.id)
                    await channel.send(
                        f"Moderator: <@{author}> \n User: <@{user}> \n Action: Warn \n Reason: {reason}")

                    await message.channel.send("Log created")
                except:
                    await message.channel.send("Unable to create automatic log. Please create manually.")
            else:
                return


def setup(bot):
    bot.add_cog(Ban(bot))
