import datetime
import json
import os
import tarfile
from asyncio import sleep

import aiohttp
import aiosqlite
from discord.ext import commands, tasks

from utils import constants
from utils.error_utils import exception_to_string
from utils.schemas.VerifiedMemberSchema import VerifiedMember


class TasksCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.update_members.start()
        self.auto_qotd.start()
        self.backup_db.start()
        self.check_verified.start()

    def cog_unload(self):
        # self.update_members.cancel()
        self.auto_qotd.cancel()
        self.backup_db.cancel()
        self.check_verified.start()

    @tasks.loop(hours=1)
    async def update_members(self):
        total_members = 0  # Stores the member count of all the guilds combined
        for idx, guild in enumerate(constants.GUILDS_INFO.keys()):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.slothpixel.me/api/guilds/id/'
                                           f'{constants.GUILDS_INFO[guild]["guild_uuid"]}') as resp:
                        assert resp.status == 200  # Unless a guild gets deleted this will never raise

                        guild_info = await resp.json()

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
        channel = self.bot.get_channel(constants.QOTD_CHANNEL_ID)
        #

        with open(constants.QOTD_PATH) as f:
            qotd_obj = json.load(f)

        qotd_list = list(qotd_obj)

        if len(qotd_list) < 1:
            channel = self.bot.get_channel(constants.MOD_CHAT_CHANNEL_ID)
            await channel.send(
                f"<@&{constants.JR_MOD_ROLE_ID}> no QOTD's left in the archive. Automatic qotd canceled.\n"
                f"Please add more using `+qotdadd`.")
            return

        message = await channel.send(qotd_list[0]["qotd"] + f" <@&{constants.QOTD_ROLE_ID}>")
        await message.create_thread(name="QOTD")
        qotd_list.pop(0)
        with open(constants.QOTD_PATH, 'w') as json_file:
            json.dump(qotd_list, json_file,
                      indent=4,
                      separators=(',', ': '))
        num1 = len(qotd_list)
        if num1 < 3:
            channel = self.bot.get_channel(constants.MOD_CHAT_CHANNEL_ID)
            await channel.send(
                f"<@&{constants.JR_MOD_ROLE_ID}> QOTD's Running Low. Only {num1} remain.\n"
                f"Please add more using `+qotdadd`.")

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
        print("test")
        async with aiosqlite.connect(VerifiedMember.DB_PATH + VerifiedMember.DB_NAME + ".db") as db:
            cursor = await db.cursor()

            sbu = self.bot.get_guild(constants.GUILD_ID)
            uuids = ()

            for guild in constants.GUILDS_INFO:
                guild_uuid = constants.GUILDS_INFO[guild]["guild_uuid"]

                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.slothpixel.me/api/guilds/id/{guild_uuid}") as resp:
                        data = await resp.json()
                        members = data["members"]
                    
                await cursor.execute(VerifiedMember.select_row_with_guild_uuid(guild_uuid))
                guild_members = await cursor.fetchall()
                for member in guild_members:
                    member = VerifiedMember.dict_from_tuple(member)
                    if not any(d['uuid'] == member["uuid"] for d in members):
                        uuids = uuids + (uuid,)

                        user = sbu.get_member(member["discord_id"])
                        await user.remove_roles(*[discord.Object(_id) for _id in GUILD_MEMBER_ROLES_IDS], atomic=False)

                    
            await cursor.execute(VerifiedMember.update_rows(uuids))
            await db.commit()



def setup(bot):
    bot.add_cog(TasksCog(bot))
