from typing import Optional
from random import random
import requests


def extract_uuid(ign: str) -> Optional[str]:
    uuid = None

    res = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}')
    if res.status_code == 200:
        uuid = res.json()['id']
    return uuid


def weighted_randint(end, loops=1) -> int:
    result = 0
    for _ in range(loops):
        result += round(random() * (end/loops))

    return int(result)
