import aiohttp
import discord
import requests
from discord.ext import commands

from utils.config.config import ConfigHandler

config = ConfigHandler().get_config()


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
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        requests.get(f"https://sky.shiiyu.moe/stats/{ign}")

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://sky.shiiyu.moe/api/v2/profile/{ign}') as resp:
                if resp.status != 200:
                    embed = discord.Embed(
                        title='Error',
                        description=f'User with IGN `{ign}` not found.\n'
                                    f'If `{ign}` is a valid IGN then it\'s an API error.\n'
                                    f'Please check manually.',
                        color=config['colors']['error']
                    )
                    await ctx.reply(embed=embed)
                    return
                profiles = await resp.json()

        dungeon_lvl = 0
        slayer_xp = 0
        weight = 0  # used to store the weight but also find the biggest weight in the profiles

        is_valid_profile = cute_name is None
        selected_profile = None

        try:
            for profile in profiles["profiles"].values():
                if cute_name is not None:
                    if profile["cute_name"].lower() != cute_name.lower():
                        continue
                    is_valid_profile = True
                    selected_profile = profile
                elif profile["data"]["weight"]["senither"]["overall"] > weight:
                    weight = profile["data"]["weight"]["senither"]["overall"]
                    selected_profile = profile

        except KeyError:
            embed = discord.Embed(
                title='Error',
                description='Something went wrong. Make sure your APIs in on.\n'
                            'If this problem continues, open a technical difficulties ticket.',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        if not is_valid_profile:
            embed = discord.Embed(
                title='Error',
                description=f'You have no {cute_name.title()} profile.',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        try:
            dungeon_lvl = int(selected_profile["data"]["dungeons"]["catacombs"]["level"]["level"])
            slayer_xp = int(selected_profile["data"]["slayer_xp"])
            weight = int(selected_profile["data"]["weight"]["senither"]["overall"])
        except KeyError:
            embed = discord.Embed(
                title='Error',
                description='Something went wrong. Make sure your APIs in on.\n'
                            'If this problem continues, open a technical difficulties ticket.',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)

        passed_reqs = 3
        slayer_req = True
        dungeon_req = True
        weight_req = True

        if dungeon_lvl < 30:
            dungeon_req = False
            passed_reqs -= 1
        if slayer_xp < 1000000:
            slayer_req = False
            passed_reqs -= 1
        if weight < 4200:
            weight_req = False
            passed_reqs -= 1

        if passed_reqs != 0 and passed_reqs != 3:
            embed = discord.Embed(
                title='Masters Requirements',
                description='',
                color=discord.Colour.purple()
            )
            embed.add_field(name="Hold Up", value=f"You meet {passed_reqs}/3 of the requirements.", inline=False)
        elif passed_reqs == 0:
            embed = discord.Embed(
                title='Masters Requirements',
                description='',
                color=discord.Colour.red()
            )
            embed.add_field(name="No requirements met", value="You dont meet any of the requirements", inline=False)
        else:
            embed = discord.Embed(
                title='Masters Requirements',
                description='',
                color=discord.Colour.blue()
            )
            embed.add_field(name="Congratulations!", value="You meet all the requirements", inline=False)

        p = "**Passed**"
        np = "**Not Passed**"

        embed.add_field(name="Your Stats", value=f"Slayer Req: 1000000 xp | "
                                                 f"Your Slayers: **{slayer_xp}** | {p if slayer_req else np} \n"
                                                 f"Cata req: level 30 | "
                                                 f"Your Cata: **{dungeon_lvl}** | {p if dungeon_req else np} \n"
                                                 f"Weight req: 4200 senither weight | "
                                                 f"Your Weight: {weight} | {p if weight_req else np}", inline=False)
        embed.set_footer(text=f'{ign} | {selected_profile["cute_name"]}')

        await ctx.send(embed=embed)

    @checkreq.error
    async def checkreq_err(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+checkreq <IGN>`.\nEx: `+checkreq RealMSpeed`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return


def setup(bot):
    bot.add_cog(Master(bot))
