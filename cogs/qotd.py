import json
from math import ceil

import discord
from discord.ext import commands

from utils.config.config import ConfigHandler

config = ConfigHandler().get_config()


class QOTD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='qotd', aliases=["q"])
    @commands.has_role(config['jr_mod_role_id'])
    async def qotd(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('qotd help').invoke(ctx)
            return
        await ctx.trigger_typing()

    @qotd.command(name="help", aliases=["commands"])
    @commands.has_role(config['jr_mod_role_id'])
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title='Command help',
            color=config['colors']['primary']
        )

        embed.add_field(name="Add a QOTD", value="`+qotd add <QOTD>`", inline=False)
        embed.add_field(name="List all QOTD's", value="`+qotd list`", inline=False)
        embed.add_field(name="Remove a QOTD", value="`+qotd remove <num>`", inline=False)

        await ctx.reply(embed=embed)

    @qotd.command(name="add", aliases=["a"])
    @commands.has_role(config['jr_mod_role_id'])
    async def add(self, ctx: commands.Context, *, qotd):
        with open('./data/qotd.json') as fp:
            list_obj = json.load(fp)

        data = {
            "qotd": qotd
        }
        list_var = list(list_obj)
        list_var.append(data)

        with open('./data/qotd.json', 'w') as json_file:
            json.dump(list_var, json_file,
                      indent=4,
                      separators=(',', ': '))

        qotd_embed = discord.Embed(
            title='Qotd Added',
            description=f'{qotd}',
            color=config['colors']['primary']
        )

        qotd_embed.set_thumbnail(url=config['logo_url'])
        await ctx.send(embed=qotd_embed)

    @add.error
    async def add_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+qotd add <question>`',
                color=config['colors']['error']
            )

            await ctx.reply(embed=embed)

    @qotd.command(name='list', aliases=['show', 'print'])
    @commands.has_role(config['jr_mod_role_id'])
    async def list_(self, ctx: commands.Context, page: int = 1):
        with open('./data/qotd.json') as fp:
            questions = json.load(fp)

        q_len = len(questions)  # The length of the questions array
        questions_max = 24  # Maximum number of questions that can be displayed at a time
        max_page = ceil(q_len / questions_max)  # The maximum page number

        # Ensure that page is within the limits
        if page > max_page:
            embed = discord.Embed(
                title='Error',
                description=f'There is no page {page}. Valid pages are between 1 and {max_page}',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        # Set the questions' start and end index
        start = questions_max * (page - 1)  # Skips the first `questions_max * page` objects
        # Keeps 24 objects skipping the rest and ensuring that we are within index bounds
        end = (questions_max * (page - 1)) + min(questions_max, q_len - (max_page * (page - 1)))

        questions = questions[start:end]

        qotd_embed = discord.Embed(
            title=f'QOTD List',
            color=config['colors']['primary']
        )

        for index, qotd in enumerate(questions):
            qotd_embed.add_field(name=f'QOTD: {index + 1}', value=qotd['qotd'], inline=False)

        qotd_embed.set_thumbnail(url=config['logo_url'])
        qotd_embed.set_footer(text=f'Page: {page}/{max_page}')

        await ctx.reply(embed=qotd_embed)

    @list_.error
    async def list_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.BadArgument):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+qotd list [page]`',
                color=config['colors']['error']
            )

            await ctx.reply(embed=embed)

    @qotd.command(name="remove", aliases=["del", "delete", "rm"])
    @commands.has_role(config['jr_mod_role_id'])
    async def remove(self, ctx: commands.Context, i: int):
        # Read all the questions
        with open('./data/qotd.json') as f:
            qotds = json.load(f)

        # Remove the question at index i-1
        qotds.pop(i - 1)

        # Write questions
        with open('./data/qotd.json', "w") as f:
            json.dump(qotds, f,
                      indent=4,
                      separators=(',', ': '))

        embed = discord.Embed(
            title='Success',
            description='Question successfully removed.',
            color=config['colors']['success']
        )
        await ctx.reply(embed=embed)

    @remove.error
    async def remove_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.MissingRequiredArgument, commands.BadArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+qotd remove <question_id>`',
                color=config['colors']['error']
            )

            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(QOTD(bot))
