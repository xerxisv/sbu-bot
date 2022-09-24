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
from utils.constants import GUILDS_INFO, MODERATOR_ROLE_ID, SBU_GOLD
from utils.error_utils import log_error
from utils.schemas.InactivePlayerSchema import InactivePlayer
from utils.schemas.VerifiedMemberSchema import VerifiedMember

dotenv.load_dotenv()


class InactiveList(commands.Cog):
    key = os.getenv("apikey")
    min_exp = 1

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Group
    async def inactive(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('inactive help').invoke(ctx)

    @inactive.command()
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title='Command Help',
            colour=SBU_GOLD
        )

        embed.add_field(name='Add yourself to the inactivity list',
                        value='`+inactive add <time>`\n'
                              '*You need to be __verified__*',
                        inline=False)
        embed.add_field(name='Check the inactive players in a guild',
                        value='`+inactive check <guild>`\n'
                              '*__Moderator__ command*',
                        inline=False)
        embed.add_field(name='Add a player to the inactivity list',
                        value='`+inactive mod add <IGN> <time>`\n'
                              '*__Moderator__ command*',
                        inline=False)
        embed.add_field(name='Remove a player from the inactivity list',
                        value='`+inactive mod remove <IGN>`\n'
                              '*__Moderator__ command*',
                        inline=False)

        await ctx.reply(embed=embed)

    @inactive.command()
    async def add(self, ctx: commands.Context, afk_time: str):
        try:
            afk_time = humanfriendly.parse_timespan(afk_time)
            if afk_time < 604800 or afk_time > 2592000:
                embed = discord.Embed(
                    title=f'Error',
                    description='Invalid Time \nEnter time in days.\n Min 7, max 30. Ex: 10d for 10 days\n'
                                '`+inactive add 10d`',
                    colour=0xFF0000
                )
                await ctx.reply(embed=embed)
                return

        except humanfriendly.InvalidTimespan:
            embed = discord.Embed(title=f'Error',
                                  description='Invalid Time \nEnter time in days Ex: 10d for 10 days\n'
                                              '`+inactive add 10d`',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return

        db = await aiosqlite.connect(VerifiedMember.DB_PATH + VerifiedMember.DB_NAME + '.db')
        cursor = await db.cursor()

        await cursor.execute(VerifiedMember.select_row_with_id(ctx.author.id))
        member = await cursor.fetchone()

        await db.close()

        if member is None:
            embed = discord.Embed(title=f'Error',
                                  description='You need to be verified to run this command',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return

        member = VerifiedMember.dict_from_tuple(member)

        cur_time = time.time()
        afk_time = cur_time + afk_time

        new_inactive = InactivePlayer(member['uuid'], ctx.author.id, member['guild_uuid'], int(afk_time))

        db = await aiosqlite.connect(InactivePlayer.DB_PATH + InactivePlayer.DB_NAME + '.db')
        cursor = await db.cursor()

        await cursor.execute(*(new_inactive.insert()))

        await db.commit()
        await db.close()

        embed = discord.Embed(title=f'Success',
                              description=f'You have been added to Inactive list until '
                                          f'{datetime.datetime.fromtimestamp(afk_time).strftime("%A, %B %d")}',
                              colour=0x00FF00)

        await ctx.reply(embed=embed)

    @add.error
    async def inactiveadd_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(title=f'Error',
                                  description='No time inputted \nEnter time in days Ex: 10d for 10 days\n'
                                              '`+inactive add 10d`',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)

    @inactive.command()
    # @commands.cooldown(1, 60)
    @commands.has_role(MODERATOR_ROLE_ID)
    async def check(self, ctx, *, guild: str):
        db = await aiosqlite.connect(InactivePlayer.DB_PATH + InactivePlayer.DB_NAME + '.db')

        cursor = await db.cursor()
        await cursor.execute('''SELECT * FROM INACTIVES''')

        values = await cursor.fetchall()
        inactives_uuids = [inactive[0] for inactive in values]  # puts all the UUIDs in an array

        # If inputted guild is invalid
        if guild.upper() not in GUILDS_INFO.keys():
            embed_var = discord.Embed(color=ctx.author.color,
                                      description=f"Inputted guild is not an SBU guild",
                                      colour=0xFF0000)
            await ctx.send(embed=embed_var)
            return

        data = requests.get(
            url="https://api.hypixel.net/guild",
            params={
                "key": self.key,
                "name": guild
            }).json()

        embed_var = discord.Embed(color=ctx.author.color,
                                  title=f"Inactive List for {data['guild']['name']}",
                                  description=f"<a:loading:978732444998070304> Skyblock University is thinking",
                                  colour=0xFFFF00)
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

            try:  # try the member's IGN
                data3 = requests.get(url=f"https://api.mojang.com/user/profile/{player['uuid']}").json()

            except Exception as exception:  # If there is an exception, log it and add the uuid in the embed
                await log_error(ctx, exception)
                embed_msg += f'{player["uuid"]}\n'

            else:  # If no error, add IGN in embed instead
                username = data3["name"]
                embed_msg += f"`{username}`\n"

            total_inactive += 1  # Increment the inactive total

        embed_var = discord.Embed(color=0x00FF00,
                                  title=f"Inactive List for {data['guild']['name']}",
                                  description=f"{total_inactive} members were found to be under {self.min_exp} GEXP."
                                              + f"\n\n{embed_msg}")
        await message.edit(embed=embed_var)

        await db.close()

    @check.error
    async def inactive_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(color=ctx.author.color,
                                  description=f"No guild inputted, `+inactive check <guild>`",
                                  colour=0xFF0000)
            await ctx.send(embed=embed)

    @inactive.group()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def mod(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('inactive help').invoke(ctx)

    @mod.command(name='add')
    async def add_(self, ctx: commands.Context, ign: str, afk_time: str):
        try:
            afk_time = int(humanfriendly.parse_timespan(afk_time))
            if afk_time < 604800 or afk_time > 2592000:
                embed = discord.Embed(
                    title=f'Error',
                    description='Invalid Time \nEnter time in days.\n Min 7, max 30. Ex: 10d for 10 days\n'
                                '`+inactive add 10d`',
                    colour=0xFF0000
                )
                await ctx.reply(embed=embed)
                return

        except humanfriendly.InvalidTimespan:
            embed = discord.Embed(title=f'Error',
                                  description='Invalid Time \nEnter time in days Ex: 10d for 10 days\n'
                                              '`+inactive add 10d`',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return

        uuid = extract_uuid(ign)

        if uuid is None:
            embed = discord.Embed(
                title='Error',
                description='Player not found',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        res = requests.get(f'https://api.hypixel.net/guild?player={uuid}&key={self.key}')
        data = res.json()

        print(data)

        if res.status_code != 200 or data['guild'] is None:
            embed = discord.Embed(
                title='Error',
                description='User either not found, or is not in a guild',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        guild_id = res.json()['guild']['_id']

        db = await aiosqlite.connect(InactivePlayer.DB_PATH + InactivePlayer.DB_NAME + '.db')
        cursor: aiosqlite.Cursor = await db.cursor()

        inactive = InactivePlayer(uuid, 1, guild_id, int(time.time()) + afk_time)

        await cursor.execute(*(inactive.insert()))

        embed = discord.Embed(
            title='Success',
            description=f'Successfully added {ign} to the inactive list',
            colour=0x00FF00
        )

        await db.commit()
        await db.close()
        await ctx.reply(embed=embed)

    @add_.error
    async def mod_add_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.MissingRequiredArgument, commands.BadArgument)):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+inactive mod add <IGN> <afk_time>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)

    @mod.command(name='remove', aliases=['rm', 'delete', 'del'])
    async def remove_(self, ctx: commands.Context, ign: str):
        uuid = extract_uuid(ign)

        if uuid is None:
            embed = discord.Embed(
                title='Error',
                description='Player not found',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        db = await aiosqlite.connect(InactivePlayer.DB_PATH + InactivePlayer.DB_NAME + '.db')
        cursor = await db.cursor()

        await cursor.execute(InactivePlayer.delete_row_with_uuid(uuid))

        embed = discord.Embed(
            title='Success',
            description=f'Successfully removed {ign} from inactives.',
            colour=0x00FF00
        )

        await ctx.reply(embed=embed)

        await db.commit()
        await db.close()

    @remove_.error
    async def mod_remove_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.MissingRequiredArgument, commands.BadArgument)):
            embed = discord.Embed(
                title='Error',
                description='',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(InactiveList(bot))
