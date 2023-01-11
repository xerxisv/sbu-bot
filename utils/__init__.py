from typing import Optional
from random import random
import requests
from discord.ext import commands

from utils.constants import WEIGHT_BANNED_ROLE_ID, INFO_EMBED_DESCRIPTION, INFO_CHANNEL_ID, SBU_GOLD, BUTTON_STRINGS
from utils.components import info_button

import discord
from discord.ui import View


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def extract_uuid(ign: str) -> Optional[str]:
    uuid = None

    res = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}')
    if res.status_code == 200:
        uuid = res.json()['id']
    return uuid


def weighted_randint(end, loops=1) -> int:
    result = 0
    for _ in range(loops):
        result += round(random() * (end / loops))

    return int(result)


def check_if_weight_banned(ctx: commands.Context) -> bool:
    if ctx.author.get_role(WEIGHT_BANNED_ROLE_ID):
        return False

    return True

async def info_reload(bot):
    channel = await bot.fetch_channel(INFO_CHANNEL_ID)
    if channel.last_message_id is not None:
        message = await channel.fetch_message(channel.last_message_id)
    else:
        message = None
    

    embed = discord.Embed(title="Info", description=INFO_EMBED_DESCRIPTION, color=SBU_GOLD)
    
    view = View()
    i = 0
    j = 0
    for button in BUTTON_STRINGS:
        i += 1
        label = button
        description = BUTTON_STRINGS[button]["description"]
        button_view = BUTTON_STRINGS[button]["view"]
        image = BUTTON_STRINGS[button]["image"]

        view.add_item(info_button(bot, label, description, button_view, image, row=j))
        if i == 5:
            i = 0
            j += 1
    
    try:
        if message is not None:
            await message.edit(embed=embed, view=view)
        else: 
            await channel.send(embed=embed, view=view)
    except discord.Forbidden:
        await channel.send(embed=embed, view=view)