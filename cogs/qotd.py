import discord
from discord.ext import commands
from discord.ext import tasks
import datetime
import json


class QOTD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Junior Moderator")
    async def qotdadd(self, ctx, *, qotd):
        if ctx.author.id == 0:
            await ctx.send("Banned from qotd")
            return
        with open('qotd.json') as fp:
            listObj = json.load(fp)

        data = {
            "qotd": qotd
        }
        listvar = list(listObj)
        listvar.append(data)

        with open('qotd.json', 'w') as json_file:
            json.dump(listvar, json_file,
                      indent=4,
                      separators=(',', ': '))
        qotdembed = discord.Embed(
            title=f'Qotd Added',
            description=f'{qotd}',
            colour=0x8F49EA
        )
        qotdembed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/937099605265485936/8a5d786e369fdda9f355f12eaf0487fb.png?size=4096")
        await ctx.send(embed=qotdembed)

    @commands.command()
    @commands.has_role("Junior Moderator")
    async def qotdlist(self, ctx):
        with open('qotd.json') as fp:
            listObj = json.load(fp)
        if len(listObj) >= 24:
            qotdembed = discord.Embed(
                title=f'QOTD List',
                description=f'Too many QOTD to display. \nTotal Number: {len(listObj)}',
                colour=0x8F49EA
            )
            await ctx.send(embed=qotdembed)
            return
        qotdembed = discord.Embed(
            title=f'QOTD List',
            colour=0x8F49EA
        )
        count=1
        for qotd in listObj:
            qotdembed.add_field(name=f'QOTD: {count}', value=qotd['qotd'], inline=False)
            count = count+1
        qotdembed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/937099605265485936/8a5d786e369fdda9f355f12eaf0487fb.png?size=4096")
        await ctx.send(embed=qotdembed)


def setup(bot):
    bot.add_cog(QOTD(bot))
