from typing import Optional
from random import random
import requests
from discord.ext import commands

from utils.constants import WEIGHT_BANNED_ROLE_ID


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
