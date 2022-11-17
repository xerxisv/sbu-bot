import asyncio
import datetime
import os
import tarfile

import aiosqlite
import discord
import requests
from discord.ext import commands

from utils.constants import ADMIN_ROLE_ID, GUILDS_INFO, GUILD_ID, GUILD_MEMBER_ROLES_IDS, GUILD_MEMBER_ROLE_ID, \
    JR_ADMIN_ROLE_ID, SBU_GOLD, VERIFIED_ROLE_ID
from utils.database import DBConnection
from utils.database.schemas import User
from utils.error_utils import log_error

error_embed = discord.Embed(title=f'Error',
                            description='Something went wrong. Please try again later',
                            colour=0xFF0000)


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db: aiosqlite.Connection = DBConnection().get_db()
        self.key = os.getenv("apikey")

    @commands.command(description="Add the role if in guild")
    @commands.cooldown(1, 5)
    async def verify(self, ctx: commands.Context, ign: str = None):
        await ctx.trigger_typing()

        if ign is None:  # No IGN was inputted
            embed = discord.Embed(title=f'Error', description='Please enter a user \n `+verify RealMSpeed`',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return

        try:
            # Convert IGN to UUID
            response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}')

            assert response.status_code != 204  # Only returns 204 when the name inputted is wrong

            uuid = response.json()['id']
            ign = response.json()["name"]
        except AssertionError:  # In case of a 204
            embed = discord.Embed(title=f'Error',
                                  description='Error fetching information from the API. Recheck the spelling of your '
                                              'IGN',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        except Exception as exception:  # In case of anything else
            await log_error(ctx, exception)

            await ctx.reply(embed=error_embed)
            return

        # Remove the previous guild member role from the command invoker
        member: discord.Member = ctx.message.author
        await member \
            .remove_roles(*[discord.Object(_id) for _id in GUILD_MEMBER_ROLES_IDS],
                          reason='verification process',
                          atomic=False)
        await member \
            .remove_roles(*[discord.Object(GUILD_MEMBER_ROLE_ID)],
                          reason='verification process',
                          atomic=False)

        try:
            # Fetch player data
            response = requests.get(f'https://api.hypixel.net/player?key={self.key}&uuid={uuid}')
            assert response.status_code == 200, 'api.hypixel.net/player did not return a 200'
            player = response.json()['player']

            # Fetch guild data
            response = requests.get(f'https://api.hypixel.net/guild?key={self.key}&player={uuid}')
            assert response.status_code == 200, 'api.hypixel.net/guild did not return a 200'
            guild = response.json()['guild']

        except Exception as exception:  # Log any errors that might araise
            await log_error(ctx, exception)

            await ctx.reply(embed=error_embed)
            return

        try:
            if player['socialMedia']['links']['DISCORD'] != str(ctx.author):
                embed = discord.Embed(title=f'Error',
                                      description='The discord linked with your hypixel account is not the same as '
                                                  'the one you are trying to verify with. \n You can connect your '
                                                  'discord following https://youtu.be/6ZXaZ-chzWI',
                                      colour=0xFF0000)
                await ctx.reply(embed=embed)
                return
        except KeyError:
            embed = discord.Embed(title=f'Error',
                                  description='You haven\'t linked your discord with your hypixel account yet\n'
                                              'You can connect your discord following https://youtu.be/6ZXaZ-chzWI',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        except Exception as exception:
            await log_error(ctx, exception)

            await ctx.reply(embed=error_embed)
            return

        embed = discord.Embed()

        is_in_guild = False

        if guild is None or guild["name"].upper() not in GUILDS_INFO.keys():
            embed = discord.Embed(title=f'Verification',
                                  description='You are not in any of the SBU guilds. You are now verified without '
                                              'the guild member roles.',
                                  colour=0x800080)

        else:
            is_in_guild = True

        await member \
            .add_roles(*[discord.Object(_id) for _id in [VERIFIED_ROLE_ID]],
                       reason='Verification Complete', atomic=False)

        verified_member = User(uuid, member.id, ign)

        if is_in_guild:
            await member \
                .add_roles(*[discord.Object(GUILDS_INFO[guild["name"].upper()]['role_id']), discord.Object(GUILD_MEMBER_ROLE_ID)], atomic=False)

            embed = discord.Embed(title=f'Verification',
                                  description=f'You have been verified as a member of {guild["name"]}',
                                  colour=0x008000)

            verified_member.guild_uuid = guild['_id']

        cursor: aiosqlite.Cursor = await self.db.cursor()
        await cursor.execute(verified_member.find())
        res = (await cursor.fetchone())[0]

        if res == 0:
            await cursor.execute(*verified_member.insert())
        else:
            await cursor.execute(*verified_member.update())

        await self.db.commit()

        try:
            await member.edit(nick=player["displayname"])

        except Exception as exception:
            embed.add_field(name="Nickname:", value="Unable to edit nickname.")

            await log_error(ctx, exception)

        await ctx.reply(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5)
    async def unverify(self, ctx: commands.Context):
        await ctx.trigger_typing()
        member: discord.Member = ctx.message.author

        await member \
            .remove_roles(*[discord.Object(_id) for _id in
                            [*GUILD_MEMBER_ROLES_IDS, GUILD_MEMBER_ROLE_ID, VERIFIED_ROLE_ID]],
                          atomic=False
                          )

        await self.db.execute(User.unverify_row_with_id(member.id))
        await self.db.commit()

        embed = discord.Embed(title=f'Verification',
                              description=f'You have been unverified.',
                              colour=0x008000)
        await ctx.reply(embed=embed)

    @commands.command(name="forcereverify", aliases=["reverify"])
    @commands.has_role(ADMIN_ROLE_ID)
    async def force_reverify(self, ctx: commands.Context, user: discord.Member):
        await ctx.trigger_typing()

        cursor: aiosqlite.Cursor = await self.db.cursor()
        await cursor.execute(User.select_row_with_id(user.id))
        data = await cursor.fetchone()
        await cursor.close()

        data = User.dict_from_tuple(data)
        uuid = data["uuid"]
        guild_uuid = data["guild_uuid"]

        roles_to_remove = None

        try:
            # Fetch player data
            response = requests.get(f'https://api.hypixel.net/player?key={self.key}&uuid={uuid}')
            assert response.status_code == 200, 'api.hypixel.net/player did not return a 200'
            player = response.json()['player']

            # Fetch guild data
            response = requests.get(f'https://api.hypixel.net/guild?key={self.key}&player={uuid}')
            assert response.status_code == 200, 'api.hypixel.net/guild did not return a 200'
            guild = response.json()['guild']

        except Exception as exception:  # Log any errors that might araise
            await log_error(ctx, exception)

        else:

            if player['socialMedia']['links']['DISCORD'] != str(ctx.author):
                roles_to_remove = [discord.Object(_id) for _id in
                                   [*GUILD_MEMBER_ROLES_IDS, GUILD_MEMBER_ROLE_ID,
                                    VERIFIED_ROLE_ID]]

                await self.db.execute(User.unverify_row_with_id(user.id))

            if guild is None or guild["_id"] != guild_uuid:
                roles_to_remove = [discord.Object(_id) for _id in
                                   [*GUILD_MEMBER_ROLES_IDS, GUILD_MEMBER_ROLE_ID]]

                await self.db.execute(User.update_row_with_id(uuid))
            if roles_to_remove is not None:
                await user.remove_roles(*roles_to_remove,
                                        atomic=False,
                                        reason='check_verified')

            embed = discord.Embed(
                title='Success',
                description=f'Reverified {user.mention}',
                colour=0x00FF00
            )
            await ctx.reply(embed=embed)

    @force_reverify.error
    async def force_reverify_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+forcereverify <@mention | ID>`.',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

    @commands.command(name="forcereverifyall", aliases=["reverifyall", "reverify_all"])
    @commands.has_role(ADMIN_ROLE_ID)
    async def force_reverify_all(self, ctx: commands.Context):
        embed = discord.Embed(
            description='Reverifying everyone now <a:loading:978732444998070304>.\nThis might take a while.',
            colour=SBU_GOLD
        )
        msg = await ctx.reply(embed=embed)

        cursor: aiosqlite.Cursor = await self.db.cursor()

        sbu = self.bot.get_guild(GUILD_ID)
        uuids: tuple = ()

        # loop for each guild
        for guild in GUILDS_INFO:
            guild_uuid = GUILDS_INFO[guild]["guild_uuid"]

            resp = requests.get(f"https://api.slothpixel.me/api/guilds/id/{guild_uuid}")
            data = resp.json()
            guild_members = data["members"]

            # fetch verified members with specific guild
            await cursor.execute(User.select_rows_with_guild_uuid(guild_uuid))
            verified_members = await cursor.fetchall()
            # for each verified member
            for v_member in verified_members:
                # convert tuple to dict
                v_member = User.dict_from_tuple(v_member)
                # check if there is any verified members in the specific guild
                if not any(g_member['uuid'] == v_member['uuid'] for g_member in guild_members):
                    discord_member = sbu.get_member(v_member["discord_id"])
                    # Check if member is still in server
                    if discord_member:
                        roles_to_remove = [discord.Object(_id) for _id in
                                           [*GUILD_MEMBER_ROLES_IDS, GUILD_MEMBER_ROLE_ID,
                                            VERIFIED_ROLE_ID]]
                        await discord_member.remove_roles(*roles_to_remove,
                                                          atomic=False,
                                                          reason='check_verified')
                        uuids = uuids + (v_member['uuid'],)
        await cursor.execute(User.update_rows_with_ids([f"'{uuid}'" for uuid in uuids]))
        await cursor.close()
        await self.db.commit()

        embed = discord.Embed(
            title='Success',
            description='Everyone has been reverified',
            colour=0x00FF00
        )
        await msg.edit(embed=embed)

    @commands.command(name="forceunverify", aliases=["unverifyforce", "unverify_force"])
    @commands.has_role(JR_ADMIN_ROLE_ID)
    async def force_unverify(self, ctx: commands.Context, user: discord.Member):
        await ctx.trigger_typing()
        # make sure the user is still in the server
        if not user:
            embed = discord.Embed(
                title='Error',
                description='Invalid user. Make sure user is a member of the server',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        await self.db.execute(User.unverify_row_with_id(user.id))  # unverify the user
        await self.db.commit()

        roles_to_remove = [discord.Object(_id) for _id in
                           [*GUILD_MEMBER_ROLES_IDS, GUILD_MEMBER_ROLE_ID,
                            VERIFIED_ROLE_ID]]

        await user.remove_roles(*roles_to_remove,
                                atomic=False,
                                reason='check_verified')

        embed = discord.Embed(
            title='Success',
            description=f'Unverified {user.mention}',
            colour=0x00FF00
        )
        await ctx.reply(embed=embed)

    @force_unverify.error
    async def force_unverify_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+forceunverify <@mention | ID>`.',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

    @commands.command(name="forceunverifyall", aliases=["force_unverify_all", "unverifyall", "unverify_all"])
    @commands.has_role(ADMIN_ROLE_ID)
    async def force_unverify_all(self, ctx: commands.Context):
        def check(m: discord.Message):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        embed = discord.Embed(color=discord.Color.red(), title="**WARNING**",
                              description='Doing this will unverify **EVERYONE** saved in the database, '
                                          'are you sure you want to do this? '
                                          '\n__**Type "yes" if you are sure, '
                                          'typing anything else or send nothing in 30 seconds this command '
                                          'will be canceled automatically**__')
        await ctx.reply(embed=embed)

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send(f"Command canceled")
            return
        else:
            if msg.content != "yes":
                await ctx.send("Command canceled")
                return

            embed = discord.Embed(
                description='Unverifying everyone now <a:loading:978732444998070304>.\nThis might take a while.',
                colour=SBU_GOLD
            )
            msg = await ctx.reply(embed=embed)

            cursor: aiosqlite.Cursor = await self.db.cursor()

            # fetch verified members with specific guild
            await cursor.execute(User.select_all())
            verified_members = await cursor.fetchall()

            sbu = self.bot.get_guild(GUILD_ID)
            # for each verified member
            for v_member in verified_members:
                # convert tuple to dict
                v_member = User.dict_from_tuple(v_member)
                discord_member = sbu.get_member(v_member["discord_id"])
                # Check if member is still in server
                if discord_member:
                    roles_to_remove = [discord.Object(_id) for _id in
                                       [*GUILD_MEMBER_ROLES_IDS, GUILD_MEMBER_ROLE_ID,
                                        VERIFIED_ROLE_ID]]
                    await discord_member.remove_roles(*roles_to_remove,
                                                      atomic=False,
                                                      reason='check_verified')
            # create a backup of the database
            with tarfile.open(f"./backup/{int(datetime.datetime.now().timestamp())}.tar.gz", "w:gz") as tar_handle:
                for root, dirs, files in os.walk("./data"):
                    for file in files:
                        if file.endswith(".db"):
                            tar_handle.add(os.path.join(root, file), arcname=file)
            # unverify everyone
            await cursor.execute(User.unverify_all())
            await cursor.close()
            await self.db.commit()
            embed = discord.Embed(
                title='Success',
                description='Everyone has been unverified',
                colour=0x00FF00
            )
            await msg.reply(embed=embed)


def setup(bot):
    bot.add_cog(Verify(bot))
