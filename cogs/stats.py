import discord
import discord.utils
import requests
import aiosqlite
from discord.ext import commands
from discord.ui import Button, View

from utils.constants import SBU_GOLD, SBU_PURPLE, WEIGHT_ROLES_INFO, GUILD_ID
from utils.database.schemas import User
from utils.database import DBConnection




class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db: aiosqlite.Connection = DBConnection().get_db()

    @commands.command()
    @commands.cooldown(20, 60, commands.BucketType.guild)
    async def hypixel(self, ctx: commands.Context, ign: str):
        # Fetch player info
        res = requests.get(f'https://api.slothpixel.me/api/players/{ign}')

        if res.status_code != 200:
            embed = discord.Embed(title=f'Error',
                                  description='Error fetching information from the API. Try again later',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        player = res.json()

        # Fetch player's guild info
        res = requests.get(f'https://api.slothpixel.me/api/guilds/{ign}')

        if res.status_code == 404:
            guild = None
        elif res.status_code != 200:
            embed = discord.Embed(title=f'Error',
                                  description='Error fetching information from the API. Try again later',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        else:
            guild = res.json()

        embed = discord.Embed(title=f'{ign} Hypixel stats', colour=SBU_GOLD)

        embed.add_field(name='Rank', value=f'{player["rank"].replace("PLUS", "+").replace("_", "")}', inline=False)
        embed.add_field(name='Level:', value=f'{player["level"]}', inline=False)
        embed.add_field(name='Discord:', value=f'{player["links"]["DISCORD"]}', inline=False)
        embed.add_field(name='Online:', value=f'{player["online"]}', inline=False)

        if guild is None:
            embed.add_field(name='Guild:', value=f'{ign} isn\'t in a guild')
        else:
            embed.add_field(name='Guild:', value=guild["name"])
        await ctx.reply(embed=embed)

    @hypixel.error
    async def check_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=f'Error', description='Please enter an IGN\n Ex: `+hypixel RealMSpeed`',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return

    @commands.command(aliases=['s'])
    async def skycrypt(self, ctx: commands.Context, ign: str):
        await ctx.reply(f'https://sky.shiiyu.moe/stats/{ign}')

    @skycrypt.error
    async def check_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Please enter an IGN\n Ex: `+skycrypt RealMSpeed`')

    @commands.command()
    async def weightcheck(self, ctx):
        cursor: aiosqlite.Cursor = await self.db.cursor()
        await cursor.execute(User.select_row_with_id(ctx.author.id))
        data = await cursor.fetchone()

        if data is None:
            embed = discord.Embed(title="Error", description="You need to be verified to use this command \n`+verify <IGN>`", color=discord.Color.red())
            await ctx.reply(embed=embed)
            return

        data = User.dict_from_tuple(data)
        view = View()
        profiles = requests.get(f'https://sky.shiiyu.moe/api/v2/profile/{data["ign"]}').json()
        profile = None
        
        for prof in profiles["profiles"]:
            if profiles["profiles"][prof]["current"]:
                profile = profiles["profiles"][prof]
                break
        weight = int(profile["data"]["weight"]["senither"]["overall"])
        can_get_rank = False
        sbu = self.bot.get_guild(GUILD_ID)
        for role in WEIGHT_ROLES_INFO:
            if weight > WEIGHT_ROLES_INFO[role]["weight_req"]:
                if ctx.author.get_role(WEIGHT_ROLES_INFO[role]["role_id"]):
                    continue
                can_get_rank = True
                view.add_item(Role_Button(self.bot, role, ctx.author.id))

        if can_get_rank:
            view.add_item(Cancel_Button(ctx.author.id))
        else:
            embed = discord.Embed(title="You dont have enough weight", description="**You dont have enough weight for any of the next weight roles**", color=SBU_PURPLE)
            await ctx.reply(embed=embed)
            return

        
        embed = discord.Embed(title="Weight roles", description="You have enough weight to teach others! These ranks will grant you access to tutoring and carry systems, are you interested in providing these things for newer players? Any sort of toxicity in tickets or channels won’t be tolerated and will result in punishment.", color=SBU_GOLD)

        await ctx.reply(embed=embed, view=view)


class Role_Button(Button):
    def __init__(self, bot, role, user):
        super().__init__(label=WEIGHT_ROLES_INFO[role]["name"], style=discord.ButtonStyle.blurple)
        self.bot = bot
        self.role = role
        self.user = user
    async def callback(self, interaction):
        if interaction.user.id == self.user:
            view = View()
            view.add_item(Accept_Button(self.bot, self.role, self.user))
            view.add_item(Cancel_Button(self.user))

            name = WEIGHT_ROLES_INFO[self.role]["name"]

            embed = discord.Embed(title="Weight roles", description=f"Accepting the role will give you the {name} role and every role bellow it", color=SBU_GOLD)

            await interaction.response.edit_message(embed=embed, view=view)
        else:
            return
    
class Accept_Button(Button):
    def __init__(self, bot, role, user):
        super().__init__(label="Accept", style=discord.ButtonStyle.green)
        self.bot = bot
        self.role = role
        self.user = user
    async def callback(self, interaction):
        if interaction.user.id == self.user:
            sbu = self.bot.get_guild(GUILD_ID)
            roles = []
            role = sbu.get_role(WEIGHT_ROLES_INFO[self.role]["role_id"])
            roles.append(role)
            for r in WEIGHT_ROLES_INFO[self.role]["previous"]:
                r = sbu.get_role(r)
                roles.append(r)
            await interaction.user.add_roles(*roles, reason="Weight roles")

            await interaction.response.edit_message(content="Successfuly updated your roles!", view=None, embed=None)
        else:
            return


class Cancel_Button(Button):
    def __init__(self, user):
        super().__init__(label="Cancel", style=discord.ButtonStyle.red)
        self.user = user
    async def callback(self, interaction):
        if interaction.user.id == self.user:
            await interaction.response.edit_message(content="Command cancelled", view=None, embed=None)
        else:
            return


def setup(bot):
    bot.add_cog(Stats(bot))
