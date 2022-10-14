import discord
from discord.ext import commands
import aiohttp

import requests


class Master(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='checkreq', aliases=['checkreqs'])
    async def checkreq(self, ctx, arg):
        requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{arg}")

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://sky.shiiyu.moe/api/v2/profile/{arg}') as resp:
                profiles = await resp.json()

        dungeon_lvl = 0
        slayer_xp = 0
        weight = 0
            
        for profile in profiles["profiles"]:
            if dungeon_lvl < int(profiles["profiles"][profile]["data"]["dungeons"]["catacombs"]["level"]["level"]):
                dungeon_lvl = int(profiles["profiles"][profile]["data"]["dungeons"]["catacombs"]["level"]["level"])
            if slayer_xp < int(profiles["profiles"][profile]["data"]["slayer_xp"]):
                slayer_xp = int(profiles["profiles"][profile]["data"]["slayer_xp"])
            if weight < int(profiles["profiles"][profile]["data"]["weight"]["senither"]["overall"]):
                weight = int(profiles["profiles"][profile]["data"]["weight"]["senither"]["overall"])

        passed_reqs = 3
        slayer_req = True
        dungeon_req = True
        weight_req = True

        if dungeon_lvl < 0:
            dungeon_req = False
            passed_reqs -= 1
        if slayer_xp < 400000:
            slayer_req = False
            passed_reqs -= 1
        if weight < 2750:
            weight_req = False
            passed_reqs -= 1

        if passed_reqs != 0 and passed_reqs != 3:
            embed = discord.Embed(
                title='Masters Requirements',
                description='',
                colour=discord.Colour.purple()
            )
            embed.add_field(name="Hold Up", value=f"You meet {passed_reqs}/3 of the requirements.", inline=False)
        elif passed_reqs == 0:
            embed = discord.Embed(
                title='Masters Requirements',
                description='',
                colour=discord.Colour.red()
            )
            embed.add_field(name="No requirements met", value="You dont meet any of the requirements", inline=False)
        else:
            embed = discord.Embed(
                title='Masters Requirements',
                description='',
                colour=discord.Colour.blue()
            )
            embed.add_field(name="Congratulations!", value="You meet all the requirements", inline=False)
        
        p = "**Passed**"
        np = "**Not Passed**"
        
        embed.add_field(name="Your Stats", value=f"Slayer Req: 400000 xp | "
                                                 f"Your Slayers: **{slayer_xp}** | {p if slayer_req else np} \n"
                                                 f"Cata req: level 0 | "
                                                 f"Your Cata: **{dungeon_lvl}** | {p if dungeon_req else np} \n"
                                                 f"Weight req: 2750 senither weight | "
                                                 f"Your Weight: {weight} | {p if weight_req else np}", inline=False)
        embed.set_footer(text='SB Masters')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Master(bot))
