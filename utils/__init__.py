from typing import Optional
import requests


def extract_uuid(ign: str) -> Optional[str]:
    uuid = None

    res = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}')
    if res.status_code == 200:
        uuid = res.json()['id']
    return uuid
