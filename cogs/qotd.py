import discord
from discord.ext import commands
import json
from utils.constants import SBU_LOGO_URL, JR_MOD_ROLE_ID, QOTD_PATH, SBU_GOLD
from math import ceil


class QOTD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='qotd', aliases=["q"])
    @commands.has_role(JR_MOD_ROLE_ID)
    async def qotd(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('qotd help').invoke(ctx)
            return
        await ctx.trigger_typing()
    
    @qotd.command(name="help", aliases=["commands"])
    @commands.has_role(JR_MOD_ROLE_ID)
    async def help(self, ctx):
        embed = discord.Embed(
            title='Command help',
            colour=SBU_GOLD
        )

        embed.add_field(name="Add a QOTD", value="`+qotd add <QOTD>`", inline=False)
        embed.add_field(name="List all QOTD's", value="`+qotd list`", inline=False)
        embed.add_field(name="Remove a QOTD", value="`+qotd remove <num>`", inline=False)

        await ctx.reply(embed=embed)

    @qotd.command(name="add", aliases=["a"])
    @commands.has_role(JR_MOD_ROLE_ID)
    async def add(self, ctx, *, qotd):
        if ctx.author.id == 0:
            await ctx.send("Banned from qotd")
            return
        with open(QOTD_PATH) as fp:
            list_obj = json.load(fp)

        data = {
            "qotd": qotd
        }
        list_var = list(list_obj)
        list_var.append(data)

        with open(QOTD_PATH, 'w') as json_file:
            json.dump(list_var, json_file,
                      indent=4,
                      separators=(',', ': '))
        qotd_embed = discord.Embed(
            title=f'Qotd Added',
            description=f'{qotd}',
            colour=0x8F49EA
        )
        qotd_embed.set_thumbnail(
            url=SBU_LOGO_URL)
        await ctx.send(embed=qotd_embed)

    @qotd.command(name='list', aliases=['show', 'print'])
    @commands.has_role(JR_MOD_ROLE_ID)
    async def list_(self, ctx: commands.Context, page: int = 0):
        with open(QOTD_PATH) as fp:
            questions = json.load(fp)

        q_len = len(questions)  # The length of the questions array
        questions_max = 24  # Maximum number of questions that can be displayed at a time
        max_page = ceil(q_len / questions_max)  # The maximum page number

        # Ensure that page is within the limits
        if page > max_page:
            embed = discord.Embed(
                title='Error',
                description=f'There is no page {page}. Valid pages are between 1 and {max_page}',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        # Set the questions' start and end index
        start = questions_max * page  # Skips the first `questions_max * page` objects
        # Keeps 24 objects skipping the rest and ensuring that we are within index bounds
        end = (max_page * page) + min(max_page, q_len - (max_page * page))

        questions = questions[start:end]

        qotd_embed = discord.Embed(
            title=f'QOTD List',
            colour=SBU_GOLD
        )

        for index, qotd in enumerate(questions):
            qotd_embed.add_field(name=f'QOTD: {index + 1}', value=qotd['qotd'], inline=False)

        qotd_embed.set_thumbnail(url=SBU_LOGO_URL)
        qotd_embed.set_footer(text=f'Page: {page+1}/{max_page}')

        await ctx.reply(embed=qotd_embed)

    @list_.error
    async def list_error(self, ctx: discord.ext.commands.Context, error: discord.DiscordException):
        if isinstance(error, discord.ext.commands.MissingRole):
            await ctx.reply('')
        
    @qotd.command(name="remove", aliases=["del", "delete", "rm"])
    @commands.has_role(JR_MOD_ROLE_ID)
    async def remove(self, ctx: commands.Context, i: int):
        # Read all the questions
        with open(QOTD_PATH) as f:
            qotds = json.load(f)

        # Remove the question at index i-1
        qotds.pop(i - 1)

        # Write questions
        with open(QOTD_PATH, "w") as f:
            json.dump(qotds, f,
                      indent=4,
                      separators=(',', ': '))
        
        await ctx.reply("Successfully removed that qotd")


def setup(bot):
    bot.add_cog(QOTD(bot))
