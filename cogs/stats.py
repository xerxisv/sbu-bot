import aiosqlite
import discord
import discord.utils
import requests
from discord.ext import commands
from discord.ui import Button, View

from utils import check_if_weight_banned
from utils.constants import FRESHMAN_ROLE_ID, GUILD_ID, SBU_ERROR, SBU_GOLD, SBU_PURPLE, SBU_SUCCESS, WEIGHT_ROLES_INFO
from utils.database import DBConnection
from utils.database.schemas import User


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
    async def hypixel_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=f'Error', description='Please enter an IGN\n Ex: `+hypixel RealMSpeed`',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return

    @commands.command(aliases=['s'])
    async def skycrypt(self, ctx: commands.Context, ign: str):
        await ctx.reply(f'https://sky.shiiyu.moe/stats/{ign}')

    @skycrypt.error
    async def skycrypt_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Please enter an IGN\n Ex: `+skycrypt RealMSpeed`')

    @commands.command(name='weightcheck')
    @commands.check(check_if_weight_banned)
    async def weight_check(self, ctx: commands.Context, cute_name: str = None):
        await ctx.trigger_typing()

        if cute_name and cute_name.lower() not in ['apple', 'banana', 'blueberry', 'coconut', 'cucumber', 'grapes',
                                                   'kiwi', 'lemon', 'lime', 'mango', 'orange', 'papaya', 'pear',
                                                   'peach', 'pineapple', 'pomegranate', 'raspberry', 'strawberry',
                                                   'tomato', 'watermelon', 'zucchini']:
            embed = discord.Embed(
                title='Error',
                description='Invalid profile.',
                colour=SBU_ERROR
            )
            await ctx.reply(embed=embed)
            return

        cursor: aiosqlite.Cursor = await self.db.cursor()

        await cursor.execute(User.select_row_with_id(ctx.author.id))
        data = await cursor.fetchone()

        await cursor.close()

        if data is None:
            embed = discord.Embed(
                title="Error",
                description="You need to be verified to use this command.\n`+verify <IGN>`",
                color=SBU_ERROR
            )
            await ctx.reply(embed=embed)
            return

        data = User.dict_from_tuple(data)
        view = View()
        profiles = requests.get(f'https://sky.shiiyu.moe/api/v2/profile/{data["ign"]}').json()
        profile = None

        is_valid_profile = cute_name is None

        for prof in profiles["profiles"].values():
            if cute_name is not None:
                if prof["cute_name"].lower() != cute_name.lower():
                    continue
                is_valid_profile = True
                profile = prof
                break

            if prof["current"]:
                profile = prof
                break

        if not is_valid_profile:
            embed = discord.Embed(
                title='Error',
                description=f'You have no {cute_name.title()} profile.',
                colour=SBU_ERROR
            )
            await ctx.reply(embed=embed)
            return

        weight = int(profile["data"]["weight"]["senither"]["overall"])
        has_previous_role = False
        max_role = None
        for role in WEIGHT_ROLES_INFO:
            if weight > WEIGHT_ROLES_INFO[role]["weight_req"]:
                if ctx.author.get_role(WEIGHT_ROLES_INFO[role]["role_id"]):
                    has_previous_role = True
                    continue
                max_role = role

        if max_role is not None:
            if not has_previous_role:
                view.add_item(RoleButton(self.bot, max_role, ctx.author.id))
                embed = discord.Embed(
                    title='Weight roles',
                    description='You have enough weight to teach others! These ranks will grant you access to our '
                                'tutoring and carry systems. Are you interested in providing these things for newer '
                                'players? Any sort of toxicity in tickets or channels won’t be tolerated and will '
                                'result in punishment.',
                    color=SBU_GOLD)
            else:
                view.add_item(RoleButton(self.bot, max_role, ctx.author.id))
                embed = discord.Embed(
                    title='Weight roles',
                    description='You have enough weight for the next role',
                    color=SBU_GOLD
                )
            view.add_item(CancelButton(ctx.author.id))

        else:
            embed = discord.Embed(
                title='Weight roles',
                description='You dont have enough weight for any of the next weight roles',
                color=SBU_PURPLE)

        embed.set_footer(text=f'{data["ign"]} - {profile["cute_name"]}')

        await ctx.reply(embed=embed, view=view)

    @weight_check.error
    async def weight_check_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.CheckFailure):
            embed = discord.Embed(
                title='Error',
                description='You have been banned from applying for weight roles.',
                colour=SBU_ERROR
            )
            await ctx.reply(embed=embed)
            return


class RoleButton(Button):
    def __init__(self, bot, role, user):
        super().__init__(label=WEIGHT_ROLES_INFO[role]["name"], style=discord.ButtonStyle.blurple)
        self.bot = bot
        self.role = role
        self.user = user

    async def callback(self, interaction):
        if interaction.user.id == self.user:
            view = View()
            view.add_item(AcceptButton(self.bot, self.role, self.user))
            view.add_item(CancelButton(self.user))

            name = WEIGHT_ROLES_INFO[self.role]["role_id"]

            embed = discord.Embed(title="Weight roles",
                                  description=f"By clicking *'Accept'* you will be given the <@&{name}> "
                                              f"role.",
                                  color=SBU_GOLD)

            await interaction.response.edit_message(embed=embed, view=view)
        else:
            return


class AcceptButton(Button):
    def __init__(self, bot, role, user):
        super().__init__(label='Accept', style=discord.ButtonStyle.green)
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

            role = sbu.get_role(FRESHMAN_ROLE_ID)
            await interaction.user.remove_roles(*[role], reason="Weight roles")

            embed = discord.Embed(
                title='Success',
                description='Successfully updated your roles!',
                colour=SBU_SUCCESS
            )

            await interaction.response.edit_message(view=None, embed=embed)


class CancelButton(Button):
    def __init__(self, user):
        super().__init__(label="Cancel", style=discord.ButtonStyle.red)
        self.user = user

    async def callback(self, interaction):
        if interaction.user.id == self.user:
            embed = discord.Embed(
                title='Weight Roles',
                description='Command canceled.',
                color=SBU_PURPLE
            )
            await interaction.response.edit_message(view=None, embed=embed)


def setup(bot):
    bot.add_cog(Stats(bot))
