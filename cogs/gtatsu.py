import discord
from discord.ext import commands

from utils.schemas.GuildTatsuSchema import GuildTatsu
from utils.schemas.VerifiedMemberSchema import VerifiedMember
from utils.constants import BRIDGE_BOT_IDS, BRIDGE_CHANNEL_IDS, SBU_BOT_LOGS_CHANNEL_ID
from utils.error_utils import exception_to_string

import random

import aiosqlite
import requests

class GTatsu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        url = message.jump_url
        try:
            if message.author.id in BRIDGE_BOT_IDS and message.channel.id in BRIDGE_CHANNEL_IDS:
                embed = message.embeds[0]
                color = embed.color
                ign = embed.title
                value = embed.description

                if str(color) != "#6494ed":
                    return
                
                db = await aiosqlite.connect(VerifiedMember.DB_PATH + VerifiedMember.DB_NAME + '.db')
                cursor = await db.cursor()

                uuid = GTatsu.extract_id(ign)

                await cursor.execute(VerifiedMember.select_row_with_uuid(uuid))
                data = await cursor.fetchone()

                discord_id = VerifiedMember.dict_from_tuple(data)["discord_id"]


                await db.close()
                db = await aiosqlite.connect(GuildTatsu.DB_PATH + GuildTatsu.DB_NAME + '.db')
                cursor = await db.cursor()

                await cursor.execute(GuildTatsu.select_row_with_id(discord_id))
                data = await cursor.fetchone()

                data = GuildTatsu.dict_from_tuple(data)
                
                tatsu = random.randint(3, 7) + data["tatsu"]

                gtatsu = GuildTatsu(discord_id, tatsu)

                await cursor.execute(gtatsu.insert())
                await db.commit()

                await db.close()
            
        except Exception as exception:
            channel = self.bot.get_channel(SBU_BOT_LOGS_CHANNEL_ID)
            await channel.send(f"gtatsu brokie when {url} was sent\n{exception_to_string('/', exception)}")
            

    
    @staticmethod
    def extract_id(ign: str):
        # Fetch user info
        res = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}')

        if res.status_code != 200:  # Ensure that the request returned a user
            return None

        return res.json()['id']



def setup(bot):
    bot.add_cog(GTatsu(bot))