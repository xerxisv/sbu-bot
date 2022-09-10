import re
import discord
from discord.ext import commands
from discord.utils import get
import requests
import time
import dotenv
import os
import sqlite3
import humanfriendly
import datetime
from discord.ext import tasks, commands


class InactiveList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.checkinactives.start()

    def cog_unload(self):
        self.checkinactives.cancel()

    @tasks.loop(hours=12)
    async def checkinactives(self):
        conn = sqlite3.connect('inactive.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM inactives''')
        values = c.fetchall()
        for value in values:
            t = time.time()
            if t > value[2]:
                c.execute(f'''SELECT * FROM inactives WHERE time = {value[2]}''')
                conn.commit()
        conn.close()
        print('Inactives Cleared')

    @commands.Cog.listener()
    async def on_ready(self):
        conn = sqlite3.connect('inactive.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS inactives (
            discordid integer,
            uuid text,
            time integer
        )""")
        conn.commit()
        conn.close()
        print('Inactive List Initialized')

    @commands.command()
    async def inactiveadd(self, ctx, ign: str, afktime=None):
        if afktime == None:
            embed = discord.Embed(title=f'Error',
                                  description='No time inputted \nEnter time in days Ex: 10d for 10 days',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        conn = sqlite3.connect('inactive.db')
        c = conn.cursor()
        request = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}')
        if request.status_code == 204:
            embed = discord.Embed(title=f'Error', description='Invalid IGN',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        request = request.json()
        uuid = request['id']
        c.execute(f'''SELECT * FROM inactives WHERE uuid = "{uuid}"''')
        value = c.fetchone()
        try:
            afktime = humanfriendly.parse_timespan(afktime)
            if afktime > 8640000:
                embed = discord.Embed(title=f'Error',
                                      description='Invalid Time \nEnter time in days max of 100 Ex: 10d for 10 days',
                                      colour=0xFF0000)
                await ctx.reply(embed=embed)
                return
        except:
            embed = discord.Embed(title=f'Error', description='Invalid Time \nEnter time in days Ex: 10d for 10 days',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        t = time.time()
        afktime = t + afktime
        if value == None:
            pass
        else:
            c.execute(f'''DELETE FROM inactives WHERE uuid = "{uuid}"''')
        c.execute(f"""INSERT INTO inactives VALUES (
            {ctx.author.id},
            "{uuid}",
            {afktime}
        )""")
        conn.commit()
        conn.close()
        embed = discord.Embed(title=f'Success',
                              description=f'{request["name"]} has been added to Inactive list until {datetime.datetime.fromtimestamp(afktime).strftime("%A, %B %d, %Y %I:%M:%S")}',
                              colour=ctx.author.color)
        await ctx.reply(embed=embed)
        channel = self.bot.get_channel(822813537704738856)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(InactiveList(bot))
