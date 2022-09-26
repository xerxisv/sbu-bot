from discord.ext.commands import Context
import traceback

from utils.constants import SBU_BOT_LOGS_CHANNEL_ID

ERROR_MESSAGE = '**Exception raised during the execution of {}**.\n```{}```*URL: <{}>*'


def exception_to_string(command: str, exception: Exception, jump_url: str = None):
    stack = traceback.extract_stack(limit=1)[:-3] + traceback.extract_tb(exception.__traceback__, limit=1)
    pretty = traceback.format_list(stack)
    return ERROR_MESSAGE.format(command, ''.join(pretty) + '\n  {} {}'.format(exception.__class__, exception), jump_url)


async def log_error(ctx: Context, exception: Exception):
    await ctx.guild\
        .get_channel(SBU_BOT_LOGS_CHANNEL_ID)\
        .send(exception_to_string(ctx.command.name, exception, ctx.message.jump_url))
