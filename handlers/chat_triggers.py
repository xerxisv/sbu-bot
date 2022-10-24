import discord
import json
from random import choice
from utils import Singleton
from typing import List, TypedDict
import aiofiles


class TriggerInfo(TypedDict):
    owner: List[int]
    reply: str | List[str]
    enabled: bool


class TriggersFileHandler(metaclass=Singleton):
    triggers_file_path = './data/triggers.json'

    def __init__(self):
        self._triggers = {}

    def get_triggers(self) -> dict:
        return self._triggers

    async def load_triggers(self) -> None:
        """
        Loads the contents of triggers.json to memory
        :return: None
        """

        async with aiofiles.open(TriggersFileHandler.triggers_file_path, mode='r') as f:
            self._triggers = json.loads(await f.read())

    async def save_triggers(self) -> None:
        """
        Writes the in-memory triggers to the triggers.json file
        :return: None
        """

        async with aiofiles.open(TriggersFileHandler.triggers_file_path, mode='w') as f:
            await f.write(json.dumps(self._triggers, indent=4))

    async def reload_triggers(self) -> None:
        """
        save_triggers() and load_triggers() shortcut
        :return: None
        """

        await self.save_triggers()
        await self.load_triggers()

    async def add_trigger(self, trigger_name: str, trigger_info: TriggerInfo) -> None:
        """
        Creates a new trigger

        :param trigger_name: The trigger's name
        :param trigger_info: The trigger's info
        :return: None
        :raise KeyError: If trigger already exists
        """

        trigger_name = trigger_name.upper()
        if trigger_name in self._triggers:
            raise KeyError('Key already exists')
        self._triggers[trigger_name] = trigger_info
        await self.reload_triggers()

    async def remove_trigger(self, key: str) -> bool:
        """
        Removed a trigger for the triggers file

        :param key: The trigger to remove
        :return: True if trigger found, False otherwise
        """

        removed = self._triggers.pop(key.upper(), None)
        await self.reload_triggers()
        return True if removed else False

    async def overwrite_trigger(self, trigger_name: str, trigger_info: TriggerInfo) -> None:
        """
        Overwrites an existing trigger

        :param trigger_name: The trigger's name
        :param trigger_info: The trigger's info
        :return: None
        :raise KeyError: If trigger does not exist
        """

        self._triggers[trigger_name.upper()] = trigger_info
        await self.reload_triggers()

    async def toggle_trigger(self, trigger_name: str) -> bool:
        """
        Toggles a trigger

        :param trigger_name: The trigger's name
        :return: The new state of the trigger
        :raise KeyError: If the trigger does not exist
        """

        trigger_name = trigger_name.upper()

        if trigger_name not in self._triggers:
            raise KeyError(f'Trigger {trigger_name} not found')

        self._triggers[trigger_name]['enabled'] = not self._triggers[trigger_name]['enabled']
        await self.reload_triggers()

        return self._triggers[trigger_name]['enabled']

    async def handle_trigger(self, msg: discord.Message) -> None:
        content = msg.content.upper()

        trigger: TriggerInfo = self._triggers[content]
        if msg.author.id not in trigger['owner'] or not trigger['enabled']:
            return

        reply = trigger['reply'] if type(trigger['reply']) is str else choice(trigger['reply'])
        await msg.reply(reply)

    def is_trigger(self, msg: str) -> bool:
        return msg.upper() in self._triggers.keys()
