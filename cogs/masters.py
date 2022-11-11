import aiohttp
import discord
import requests
from discord.ext import commands


class Master(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='checkreq', aliases=['checkreqs'])
    @commands.cooldown(1, 0)
    async def checkreq(self, ctx: commands.Context, ign: str, cute_name: str = None):
        await ctx.trigger_typing()

        if cute_name and cute_name.lower() not in ['apple', 'banana', 'blueberry', 'coconut', 'cucumber', 'grapes',
                                                   'kiwi', 'lemon', 'lime', 'mango', 'orange', 'papaya', 'pear',
                                                   'peach', 'pineapple', 'pomegranate', 'raspberry', 'strawberry',
                                                   'tomato', 'watermelon', 'zucchini']:
            embed = discord.Embed(
                title='Error',
                description='Invalid profile.',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        requests.get(f"https://sky.shiiyu.moe/stats/{ign}")

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://sky.shiiyu.moe/api/v2/profile/{ign}') as resp:
                profiles = await resp.json()

        dungeon_lvl = 0
        slayer_xp = 0
        weight = 0

        is_valid_profile = cute_name is None

        for profile in profiles["profiles"].values():
            if cute_name is not None:
                if profile["cute_name"].lower() != cute_name.lower():
                    continue
                is_valid_profile = True
            elif not profile["current"]:
                continue

            try:
                dungeon_lvl = int(profile["data"]["dungeons"]["catacombs"]["level"]["level"])
                slayer_xp = int(profile["data"]["slayer_xp"])
                weight = int(profile["data"]["weight"]["senither"]["overall"])
            except KeyError:
                embed = discord.Embed(
                    title='Error',
                    description='Something went wrong. Make sure your APIs in on.\nRun `!enableapi` for the tutorial',
                    colour=0xFF0000
                )
                await ctx.reply(embed=embed)

        if not is_valid_profile:
            embed = discord.Embed(
                title='Error',
                description=f'You have no {cute_name.title()} profile.',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        passed_reqs = 3
        slayer_req = True
        dungeon_req = True
        weight_req = True

        if dungeon_lvl < 0:
            dungeon_req = False
            passed_reqs -= 1
        if slayer_xp < 4000000:
            slayer_req = False
            passed_reqs -= 1
        if weight < 2750 :
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

    @checkreq.error
    async def checkreq_err(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+checkreq <IGN>`.\nEx: `+checkreq RealMSpeed`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return


def setup(bot):
    bot.add_cog(Master(bot))
