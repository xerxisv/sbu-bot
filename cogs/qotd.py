import discord
from discord.ext import commands
import json
from utils.constants import SBU_LOGO_URL, JR_MOD_ROLE_ID, QOTD_PATH, SBU_GOLD


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

        embed.add_field(name="Add a QOTD", value="`qotd add <QOTD>`", inline=False)
        embed.add_field(name="List all QOTD's", value="`qotd list`", inline=False)

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

    @qotd.command(name="list", aliases=["l"])
    @commands.has_role(JR_MOD_ROLE_ID)
    async def list_(self, ctx):
        with open(QOTD_PATH) as fp:
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

    @list_.error
    async def on_qotdlist_error(self, ctx: discord.ext.commands.Context, error: discord.DiscordException):
        if isinstance(error, discord.ext.commands.MissingRole):
            await ctx.reply('')
        
    @qotd.command(name="remove", aliases=["del", "delete", "d", "r"])
    @commands.has_role(JR_MOD_ROLE_ID)
    async def remove(self, ctx, _id: int):
        with open(QOTD_PATH) as f:
            qotds = json.load(f)
        qotds.pop(_id-1)
        with open(QOTD_PATH, "w") as f:
            json.dump(qotds, f,
                      indent=4,
                      separators=(',', ': '))
        
        await ctx.reply("Successfully removed that qotd")


def setup(bot):
    bot.add_cog(QOTD(bot))
