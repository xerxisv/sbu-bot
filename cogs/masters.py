import discord
from discord.ext import commands
import aiohttp

import requests


class Master(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['checkreqs'])
    async def checkreq(self, ctx, arg):
        response = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{arg}")

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://sky.shiiyu.moe/api/v2/profile/{arg}') as resp:
                profiles = await resp.json()

        dungeonlvl = 0
        slayerxp = 0
        weight = 0
            
        for profile in profiles["profiles"]:
            if dungeonlvl < int(profiles["profiles"][profile]["data"]["dungeons"]["catacombs"]["level"]["level"]):
                dungeonlvl = int(profiles["profiles"][profile]["data"]["dungeons"]["catacombs"]["level"]["level"])
            if slayerxp < int(profiles["profiles"][profile]["data"]["slayer_xp"]):
                slayerxp = int(profiles["profiles"][profile]["data"]["slayer_xp"])
            if weight < int(profiles["profiles"][profile]["data"]["weight"]["senither"]["overall"]):
                weight = int(profiles["profiles"][profile]["data"]["weight"]["senither"]["overall"])
            
        embed = discord.Embed(
            title='Masters Requirements',
            description='',
            colour=discord.Colour.red()
        )
        embed.set_footer(text='SB Masters')

        passedreqs = 3
        slayerreq = True
        dungeonreq = True
        weightreq = True

        if dungeonlvl < 0:
            dungeonreq = False
            passedreqs -= 1
        if slayerxp < 400000:
            slayerreq = False
            passedreqs -= 1
        if weight < 2750:
            weightreq = False
            passedreqs -= 1
        
        
        if passedreqs != 0 and passedreqs != 3:
            embed.add_field(name="Hold Up", value=f"You meet {passedreqs}/3 of the requirements.", inline=False)
            embed.color = discord.Colour.purple()
        elif passedreqs == 0:
            embed.add_field(name="No requirements met", value="You dont meet any of the requirements", inline=False)
        else:
            embed.add_field(name="Congratulations!", value="You meet all the requirements", inline=False)
            embed.color = discord.Colour.blue()
        
        p = "**Passed**"
        np = "**Not Passed**"
        
        embed.add_field(name="Your Stats", value=f"Slayer Req: 400000 xp | Your Slayers: **{slayerxp}** | {p if slayerreq else np} \n Cata req: level 0 | Your Cata: **{dungeonlvl}** | {p if dungeonreq else np} \nWeight req: 2750 senither weight | Your Weight: {weight} | {p if weightreq else np}", inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Master(bot))

