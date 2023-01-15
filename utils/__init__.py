import requests


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
