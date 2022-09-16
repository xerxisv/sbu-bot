import json

import aiohttp
from discord.ext import commands, tasks

from utils import constants
from utils.error_utils import exception_to_string


class TasksCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_member.start()
        self.auto_qotd.start()

    def cog_unload(self):
        self.update_member.cancel()
        self.auto_qotd.cancel()

    @tasks.loop(hours=1)
    async def update_member(self):
        # noinspection SpellCheckingInspection
        guilds = ["6111fcb48ea8c95240436c57", "604a765e8ea8c962f2bb3b7a",
                  "607a0d7c8ea8c9c0ff983976", "608d91e98ea8c9925cdb91b7",
                  "60a16b088ea8c9bb7f6d9052", "60b923478ea8c9a3aefbf3dd",
                  "6125800e8ea8c92e1833e851", "570940fb0cf2d37483e106b3"]

        total_members = 0  # Stores the member count of all the guilds combined
        for idx, guild in enumerate(guilds):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.slothpixel.me/api/guilds/id/{guild}') as resp:
                        assert resp.status == 200  # Unless a guild gets deleted this will never raise

                        guild_info = await resp.json()

                new_name = f'{guild_info["name"]}: {str(len(guild_info["members"]))}'
                total_members += int(len(guild_info["members"]))

                vc = self.bot.get_channel(constants.MEMBER_COUNT_VC_IDS[idx])

                await vc.edit(name=new_name)
            except AssertionError:
                await self.bot \
                    .get_channel(constants.SBU_BOT_LOGS_CHANNEL_ID) \
                    .send(f'Guild info fetch with id `{guild}` did not return a 200.')

            except Exception as exception:
                await self.bot \
                    .get_channel(constants.SBU_BOT_LOGS_CHANNEL_ID) \
                    .send(exception_to_string('update_member task', exception))

        total_member_vc = self.bot.get_channel(constants.TOTAL_MEMBER_COUNT_VC_ID)
        new_name = "Guild members: " + str(total_members)
        await total_member_vc.edit(name=new_name)

        channel = self.bot.get_channel(constants.SBU_BOT_LOGS_CHANNEL_ID)
        await channel.send(f"Guild Stats VC Updated")

    @tasks.loop(hours=24)
    async def auto_qotd(self):
        channel = self.bot.get_channel(constants.QOTD_CHANNEL_ID)
        #

        with open('qotd.json') as f:
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
        with open('qotd.json', 'w') as json_file:
            json.dump(qotd_list, json_file,
                      indent=4,
                      separators=(',', ': '))
        num1 = len(qotd_list)
        if num1 < 3:
            channel = self.bot.get_channel(constants.MOD_CHAT_CHANNEL_ID)
            await channel.send(
                f"<@&{constants.JR_MOD_ROLE_ID}> QOTD's Running Low. Only {num1} remain.\n"
                f"Please add more using `+qotdadd`.")


def setup(bot):
    bot.add_cog(TasksCog(bot))
