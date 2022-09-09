import discord
from discord.ext import commands
from discord.utils import get
import requests
import os
import datetime
import json

class GEXP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_any_role("Council","Bot")
    async def fetchgexpleaderboard(self, ctx):
        key = os.getenv("apikey")
        guilds = ["6111fcb48ea8c95240436c57", "604a765e8ea8c962f2bb3b7a",
                "607a0d7c8ea8c9c0ff983976", "608d91e98ea8c9925cdb91b7",
                "60a16b088ea8c9bb7f6d9052", "60b923478ea8c9a3aefbf3dd", "6125800e8ea8c92e1833e851",
                "570940fb0cf2d37483e106b3"]
        embedVar = discord.Embed(description="<a:loading:973262460876374016> This message will be updated with the leaderboard once processing is complete.")
        message = await ctx.send(embed=embedVar)
        key = os.getenv("apikey")
        topearnersgexp = []
        topearnersuuid = []
        for guild in guilds:
            data = requests.get(f'https://api.hypixel.net/guild?key={key}&id={guild}').json()
            for i in data["guild"]["members"]:
                total = 0
                for i2 in i["expHistory"]:
                    total += i["expHistory"][i2]
                uuid = i["uuid"]
                topearnersgexp.append(total)
                topearnersuuid.append(uuid)

        topearnersgexp, topearnersuuid = (list(t) for t in zip(*sorted(zip(topearnersgexp, topearnersuuid))))    
        temp = []
        for x in topearnersgexp:
            if x not in temp:
                temp.append(x)
        topearnersgexp = temp
        temp = []
        for x in topearnersuuid:
            if x not in temp:
                temp.append(x)
        topearnersuuid = temp
        topearnersgexp = topearnersgexp[-10:]
        topearnersuuid = topearnersuuid[-10:]
        convertedign = []
        for uuid in topearnersuuid:
            data = requests.get(f'https://api.mojang.com/user/profile/{uuid}').json()
            convertedign.append(data['name'])
        convertedign.reverse()
        topearnersgexp.reverse()
        embedVar = discord.Embed(title="SBU's GEXP Leaderboard")
        for i in range(10):
            embedVar.add_field(name=f'{convertedign[i]}', value=f'GEXP Earned: {topearnersgexp[i]}')
        await message.edit(embed=embedVar)

def setup(bot):
    bot.add_cog(GEXP(bot))
