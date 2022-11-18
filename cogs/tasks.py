import datetime
import json
import os
import tarfile
from asyncio import sleep

import aiohttp
import aiosqlite
import discord
import dotenv
from discord.ext import commands, tasks

from utils import constants
from utils.database import DBConnection
from utils.database.schemas import User
from utils.error_utils import exception_to_string


class TasksCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        dotenv.load_dotenv()
        self.bot = bot
        self.db: aiosqlite.Connection = DBConnection().get_db()
        self.key = os.getenv('apikey')
        self.update_members.start()
        self.auto_qotd.start()
        self.backup_db.start()
        self.inactives_check.start()
        self.check_verified.start()
        self.weekly_tatsu.start()
        self.booster_log.start()

    def cog_unload(self):
        self.update_members.cancel()
        self.auto_qotd.cancel()
        self.backup_db.cancel()
        self.inactives_check.cancel()
        self.check_verified.cancel()
        self.weekly_tatsu.cancel()
        self.booster_log.cancel()

    @tasks.loop(hours=1)
    async def update_members(self):
        total_members = 0  # Stores the member count of all the guilds combined
        for idx, guild in enumerate(constants.GUILDS_INFO.keys()):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.hypixel.net/guild?key={self.key}&id='
                                           f'{constants.GUILDS_INFO[guild]["guild_uuid"]}') as resp:
                        assert resp.status == 200  # Unless a guild gets deleted this will never raise

                        guild_info = (await resp.json())["guild"]

            except AssertionError:
                await self.bot \
                    .get_channel(constants.SBU_BOT_LOGS_CHANNEL_ID) \
                    .send(f'Guild info fetch with id `{constants.GUILDS_INFO[guild]["guild_uuid"]}` '
                          'did not return a 200.')

            except Exception as exception:
                await self.bot \
                    .get_channel(constants.SBU_BOT_LOGS_CHANNEL_ID) \
                    .send(exception_to_string('update_member task', exception))

            else:
                new_name = f'{guild_info["name"]}: {str(len(guild_info["members"]))}'
                total_members += int(len(guild_info["members"]))

                vc = self.bot.get_channel(constants.GUILDS_INFO[guild]['vc_id'])

                await vc.edit(name=new_name)

        total_member_vc = self.bot.get_channel(constants.TOTAL_MEMBER_COUNT_VC_ID)
        new_name = "Guild members: " + str(total_members)
        await total_member_vc.edit(name=new_name)

    @tasks.loop(hours=24)
    async def auto_qotd(self):
        qotd_channel = self.bot.get_channel(constants.QOTD_CHANNEL_ID)
        mod_chat = self.bot.get_channel(constants.MOD_CHAT_CHANNEL_ID)

        with open(constants.QOTD_PATH) as f:
            qotd_obj = json.load(f)

        qotd_list = list(qotd_obj)
        if len(qotd_list) < 1:
            await mod_chat.send(
                f"<@&{constants.JR_MOD_ROLE_ID}> no QOTD's left in the archive. Automatic qotd canceled.\n"
                f"Please add more using `+qotd add`.")
            return

        try:
            message = await qotd_channel.fetch_message(qotd_channel.last_message_id)
            await message.thread.edit(locked=True, archived=True)
        except AttributeError:
            pass

        message = await qotd_channel.send(qotd_list[0]["qotd"] + f" <@&{constants.QOTD_ROLE_ID}>")
        await message.create_thread(name="QOTD")

        qotd_list.pop(0)

        with open(constants.QOTD_PATH, 'w') as json_file:
            json.dump(qotd_list, json_file,
                      indent=4,
                      separators=(',', ': '))

        num1 = len(qotd_list)

        if num1 < 3:
            await mod_chat.send(
                f"<@&{constants.JR_MOD_ROLE_ID}> QOTD's Running Low. Only {num1} remain.\n"
                f"Please add more using `+qotd add`.")

    @auto_qotd.before_loop
    async def wait_until_next(self):
        next_midnight = datetime.datetime.now().timestamp() - (datetime.datetime.now().timestamp() % 86400) + 86400
        seconds_until_next = next_midnight - datetime.datetime.now().timestamp()
        await sleep(seconds_until_next)

    @tasks.loop(hours=24)
    async def backup_db(self):
        with tarfile.open("./backup/backup.tar.gz", "w:gz") as tar_handle:
            for root, dirs, files in os.walk("./data"):
                for file in files:
                    if file.endswith(".db"):
                        tar_handle.add(os.path.join(root, file), arcname=file)

    @tasks.loop(hours=24)
    async def check_verified(self):
        cursor: aiosqlite.Cursor = await self.db.cursor()

        sbu = self.bot.get_guild(constants.GUILD_ID)
        uuids: tuple = ()

        # loop for each guild
        for guild in constants.GUILDS_INFO:
            guild_uuid = constants.GUILDS_INFO[guild]["guild_uuid"]

            async with aiohttp.ClientSession() as session:  # fetch guild members
                async with session.get(f"https://api.hypixel.net/guild?id={guild_uuid}&key={self.key}") as resp:
                    data = await resp.json()
                    guild_members = data["guild"]["members"]

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
                                           [*constants.GUILD_MEMBER_ROLES_IDS, constants.GUILD_MEMBER_ROLE_ID]]
                        await discord_member.remove_roles(*roles_to_remove,
                                                          atomic=False,
                                                          reason='check verified task')
                        uuids = uuids + (v_member['uuid'],)
        await cursor.execute(User.update_rows_with_ids([f"'{uuid}'" for uuid in uuids]))
        await cursor.close()
        await self.db.commit()

    @tasks.loop(hours=12)
    async def inactives_check(self):
        try:
            # Deletes all rows that are past their inactive time
            await self.db.execute(User.remove_inactives())
            await self.db.commit()

        except Exception as exception:
            await self.bot \
                .get_channel(constants.SBU_BOT_LOGS_CHANNEL_ID) \
                .send(exception_to_string('inactives_check task', exception))

    @tasks.loop(hours=168)
    async def weekly_tatsu(self):
        cursor: aiosqlite.Cursor = await self.db.cursor()
        await cursor.execute(User.select_top_tatsu())
        users = await cursor.fetchall()

        max_tatsu = {
            "tatsu": 0,
            "id": 0,
            "ign": None
        }

        for user in users:
            user = User.dict_from_tuple(user)
            weekly_tatsu = user['tatsu_score'] - user['weekly_tatsu_score']
            if weekly_tatsu > max_tatsu['tatsu']:
                max_tatsu['tatsu'] = weekly_tatsu
                max_tatsu['id'] = user['discord_id']
                max_tatsu['ign'] = user['ign']
            await self.db.execute(User.set_last_week_tatsu(user["ign"], user["tatsu_score"]))

        if max_tatsu["id"] != 0:
            guild = self.bot.get_guild(constants.GUILD_ID)
            role = guild.get_role(constants.TOP_GUILD_ACTIVE_ROLE_ID)
            for member in role.members:
                await member.remove_roles(role)
            member = guild.get_member(max_tatsu["id"])
            await member.add_roles(role)

    @weekly_tatsu.before_loop
    async def wait_until_next_week(self):
        next_week = datetime.datetime.now().replace(day=datetime.datetime.now().day +
                                                    (7 - datetime.datetime.weekday(datetime.datetime.now())))\
                                                        .timestamp()
        seconds_until_next_week = (next_week - (next_week % 86400) + 86400) - datetime.datetime.now().timestamp()
        await sleep(seconds_until_next_week)
    
    @tasks.loop(hours=24)
    async def booster_log(self):
        # Get the booster role
        sbu = self.bot.get_guild(constants.GUILD_ID)
        booster_role = sbu.get_role(constants.BOOSTER_ROLE_ID)

        # Put all boosters in a string
        booster_string = ""
        booster_list = []
        for member in booster_role.members:
            booster_string += f"{member.mention}\n"
            booster_list.append(member.mention)

        
        embed = discord.Embed(title="Booster Log", description=booster_string, color=constants.SBU_PURPLE)
        
        
        # Check if boosters changed
        log_channel = self.bot.get_channel(constants.BOOSTER_LOG_ID)
        message = self.bot.get_message(log_channel.last_message_id)
        try:
            if message.embeds[0] != None:
                previous_list = message.embeds[0].description.split("\n")
        except IndexError:
            previous_list = []
        x = False
        added_string = ""
        for user in booster_list:
            if user not in previous_list:
                added_string = f"{user}\n"
                x = True
        if x:
            embed.add_field(name="Added boosters:", value=added_string)
        
        y = False
        removed_string = ""
        for user in previous_list:
            if user not in booster_list:
                removed_string = f"{user}\n"
                y = True
        if y:
            embed.add_field(name="Removed boosters", value=removed_string)
        
        if not y and not x:
            return
        # Send a new log
        role = sbu.get_role(constants.JR_ADMIN_ROLE_ID)
        await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(TasksCog(bot))