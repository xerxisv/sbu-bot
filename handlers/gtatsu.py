import time

import discord

from utils import weighted_randint
from utils.constants import BRIDGE_BOT_IDS, BRIDGE_CHANNEL_IDS
from utils.database import DBConnection
from utils.database.schemas import User

TATSU_CD = 20  # in seconds
tatsu_dates = {}

global db
is_db_ready = False


async def handle_gtatsu(message: discord.Message):
    ign = message.embeds[0].author.name

    if not isinstance(ign, str):
        return

    if ign.find(' ') > 0:
        return
    if ensure_cooldown(ign):
        return

    await db.execute(User.add_to_tatsu(ign, weighted_randint(12, 3)))
    await db.commit()
    tatsu_dates[ign] = int(time.time())


def is_bridge_message(message: discord.Message):
    return message.author.id in BRIDGE_BOT_IDS and message.channel.id in BRIDGE_CHANNEL_IDS and len(message.embeds) > 0


def ensure_cooldown(ign: str) -> bool:
    return False if ign not in tatsu_dates else tatsu_dates[ign] + TATSU_CD > int(time.time())


def set_up_db():
    global db
    db = DBConnection().get_db()
    global is_db_ready
    is_db_ready = False
