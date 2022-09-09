from discord.ext import tasks, commands
import discord
import discord.utils
import os
import random
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
import aiohttp
import asyncio
import json
import time
import datetime

class TasksCog(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot

    def cog_unload(self):
        self.updatemember.cancel()
        self.autoqotd.cancel()
    @commands.Cog.listener()
    async def on_ready(self):
        self.updatemember.start()
        self.autoqotd.start()
        
    @tasks.loop(hours=1)
    async def updatemember(self):
        vc = [945493379599446056,945493468539654205,945493492434604072,945493508398153808
                ,945493526047776889,945493540748791899,945493556909473812,945493573263040522]
        guilds = ["6111fcb48ea8c95240436c57", "604a765e8ea8c962f2bb3b7a",
                "607a0d7c8ea8c9c0ff983976", "608d91e98ea8c9925cdb91b7",
                "60a16b088ea8c9bb7f6d9052", "60b923478ea8c9a3aefbf3dd", "6125800e8ea8c92e1833e851",
                "570940fb0cf2d37483e106b3"]
        total_members = 0
        for i in range(len(guilds)):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.slothpixel.me/api/guilds/id/{guilds[i]}') as resp:
                        guildrename = await resp.json()
                rename = guildrename["name"] + ": " + str(len(guildrename["members"]))
                total_members = total_members + int(len(guildrename["members"]))
                vc1 = self.bot.get_channel(vc[i])
                await vc1.edit(name=rename)
            except:
                channel = self.bot.get_channel(946591422616838264)
                await channel.send(f"<@462940637595959296> Obby fix the vcs nerd: {guilds[i]}")
        vc2 = self.bot.get_channel(890288776302190602)
        rename1 = "Guild members: " + str(total_members)
        await vc2.edit(name=rename1)
        channel = self.bot.get_channel(946591422616838264)
        await channel.send(f"Guild Stats VC Updated")
        print("Updated")
        
    @tasks.loop(hours=24)
    async def autoqotd(self):
        channel = self.bot.get_channel(868630191080083476)
        with open('qotd.json') as fp:
            listObj = json.load(fp)
        listvar = list(listObj)
        try:
            name1 = listvar[0]["qotd"]
        except:
            channel = self.bot.get_channel(802982854291488808)
            await channel.send(f"<@&924332988743966751> no QOTD's left in the archive. Automatic qotd canceled. \n "
                            f"Please add more using `+qotdadd`")
            return
        message = await channel.send(listvar[0]["qotd"] + "<@&868630686712614922>")
        await message.create_thread(name="QOTD")
        listvar.pop(0)
        with open('qotd.json', 'w') as json_file:
            json.dump(listvar, json_file,
                    indent=4,
                    separators=(',', ': '))
        num1 = len(listvar)
        if num1 < 3:
            channel = self.bot.get_channel(802982854291488808)
            await channel.send(f"<@&924332988743966751> QOTD's Running Low. Only {num1} remain. \n Please add more "
                            f"using `+qotdadd`")
            
def setup(bot):
    bot.add_cog(TasksCog(bot))
