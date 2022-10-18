from io import BytesIO

import discord
from discord.ext import commands
from petpetgif import petpet

from utils.constants import ACTIVE_ROLE_ID


class Pat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(ACTIVE_ROLE_ID)
    @commands.cooldown(1, 20, commands.BucketType.member)
    async def pat(self, ctx: commands.Context, member: discord.User = None):
        if member is None:
            member = ctx.author

        image = await member.display_avatar.read()  # retrieve the image bytes

        source = BytesIO(image)
        dest = BytesIO()
        petpet.make(source, dest)
        dest.seek(0)

        await ctx.send(file=discord.File(dest, filename=f"{image[0]}-petpet.gif"))

    @pat.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Insufficient Permissions, you need active role or higher to use this command.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)


def setup(bot):
    bot.add_cog(Pat(bot))
