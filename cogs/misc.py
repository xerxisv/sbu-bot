from io import BytesIO

import discord
from discord.ext import commands
from petpetgif import petpet

from utils.config.config import ConfigHandler

config = ConfigHandler().get_config()


class Misc(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(config['misc']['allowed_role_id'])
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
    async def check_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.BadArgument):
            await self.bot.get_command("pat").invoke(ctx)


def setup(bot):
    bot.add_cog(Misc(bot))
