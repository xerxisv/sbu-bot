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

from utils.config.config import ConfigHandler
from utils.database import DBConnection
from utils.database.schemas import User
from utils.error_utils import exception_to_string

config = ConfigHandler().get_config()


class TasksCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        dotenv.load_dotenv()
        self.bot = bot
        self.db: aiosqlite.Connection = DBConnection().get_db()
        self.key = os.getenv('APIKEY')
        self.update_member_count.start()
        self.backup_db.start()
        self.booster_log.start()

        if config['modules']['qotd']:
            self.auto_qotd.start()
        if config['modules']['inactives']:
            self.inactives_check.start()
        if config['modules']['verify']:
            self.check_verified.start()
        if config['modules']['gtatsu']:
            self.weekly_tatsu.start()

    def cog_unload(self):
        self.update_member_count.cancel()
        self.auto_qotd.cancel()
        self.backup_db.cancel()
        self.inactives_check.cancel()
        self.check_verified.cancel()
        self.weekly_tatsu.cancel()
        self.booster_log.cancel()

    @tasks.loop(hours=1)
    async def update_member_count(self):
        total_members = 0  # Stores the member count of all the guilds combined
        for idx, guild in enumerate(config['guilds'].keys()):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.hypixel.net/guild?key={self.key}&id="
                                           f"{config['guilds'][guild]['guild_uuid']}") as resp:
                        assert resp.status == 200  # Unless a guild gets deleted this will never raise

                        guild_info = (await resp.json())["guild"]

            except AssertionError:
                await self.bot \
                    .get_channel(config['bot_log_channel_id']) \
                    .send(f"Guild info fetch with id `{config['guilds'][guild]['guild_uuid']}` "
                          "did not return a 200.")

            except Exception as exception:
                await self.bot \
                    .get_channel(config['bot_log_channel_id']) \
                    .send(exception_to_string('update_member task', exception))

            else:
                new_name = f'{guild_info["name"]}: {str(len(guild_info["members"]))}'
                total_members += int(len(guild_info["members"]))

                vc = self.bot.get_channel(config['guilds'][guild]['member_count_channel_id'])

                if vc is None:
                    await self.bot \
                        .get_channel(config['bot_log_channel_id']) \
                        .send(f"Could not fetch channel with id {config['guilds'][guild]['member_count_channel_id']}")

                    return

                await vc.edit(name=new_name)

        total_member_vc = self.bot.get_channel(config['tasks']['total_members_channel_id'])
        new_name = "Guild members: " + str(total_members)

        if total_member_vc is None:
            await self.bot \
                .get_channel(config['bot_log_channel_id']) \
                .send(f"Could not fetch channel with id {config['tasks']['total_members_channel_id']}")

            return

        await total_member_vc.edit(name=new_name)

    @tasks.loop(hours=24)
    async def auto_qotd(self):
        qotd_channel = self.bot.get_channel(config['qotd']['qotd_channel_id'])
        mod_chat = self.bot.get_channel(config['mod_chat_channel_id'])

        with open('./data/qotd.json') as f:
            qotd_obj = json.load(f)

        qotd_list = list(qotd_obj)
        if len(qotd_list) < 1:
            await mod_chat.send(
                f"<@&{config['jr_mod_role_id']}> no QOTD's left in the archive. Automatic qotd canceled.\n"
                f"Please add more using `+qotd add`.")
            return

        try:
            message = await qotd_channel.fetch_message(qotd_channel.last_message_id)
            await message.thread.edit(locked=True, archived=True)
        except AttributeError:
            pass

        message = await qotd_channel.send(qotd_list[0]["qotd"] + f" <@&{config['qotd']['qotd_role_id']}>")
        await message.create_thread(name="QOTD")

        qotd_list.pop(0)

        with open('./data/qotd.json', 'w') as json_file:
            json.dump(qotd_list, json_file,
                      indent=4,
                      separators=(',', ': '))

        num1 = len(qotd_list)

        if num1 < 3:
            await mod_chat.send(
                f"<@&{config['jr_mod_role_id']}> QOTD's Running Low. Only {num1} remain.\n"
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
                    if file.endswith((".db", ".json")):
                        tar_handle.add(os.path.join(root, file), arcname=file)

    @tasks.loop(hours=24)
    async def check_verified(self):
        cursor: aiosqlite.Cursor = await self.db.cursor()

        sbu = self.bot.get_guild(config['server_id'])
        uuids: tuple = ()

        # loop for each guild
        for guild in config['guilds']:
            guild_uuid = config['guilds'][guild]["guild_uuid"]

            try:
                # fetch guild members
                async with aiohttp.ClientSession() as session:
                    res = await session.get(f"https://api.hypixel.net/guild?id={guild_uuid}&key={self.key}")

                    assert res.status == 200

                    data = await res.json()
                    guild_members = data["guild"]["members"]

            except AssertionError:
                await self.bot \
                    .get_channel(config['bot_log_channel_id']) \
                    .send(f"Guild info fetch with id `{config['guilds'][guild]['guild_uuid']}` "
                          "did not return a 200.")
                continue

            except Exception as exception:
                await self.bot \
                    .get_channel(config['bot_log_channel_id']) \
                    .send(exception_to_string('update_member task', exception))
                continue

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
                                           [*config['verify']['guild_member_roles'],
                                            config['verify']['member_role_id']]]
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
                .get_channel(config['bot_log_channel_id']) \
                .send(exception_to_string('inactives_check task', exception))

    @tasks.loop(hours=168)
    async def weekly_tatsu(self):
        cursor: aiosqlite.Cursor = await self.db.cursor()
        await cursor.execute(User.select_top_tatsu())
        user = User.dict_from_tuple((await cursor.fetchone())[0])
        users = await cursor.fetchall()

        guild = self.bot.get_guild(config["server_id"])
        role = guild.get_role(config["gtatsu"]["top_active_role_id"])
        for member in role.members:
            await member.remove_roles(role)

        max_tatsu = user

        for user in users:
            user = User.dict_from_tuple(user)
            weekly_tatsu = user['tatsu_score'] - user['weekly_tatsu_score']
            if weekly_tatsu > max_tatsu['tatsu_score']:
                max_tatsu['tatsu_score'] = weekly_tatsu
                max_tatsu['discord_id'] = user['discord_id']
                max_tatsu['ign'] = user['ign']
            await self.db.execute(User.set_last_week_tatsu(user["ign"], user["tatsu_score"]))

        if max_tatsu["discord_id"] != 0:
            guild = self.bot.get_guild(config['server_id'])
            role = guild.get_role(config['gtatsu']['top_active_role_id'])
            for member in role.members:
                await member.remove_roles(role)
            member = guild.get_member(max_tatsu["discord_id"])
            await member.add_roles(role)
        
        await self.db.execute(User.set_last_week_tatsu_all())
        await self.db.commit()

    @weekly_tatsu.before_loop
    async def wait_until_next_week(self):
        next_week = datetime.datetime.now() \
            .replace(day=datetime.datetime.now().day + (7 - datetime.datetime.weekday(datetime.datetime.now()))) \
            .timestamp()
        seconds_until_next_week = (next_week - (next_week % 86400) + 86400) - datetime.datetime.now().timestamp()
        await sleep(seconds_until_next_week)

    @tasks.loop(hours=24)
    async def booster_log(self):
        # Get the booster role
        sbu = self.bot.get_guild(config['server_id'])
        booster_role = sbu.get_role(config['tasks']['booster_role_id'])

        # Put all boosters in a string
        booster_string = ""
        booster_list = []
        for member in booster_role.members:
            booster_string += f"{member.mention}\n"
            booster_list.append(member.mention)

        embed = discord.Embed(
            title="Booster Log",
            description=booster_string,
            color=config['colors']['secondary'])

        # Check if boosters changed
        log_channel = self.bot.get_channel(config['tasks']['booster_log_channel_id'])
        message = self.bot.get_message(log_channel.last_message_id)
        previous_list = []

        try:
            if message is not None and message.embeds[0] is not None:
                previous_list = message.embeds[0].description.split("\n")
        except IndexError:
            previous_list = []

        new_booster_added = False
        added_string = ""
        for user in booster_list:
            if user not in previous_list:
                added_string += f"{user}\n"
                new_booster_added = True
        if new_booster_added:
            embed.add_field(name="Added boosters:", value=added_string)

        was_booster_removed = False
        removed_string = ""
        for user in previous_list:
            if user not in booster_list:
                removed_string += f"{user}\n"
                was_booster_removed = True
        if was_booster_removed:
            embed.add_field(name="Removed boosters", value=removed_string)

        if not was_booster_removed and not new_booster_added:
            return
        # Send a new log
        await log_channel.send(embed=embed)

    @booster_log.before_loop
    async def wait_until_next(self):
        next_midnight = datetime.datetime.now().timestamp() - (datetime.datetime.now().timestamp() % 86400) + 86400
        seconds_until_next = next_midnight - datetime.datetime.now().timestamp()
        await sleep(seconds_until_next)

def setup(bot):
    bot.add_cog(TasksCog(bot))
