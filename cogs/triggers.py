import json
from math import ceil
from random import choice
from typing import List, TypedDict

import aiofiles
import discord
from discord.ext import commands

from utils import Singleton
from utils.config.config import ConfigHandler

config = ConfigHandler().get_config()


class Triggers(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.trigger_handler = TriggersFileHandler()
        self.trigger_handler.load_triggers()

    @commands.group(name='trigger', aliases=['ct', 'triggers'])
    @commands.cooldown(1, 5)
    @commands.has_role(config['jr_admin_role_id'])
    async def trigger(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('trigger help').invoke(ctx)
            return
        await ctx.trigger_typing()

    @trigger.command(name='help')
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title='Command Help',
            color=config['colors']['primary']
        )

        embed.add_field(name='Create a new trigger.',
                        value='`+trigger create <trigger> | <owner_id> | <response>`\n'
                              '*For multiple owners put the IDs inside brackets, separated by semicolons.*\n'
                              '*For random responses put the responses inside brackets, separated by semicolons.*\n'
                              'E.g., \n'
                              '*`+trigger add hehe | [123; 456] | [xd; hehe]`*',
                        inline=False)
        embed.add_field(name='Remove a trigger',
                        value='`+trigger remove <trigger>`',
                        inline=False)
        embed.add_field(name='Replace a trigger',
                        value='`+trigger replace <trigger> | <owner_id> | <response>`\n'
                              '*Same format as create*\n'
                              '*Replaced triggers cannot be restored. Use with caution*')
        embed.add_field(name='Enable or disable a trigger',
                        value='`+trigger toggle <trigger>`',
                        inline=False)
        embed.add_field(name='Lists triggers',
                        value='`+trigger list [page]`',
                        inline=False)
        embed.add_field(name='Command aliases list',
                        value='`+trigger alias`',
                        inline=False)

        await ctx.reply(embed=embed)

    @trigger.command(name='aliases', aliases=['alias'])
    async def aliases(self, ctx: commands.Context):
        embed = discord.Embed(
            title='Command aliases',
            color=config['colors']['primary']
        )

        embed.add_field(name='trigger', value='"triggers", "ct"')
        embed.add_field(name='create', value='"add"')
        embed.add_field(name='remove', value='"rm", "delete", "del"')
        embed.add_field(name='replace', value='"rp", "overwrite", "override"')
        embed.add_field(name='dump', value='None')

        await ctx.reply(embed=embed)

    @trigger.command(name='create', aliases=['add'])
    async def create(self, ctx: commands.Context, *, args: str):
        trigger, trigger_info = extract_trigger_info(args)

        try:
            await self.trigger_handler.add_trigger(trigger, trigger_info)

        except KeyError:
            embed = discord.Embed(
                title='Error',
                description=f'Trigger `{trigger}` already exists. Use `+trigger replace`.',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(
                title='Success',
                description='Chat trigger added successfully',
                color=config['colors']['success']
            )
            await ctx.reply(embed=embed)

    @create.error
    async def create_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.BadArgument):
            embed = discord.Embed(
                title='Error',
                description=f'Invalid owners. Use discord IDs',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return
        elif isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+trigger replace <trigger> | <owner_id> | <response>`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

    @trigger.command(name='remove', aliases=['rm', 'delete', 'del'])
    async def remove(self, ctx: commands.Context, *, trigger_name: str):
        removed = await self.trigger_handler.remove_trigger(trigger_name)
        if removed:
            embed = discord.Embed(
                title='Success',
                description=f'Removed trigger `{trigger_name}`.',
                color=config['colors']['success']
            )
        else:
            embed = discord.Embed(
                title='Error',
                description=f'Trigger `{trigger_name}` not found.',
                color=config['colors']['success']
            )

        await ctx.reply(embed=embed)

    @remove.error
    async def remove_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+trigger remove <trigger>`',
                color=config['colors']['success']
            )
            await ctx.reply(embed=embed)
            return

    @trigger.command(name='replace', aliases=['overwrite', 'override', 'rp'])
    async def replace(self, ctx: commands.Context, *, trigger_name: str):
        trigger_name, trigger_info = extract_trigger_info(trigger_name)

        try:
            await self.trigger_handler.overwrite_trigger(trigger_name, trigger_info)

        except KeyError:
            embed = discord.Embed(
                title='Error',
                description=f'Trigger `{trigger_name}` does not exist. Use `+trigger create`.',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(
                title='Success',
                description='Chat trigger replaced successfully',
                color=config['colors']['success']
            )
            await ctx.reply(embed=embed)

    @replace.error
    async def replace_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.BadArgument):
            embed = discord.Embed(
                title='Error',
                description=f'Invalid owners. Use discord IDs',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return
        elif isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+trigger replace <trigger> | <owner_id> | <response>`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

    @trigger.command(name='toggle')
    async def toggle(self, ctx: commands.Context, *, trigger_name: str):
        try:
            is_enabled = await self.trigger_handler.toggle_trigger(trigger_name)
        except KeyError:
            embed = discord.Embed(
                title='Error',
                description=f'Trigger `{trigger_name}` not found.',
                color=config['colors']['error']
            )
        else:
            embed = discord.Embed(
                title='Success',
                description=f'Trigger is now {"enabled" if is_enabled else "disabled"}.',
                color=config['colors']['success']
            )

        await ctx.reply(embed=embed)

    @toggle.error
    async def toggle_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+trigger toggle <trigger>`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

    @trigger.command(name='show', aliases=['list', 'print'])
    async def show(self, ctx: commands.Context, page: int = 1):
        triggers = self.trigger_handler.get_triggers()

        triggers_length = len(triggers.keys())
        max_page = ceil(triggers_length / 10)

        if page > max_page or page < 1:
            embed = discord.Embed(
                title='Error',
                description=f'There is no page {page}. Valid pages are between 1 and {max_page}',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        start = (page - 1) * 10
        end = 10 * page

        embed = discord.Embed(
            title='Chat Triggers List',
            color=config['colors']['primary']
        )

        for index, trigger in enumerate(triggers.keys()):
            if index < start or index >= end:
                continue

            owners = ' | '.join([f'<@{owner}>' for owner in triggers[trigger]['owner']])
            embed.add_field(
                name=f'{trigger}',
                value=f'Owners: *{owners}*\nEnabled: *{triggers[trigger]["enabled"]}*',
                inline=False
            )
        embed.set_footer(text=f'Page: {page}/{max_page}')
        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.trigger_handler.is_trigger(message.content):
            await self.trigger_handler.handle_trigger(message)


class TriggerInfo(TypedDict):
    owner: List[int]
    reply: str | List[str]
    enabled: bool


def extract_trigger_info(args: str) -> (str, TriggerInfo):
    """
    Extracts the trigger's info from the command

    :param args: String from command containing all the trigger information
    :return: Tuple with trigger name and info
    :raise commands.BadArgument: If provided IDs are not numbers
    :raise commands.MissingRequiredArgument: When the input is missing one of the arguments
    """
    args = args.split('|')

    if len(args) < 3:
        raise commands.MissingRequiredArgument

    trigger = args[0].strip().upper()
    owners = args[1].strip()
    response = args[2].strip()

    if owners.startswith('[') and owners.endswith(']'):
        owners = list(owners.removeprefix('[').removesuffix(']').split(';'))
    else:
        owners = list([owners, ])

    if response.startswith('[') and response.endswith(']'):
        response = response.removeprefix('[').removesuffix(']').split(';')
        response = [res.strip() for res in response]
    else:
        response = response.strip()

    for index, owner in enumerate(owners):
        owner = owner.strip()
        if owner.isnumeric():
            owners[index] = int(owner)
            continue

        raise commands.BadArgument

    return trigger, {"owner": owners, "reply": response, "enabled": True}


class TriggersFileHandler(metaclass=Singleton):
    triggers_file_path = './data/triggers.json'

    def __init__(self):
        self._triggers = {}

    def get_triggers(self) -> dict:
        return self._triggers

    def load_triggers(self) -> None:
        """
        Loads the contents of triggers.json to memory
        :return: None
        """

        with open(TriggersFileHandler.triggers_file_path, mode='r') as f:
            self._triggers = json.loads(f.read())

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
        self.load_triggers()

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


def setup(bot):
    bot.add_cog(Triggers(bot))
