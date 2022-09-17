import discord
from discord.ext import commands
import json
from utils.constants import SBU_LOGO_URL, JR_MOD_ROLE_ID


class QOTD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(JR_MOD_ROLE_ID)
    async def qotdadd(self, ctx, *, qotd):
        if ctx.author.id == 0:
            await ctx.send("Banned from qotd")
            return
        with open('qotd.json') as fp:
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
            title=f'Qotd Added',
            description=f'{qotd}',
            colour=0x8F49EA
        )
        qotd_embed.set_thumbnail(
            url=SBU_LOGO_URL)
        await ctx.send(embed=qotd_embed)

    @commands.command()
    @commands.has_role(JR_MOD_ROLE_ID)
    async def qotdlist(self, ctx):
        with open('./data/qotd.json') as fp:
            list_obj = json.load(fp)
        if len(list_obj) >= 24:
            qotd_embed = discord.Embed(
                title=f'QOTD List',
                description=f'Too many QOTD to display. \nTotal Number: {len(list_obj)}',
                colour=0x8F49EA
            )
            await ctx.send(embed=qotd_embed)
            return
        qotd_embed = discord.Embed(
            title=f'QOTD List',
            colour=0x8F49EA
        )
        count = 1
        for qotd in list_obj:
            qotd_embed.add_field(name=f'QOTD: {count}', value=qotd['qotd'], inline=False)
            count = count + 1
        qotd_embed.set_thumbnail(
            url=SBU_LOGO_URL)
        await ctx.send(embed=qotd_embed)

    @qotdlist.error
    async def on_qotdlist_error(self, ctx: discord.ext.commands.Context, error: discord.DiscordException):
        if isinstance(error, discord.ext.commands.MissingRole):
            await ctx.reply('')


def setup(bot):
    bot.add_cog(QOTD(bot))
