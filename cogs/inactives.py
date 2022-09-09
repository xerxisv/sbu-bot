import discord
from discord.ext import commands
from discord.utils import get
import requests
import time
import dotenv
import os
import sqlite3


class GuildInactiveCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(1, 60)
    async def inactive(self, ctx, *,guild = None):
        conn = sqlite3.connect('inactive.db')
        c = conn.cursor()   
        c.execute('''SELECT * FROM inactives''')
        values = c.fetchall()
        valuecheck = []
        for value in values:
            valuecheck.append(value[1])
        if guild == None:
            embedVar = discord.Embed(color=ctx.author.color,
                        description=f"No guild inputted, `+inactive GUILD`")
            await ctx.send(embed=embedVar)
            return
        if guild.lower() in ["sb lambda pi", "sb theta tau", "sb delta omega", "sb iota theta",
                                        "sb uni", "sb rho xi", "sb kappa eta", "sb alpha psi", "sb masters"]:
            pass
        else:
            embedVar = discord.Embed(color=ctx.author.color,
                    description=f"Inputted guild is not an SBU guild")
            await ctx.send(embed=embedVar)
            return
        key = os.getenv("apikey")
        amount = 1
        data = requests.get(
            url="https://api.hypixel.net/guild",
            params={
                "key": key,
                "name": guild
            }).json()
        embedVar = discord.Embed(color=ctx.author.color, title=f"Inactive List for {data['guild']['name']}",
                        description=f"<a:loading:978732444998070304> Skyblock University is thinking")
        message=await ctx.send(embed=embedVar)
        if data["guild"] is not None:
            embedmsg = ""
            totalmembers = 0
            ManualCheck = []
            for i in data["guild"]["members"]:
                total = 0
                try:
                    for i2 in i["expHistory"]:
                        total += i["expHistory"][i2]
                    uuid = i["uuid"]
                    if total <= int(amount):
                        data3 = requests.get(url=f"https://api.mojang.com/user/profile/{uuid}").json()
                        if uuid in valuecheck:
                            pass
                        else:
                            username = data3["name"]
                            if username in ['MastersBridge','RhoXiBridge','ThetaTauBridge','LambdaPiBridg',
                                            'DeltaOmegaBridge','KappaEtasBridge','AlphaPsisBridge','UniversityBot']:
                                pass
                            else:
                                ManualCheck.append(username)
                                embedmsg += f"`{username}`\n"
                                totalmembers += 1
                except:
                    print("error")
            embedVar = discord.Embed(color=ctx.author.color, title=f"Inactive List for {data['guild']['name']}",
                                        description=f"{totalmembers} members were found to be under {amount} GEXP." + f"\n\n{embedmsg}")
            await message.edit(embed=embedVar)
        conn.close()
    @inactive.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)


def setup(bot):
    bot.add_cog(GuildInactiveCheck(bot))
