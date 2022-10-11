import discord
import discord.utils
from discord.ext import commands
import requests


class HypixelStats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(20, 60, commands.BucketType.guild)
    async def hypixel(self, ctx, arg1: str = None):
        color = ctx.author.color
        if arg1 is None:
            embed = discord.Embed(title=f'Error', description='Please enter a user \n `+hypixel ObbyTrusty`',
                                  colour=color)
            await ctx.reply(embed=embed)
            return

        response = requests.get(f'https://api.slothpixel.me/api/players/{arg1}')
        if response.status_code != 200:
            embed = discord.Embed(title=f'Error',
                                  description='Error fetching information from the API. Try again later',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        player = response.json()
        response = requests.get(f'https://api.slothpixel.me/api/guilds/{arg1}')
        guild = response.json()
        if response.status_code != 200 and guild["guild"] is not None:
            embed = discord.Embed(title=f'Error',
                                  description='Error fetching information from the API. Try again later',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        embed = discord.Embed(title=f'{arg1} Hypixel stats', colour=color)
        if player['rank'] == "MVP_PLUS_PLUS":
            embed.add_field(name="PlayerRank", value="MVP++", inline=False)
        elif player['rank'] == "MVP_PLUS":
            embed.add_field(name="PlayerRank", value="MVP+", inline=False)
        elif player['rank'] == "VIP_PLUS":
            embed.add_field(name="PlayerRank", value="VIP+", inline=False)
        else:
            embed.add_field(name="PlayerRank", value=player['rank'], inline=False)
            embed.add_field(name="Level:", value=player["level"], inline=False)
        embed.add_field(name="Discord:", value=player["links"]["DISCORD"], inline=False)
        embed.add_field(name="Online:", value=player['online'], inline=False)
        if "error" in guild or guild["guild"] is None:
            embed.add_field(name="Guild:", value=f"{arg1} isn't in a guild")
        else:
            embed.add_field(name="Guild:", value=guild["name"])
        await ctx.reply(embed=embed)

    @hypixel.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    @commands.command()
    async def skycrypt(self, ctx, ign):
        await ctx.reply(f"https://sky.shiiyu.moe/stats/{ign})
    
    @skycrypt.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("IGN not provided, please try again")

def setup(bot):
    bot.add_cog(HypixelStats(bot))

