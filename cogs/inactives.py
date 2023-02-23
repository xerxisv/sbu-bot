import datetime
import os
import time

import aiosqlite
import discord
import dotenv
import humanfriendly
import requests
from discord.ext import commands

from utils import extract_uuid
from utils.config.config import ConfigHandler
from utils.database import DBConnection
from utils.database.schemas import User
from utils.error_utils import log_error

dotenv.load_dotenv()
config = ConfigHandler().get_config()


class InactiveList(commands.Cog):
    key = os.getenv("APIKEY")
    min_exp = 1

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db: aiosqlite.Connection = DBConnection().get_db()

    @commands.group(name='inactive', aliases=['inactives'], case_insensitive=True)
    async def inactive(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('inactive help').invoke(ctx)
            return
        await ctx.trigger_typing()

    @inactive.command(name='help', aliases=['commands'])
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title='Command Help',
            color=config['colors']['primary']
        )

        embed.add_field(name='Add yourself to the inactivity list',
                        value='`+inactive add <time>`\n'
                              '*You need to be __verified__*',
                        inline=False)
        embed.add_field(name='Check the inactive players in a guild',
                        value='`+inactive check <guild>`\n'
                              '*__Junior Moderator__ command*',
                        inline=False)
        embed.add_field(name='Add a player to the inactivity list',
                        value='`+inactive mod add <IGN> <time>`\n'
                              '*__Junior Moderator__ command*',
                        inline=False)
        embed.add_field(name='Remove a player from the inactivity list',
                        value='`+inactive mod remove <IGN>`\n'
                              '*__Junior Moderator__ command*',
                        inline=False)
        embed.add_field(name='Command aliases list',
                        value='`+inactive aliases`',
                        inline=False)

        await ctx.reply(embed=embed)

    @inactive.command(name='alias', aliases=['aliases'])
    async def alias(self, ctx: commands.Context):
        embed = discord.Embed(
            title='Command aliases',
            color=config['colors']['primary']
        )

        embed.add_field(name='inactive', value='"inactives"', inline=False)
        embed.add_field(name='add', value='None', inline=False)
        embed.add_field(name='check', value='None', inline=False)
        embed.add_field(name='mod', value='"moderator"', inline=False)
        embed.add_field(name='remove', value='"rm", "delete", "del"', inline=False)

        await ctx.reply(embed=embed)

    @inactive.command()
    @commands.cooldown(1, 5)
    async def add(self, ctx: commands.Context, afk_time: str):
        try:
            afk_time = humanfriendly.parse_timespan(afk_time)
            if afk_time < 604800 or afk_time > 2592000:
                embed = discord.Embed(
                    title='Error',
                    description='Invalid Time \nEnter time in days.\n Min 7, max 30. Ex: 10d for 10 days\n'
                                '`+inactive add 10d`',
                    color=config['colors']['error']
                )
                await ctx.reply(embed=embed)
                return

        except humanfriendly.InvalidTimespan:
            embed = discord.Embed(
                title=f'Error',
                description='Invalid Time \nEnter time in days Ex: 10d for 10 days\n`+inactive add 10d`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        cursor: aiosqlite.Cursor = await self.db.cursor()

        await cursor.execute(User.select_row_with_id(ctx.author.id))
        member = await cursor.fetchone()
        await cursor.close()

        if member is None:
            embed = discord.Embed(
                title=f'Error',
                description='You need to be verified to run this command.\nRun `+verify <IGN>`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        member = User.dict_from_tuple(member)

        cur_time = time.time()
        afk_time = cur_time + afk_time

        await self.db.execute(User.add_inactive(member['uuid'], int(afk_time)))
        await self.db.commit()

        embed = discord.Embed(
            title=f'Success',
            description=f'You have been added to Inactive list until '
                        f'{datetime.datetime.fromtimestamp(afk_time).strftime("%A, %B %d")}',
            color=config['colors']['success']
        )

        await ctx.reply(embed=embed)

    @add.error
    async def inactiveadd_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title=f'Error',
                description='No time inputted \nEnter time in days Ex: 10d for 10 days\n'
                            '`+inactive add 10d`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)

    @inactive.command()
    @commands.cooldown(1, 30)
    @commands.has_role(config['jr_mod_role_id'])
    async def check(self, ctx: commands.Context, *, guild: str):
        # If inputted guild is invalid
        if guild.upper() not in config['guilds'].keys():
            embed_var = discord.Embed(
                title='Error',
                description=f"Inputted guild is not an SBU guild",
                color=config['colors']['error']
            )
            await ctx.send(embed=embed_var)
            return

        cursor = await self.db.cursor()
        await cursor.execute('''
                SELECT *
                FROM USERS
                WHERE inactive_until IS NOT null
            ''')

        values = await cursor.fetchall()
        await cursor.close()

        inactives_uuids = [inactive[0] for inactive in values]  # puts all the UUIDs in an array

        data = requests.get(
            url="https://api.hypixel.net/guild",
            params={
                "key": self.key,
                "name": guild
            }).json()

        embed_var = discord.Embed(
            title=f"Inactive List for {data['guild']['name']}",
            description=f"<a:loading:978732444998070304> Skyblock University is thinking",
            color=config['colors']['secondary']
        )
        await ctx.trigger_typing()
        message = await ctx.send(embed=embed_var)

        embed_msg = ""  # List of inactive IGNs (or UUIDs if API error)
        total_inactive = 0  # Sum of inactive players

        for player in data["guild"]["members"]:  # for every member in the guild
            exp_7d_total = 0

            for key in player["expHistory"]:  # find his total exp over the past 7 days
                exp_7d_total += player["expHistory"][key]

            # if total exp is over the minimum or player uuid is in the inactives then go to next member
            if exp_7d_total > self.min_exp or player["uuid"] in inactives_uuids:
                continue

            try:  # Fetch player info from hypixel API
                hypixel_res = requests.get(f"https://api.hypixel.net/player?key={self.key}&uuid={player['uuid']}")
                # Ensure OK status
                assert hypixel_res.status_code == 200, 'Hypixel did not return a 200'

                hypixel_prof = hypixel_res.json()
                # Ensure player exists
                assert hypixel_prof['player'] is not None, f'Player with UUID {player["uuid"]} not found'

            except Exception as exception:  # If there is an exception, log it and add the uuid in the embed
                await log_error(ctx, exception)
                embed_msg += f'{player["uuid"]}\n'

            else:  # Else
                # Continue if player has logged in the last 7 days
                try:
                    if (hypixel_prof['player']['lastLogin'] / 1000) + 604800 > time.time():
                        continue
                except KeyError:
                    pass
                # Add him to inactives if not
                username = hypixel_prof['player']['displayname']
                embed_msg += f"`{username}`\n"

            total_inactive += 1  # Increment the inactive total

        embed_var = discord.Embed(
            title=f"Inactive List for {data['guild']['name']}",
            description=f"{total_inactive} members were found to be inactive."
                        + f"\n\n{embed_msg}",
            color=config['colors']['primary']
        )
        await message.edit(embed=embed_var)

    @check.error
    async def inactive_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description=f"No guild inputted, `+inactive check <guild>`",
                color=config['colors']['error']
            )
            await ctx.send(embed=embed)

    @inactive.group(name='mod', aliases=['moderator'], case_insensitive=True)
    @commands.has_role(config['jr_mod_role_id'])
    async def mod(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('inactive help').invoke(ctx)

    @mod.command(name='add')
    @commands.cooldown(1, 5)
    async def add_(self, ctx: commands.Context, ign: str, afk_time: str):
        try:
            afk_time = int(humanfriendly.parse_timespan(afk_time))
            if afk_time < 604800 or afk_time > 2592000:
                embed = discord.Embed(
                    title=f'Error',
                    description='Invalid Time \nEnter time in days.\n Min 7, max 30. Ex: 10d for 10 days\n'
                                '`+inactive add 10d`',
                    color=config['colors']['error']
                )
                await ctx.reply(embed=embed)
                return

        except humanfriendly.InvalidTimespan:
            embed = discord.Embed(
                title=f'Error',
                description='Invalid Time \nEnter time in days Ex: 10d for 10 days\n'
                            '`+inactive add 10d`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        uuid = extract_uuid(ign)

        if uuid is None:
            embed = discord.Embed(
                title='Error',
                description='User not found',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        res = requests.get(f'https://api.hypixel.net/guild?player={uuid}&key={self.key}')
        data = res.json()

        if res.status_code != 200 or data['guild'] is None:
            embed = discord.Embed(
                title='Error',
                description='User either not found, or is not in a guild',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        await self.db.execute(User.add_inactive(uuid, int(time.time()) + afk_time))

        embed = discord.Embed(
            title='Success',
            description=f'Successfully added {ign} to the inactive list until '
                        f'{datetime.datetime.fromtimestamp(int(time.time()) + afk_time).strftime("%A, %B %d")}',
            color=config['colors']['success']
        )

        await self.db.commit()
        await ctx.reply(embed=embed)

    @add_.error
    async def mod_add_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.MissingRequiredArgument, commands.BadArgument)):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+inactive mod add <IGN> <afk_time>`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)

    @mod.command(name='remove', aliases=['rm', 'delete', 'del'])
    @commands.cooldown(1, 5)
    async def remove_(self, ctx: commands.Context, ign: str):
        uuid = extract_uuid(ign)

        if uuid is None:
            embed = discord.Embed(
                title='Error',
                description='Player not found',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        await self.db.execute(User.remove_inactive(uuid))

        embed = discord.Embed(
            title='Success',
            description=f'Successfully removed {ign} from inactives.',
            color=config['colors']['success']
        )

        await self.db.commit()
        await ctx.reply(embed=embed)

    @remove_.error
    async def mod_remove_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.MissingRequiredArgument, commands.BadArgument)):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+inactive mod remove <IGN>`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(InactiveList(bot))
