import requests
from utils.components import info_button

import discord
from discord.ui import View


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def extract_uuid(ign: str) -> str | None:
    uuid = None

    res = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}')
    if res.status_code == 200:
        uuid = res.json()['id']
    return uuid
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
