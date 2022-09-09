import discord
from discord.ext import commands
import aiohttp


class Master(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['checkreqs'])
    async def checkreq(self, ctx, arg):
        await ctx.send("Checking Reqs now...")
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://sky.shiiyu.moe/api/v2/profile/{arg}') as resp:
                skill = await resp.json()
            async with session.get(f'https://sky.shiiyu.moe/api/v2/slayers/{arg}') as resp:
                slayer = await resp.json()
            async with session.get(f'https://sky.shiiyu.moe/api/v2/dungeons/{arg}') as resp:
                dungeon = await resp.json()
        temp = 0
        temp1 = 0
        temp2 = 0
        for profile in slayer["profiles"]:
            if temp <= int(slayer["profiles"][profile]["slayer_xp"]):
                temp = int(slayer["profiles"][profile]["slayer_xp"])
            if dungeon["profiles"][profile]["dungeons"]["catacombs"]["visited"]:
                if temp1 <= int(dungeon["profiles"][profile]["dungeons"]["catacombs"]["level"]["level"]):
                    temp1 = int(dungeon["profiles"][profile]["dungeons"]["catacombs"]["level"]["level"])
            if temp2 <= int(skill["profiles"][profile]["data"]["average_level"]):
                temp2 = int(skill["profiles"][profile]["data"]["average_level"])
        slayerreq = f"""You do not meet the slayer reqirement.
        Current req is **500k total slayer xp**. 
        Your XP is {temp}"""
        dungeonreq = f"""You do not meet the cata lvl reqirement.
                Current req is **cata 25**. 
                Your cata lvl is {temp1}"""
        skillreq = f"""You do not meet the skill avg reqirement.
                        Current req is **SA 30**. 
                        Your SA is {temp2}"""
        mastersreq = discord.Embed(
            title='Masters Requirements',
            description='',
            colour=discord.Colour.red()
        )
        mastersreq.set_footer(text='SB Masters')
        check = True
        sacheck = True
        slayercheck = True
        catacheck = True
        if temp < 500000:
            mastersreq.add_field(name="Slayer", value=slayerreq, inline=False)
            check = False
            slayercheck = False
        if temp1 < 25:
            mastersreq.add_field(name="Dungeons", value=dungeonreq, inline=False)
            check = False
            catacheck = False
        if temp2 < 30:
            mastersreq.add_field(name="Skill Avg", value=skillreq, inline=False)
            check = False
            sacheck = False
        check1 = 0
        for a in [slayercheck, catacheck, sacheck]:
            if not a:
                check1 = check1 + 1
        if check == True and slayercheck == True and catacheck == True and sacheck == True:
            mastersreq1 = discord.Embed(
                title='Masters Requirements',
                description='',
                colour=discord.Colour.blue()
            )
            mastersreq1.add_field(name="Congratulations!", value="You meet all the requirements.", inline=False)
            await ctx.send(embed=mastersreq1)
        elif check == False and check1==1:
            mastersreq2 = discord.Embed(
                title='Masters Requirements',
                description='',
                colour=discord.Colour.purple()
            )
            mastersreq2.add_field(name="Hold Up", value="You meet 2/3 of the requirements.", inline=False)
            reqsmhm = f"""Slayer Req = 500k | Your Slayers **{temp}**
            Cata Req = Cata 25 | Your Cata **{temp1}**
            Skills Req = SA 30 | Your SA **{temp2}**"""
            mastersreq2.add_field(name="Your Stats", value=reqsmhm, inline=False)
            await ctx.send(embed=mastersreq2)
        else:
            await ctx.send(embed=mastersreq)


def setup(bot):
    bot.add_cog(Master(bot))

