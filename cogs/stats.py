import discord
import discord.utils
from discord.ext import commands
import requests

from utils.constants import SBU_GOLD


class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(20, 60, commands.BucketType.guild)
    async def hypixel(self, ctx: commands.Context, ign: str):
        # Fetch player info
        res = requests.get(f'https://api.slothpixel.me/api/players/{ign}')

        if res.status_code != 200:
            embed = discord.Embed(title=f'Error',
                                  description='Error fetching information from the API. Try again later',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        player = res.json()

        # Fetch player's guild info
        res = requests.get(f'https://api.slothpixel.me/api/guilds/{ign}')

        if res.status_code == 404:
            guild = None
        elif res.status_code != 200:
            embed = discord.Embed(title=f'Error',
                                  description='Error fetching information from the API. Try again later',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        else:
            guild = res.json()

        embed = discord.Embed(title=f'{ign} Hypixel stats', colour=SBU_GOLD)

        embed.add_field(name='Rank', value=f'{player["rank"].replace("PLUS", "+").replace("_", "")}', inline=False)
        embed.add_field(name='Level:', value=f'{player["level"]}', inline=False)
        embed.add_field(name='Discord:', value=f'{player["links"]["DISCORD"]}', inline=False)
        embed.add_field(name='Online:', value=f'{player["online"]}', inline=False)

        if guild is None:
            embed.add_field(name='Guild:', value=f'{ign} isn\'t in a guild')
        else:
            embed.add_field(name='Guild:', value=guild["name"])
        await ctx.reply(embed=embed)

    @hypixel.error
    async def check_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=f'Error', description='Please enter an IGN\n Ex: `+hypixel RealMSpeed`',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return

    @commands.command(aliases=['s'])
    async def skycrypt(self, ctx: commands.Context, ign: str):
        await ctx.reply(f'https://sky.shiiyu.moe/stats/{ign}')
    
    @skycrypt.error
    async def check_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Please enter an IGN\n Ex: `+skycrypt RealMSpeed`')


def setup(bot):
    bot.add_cog(Stats(bot))
