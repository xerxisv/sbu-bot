import os

import discord
from discord.ext import commands

from utils.config.config import ConfigHandler

config = ConfigHandler().get_config()


class Files(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @commands.group(name='files', aliases=['f', 'fl'])
    @commands.has_role(config['jr_admin_role_id'])
    async def files(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return

        await ctx.trigger_typing()

    @files.command(name='get', aliases=['g', 'fetch', 'f'])
    async def get(self, ctx: commands.Context, *, f_name: str):
        if ctx.channel.category.id != config['files']['allowed_category']:
            await ctx.reply('This can only be used in admin channels.')
            return
        try:
            file = discord.File(os.getcwd() + f'/data/{f_name}')
        except FileNotFoundError:
            await ctx.reply('File not found')
        else:
            await ctx.reply(file=file)

    @get.error
    async def get_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            await ctx.reply('No file name given.')


def setup(bot):
    bot.add_cog(Files(bot))
