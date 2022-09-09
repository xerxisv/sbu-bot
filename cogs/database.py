import discord
import psycopg2
from discord.ext import commands

hostname = 'localhost'
database = 'SBU'
username = 'postgres'
pwd = 'obbytrusty'
port_id = 5432

create_script = '''CREATE TABLE IF NOT EXISTS verified (id varchar(40) PRIMARY KEY,
                    uuid varchar(40) NOT NULL,
                    guild varchar(40))'''

create_script1 = '''CREATE TABLE IF NOT EXISTS reputation (num varchar(40) PRIMARY KEY, 
                id varchar(40) NOT NULL, rep varchar(40) NOT NULL, value varchar(200), reason varchar(200))
                '''


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def databasecreate(self, ctx):
        if ctx.message.author.id == 462940637595959296:
            conn = psycopg2.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id)
            cur = conn.cursor()
            cur.execute(create_script)
            conn.commit()
            cur.execute(create_script1)
            conn.commit()
            cur.close()
            conn.close()
            await ctx.send("Database created")
        elif ctx.message.author.id == 438529479355400194:
            await ctx.send("No ashlie bad")
            await ctx.send(":ashliebonk:")
        elif ctx.message.author.id == 397389995113185293:
            await ctx.send("<:adubonk:938997760181563442>")
        elif ctx.message.author.id == 565799167952289792:
            await ctx.send("NO bad")
            await ctx.send("I will eat all the dino nuggets")
        else:
            await ctx.send("smh you are not obby")


def setup(bot):
    bot.add_cog(Database(bot))
