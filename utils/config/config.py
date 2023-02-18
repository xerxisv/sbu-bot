import aiofiles
import json

from utils import Singleton
from .types.config_dict_type import Config


class ConfigHandler(metaclass=Singleton):
    config_file_path = './config.json'

    def __init__(self):
        self.__config: Config = {}

    def get_config(self) -> Config:
        return self.__config

    def load_config(self) -> None:
        with open(self.config_file_path, mode='r') as f:
            self.__config = json.loads(f.read())
