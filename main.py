import asyncio
import os

import discord
import discord.utils
from discord.ext import commands
from dotenv import load_dotenv

from handlers import chat_triggers, gtatsu, warns
from utils.constants import ADMIN_CHAT_CHANNEL_ID, BOT_OWNER_ROLE_ID, CARRY_SERVICE_REPS_CHANNEL_ID, \
    CRAFT_REPS_CHANNEL_ID, JR_MOD_ROLE_ID, SBU_BOT_LOGS_CHANNEL_ID, SBU_GOLD
from utils.database import DBConnection
from utils.error_utils import exception_to_string, log_error
from utils.setup import run_setup

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="+", intents=intents, case_insensitive=True)
bot.remove_command('help')

trigger_handler = chat_triggers.TriggersFileHandler()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready")

    await DBConnection().create_db()
    gtatsu.set_up_db()
    await trigger_handler.load_triggers()

    channel = bot.get_channel(ADMIN_CHAT_CHANNEL_ID)
    await channel.send(f"The Bot has been recently rebooted.\n"
                       "Please enable all the necessary cogs <a:wiggles:917695379485634580>.")

@bot.command()
@commands.has_role(BOT_OWNER_ROLE_ID)
async def load_all(ctx: commands.Context):
    for filename in os.listdir('./cogs'):
        if not filename.endswith('.py'):
            continue

        bot.load_extension(f'cogs.{filename[:-3]}')

    await ctx.reply('Cogs loaded successfully')


@bot.command()
@commands.has_role(BOT_OWNER_ROLE_ID)
async def load(ctx: commands.Context, extension):
    if extension == 'all':
        await bot.get_command('load_all').invoke(ctx)
        return
    try:
        bot.load_extension(f'cogs.{extension}')
    except discord.ExtensionAlreadyLoaded:
        await ctx.reply(f'Cog {extension} already loaded')
    except discord.ExtensionNotFound:
        await ctx.reply(f'Cog {extension} does not exist')
    else:
        await ctx.reply(f'Cog {extension} loaded successfully')


@bot.command()
@commands.has_role(BOT_OWNER_ROLE_ID)
async def unload(ctx: commands.Context, extension):
    try:
        bot.unload_extension(f'cogs.{extension}')
    except discord.ExtensionNotLoaded:
        await ctx.reply(f'Cog {extension} has not been loaded')
    except discord.ExtensionNotFound:
        await ctx.reply(f'Cog {extension} does not exist')
    else:
        await ctx.reply(f'Cog {extension} unloaded successfully')


@bot.command()
@commands.has_role(BOT_OWNER_ROLE_ID)
async def reload(ctx: commands.Context):
    for filename1 in os.listdir('./cogs'):
        if not filename1.endswith('.py'):
            continue

        try:
            bot.unload_extension(f'cogs.{filename1[:-3]}')
        except discord.ExtensionNotLoaded:
            print(f'Cog {filename1[:-3]} has not been loaded')

    for filename1 in os.listdir('./cogs'):
        if not filename1.endswith('.py'):
            continue

        bot.load_extension(f'cogs.{filename1[:-3]}')

    await ctx.reply('Cogs reloaded successfully')


@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')


@bot.command(name='help', aliases=['commands'])
async def help(ctx: commands.Context):
    embed = discord.Embed(
        title='Help',
        description='All the help commands are listed below.\n'
                    'Options inside "<>" are required while options inside "[]" are optional.',
        colour=SBU_GOLD
    )
    embed.add_field(name="Ping the bot.", value="`+ping`", inline=False)
    embed.add_field(name="Link your discord and hypixel accounts.", value="`+verify <IGN>`", inline=False)
    embed.add_field(name="UnLink your discord and hypixel accounts.", value="`+unverify`", inline=False)
    embed.add_field(name="Lists hypixel stats.", value="`+hypixel <IGN>`", inline=False)
    embed.add_field(name="Check if you meet reqs for SB Masters.", value="`+checkreq <IGN>`", inline=False)
    embed.add_field(name="Suggest something.", value="`+suggest <suggestion>`", inline=False)
    embed.add_field(name="Give reputation to a user.",
                    value='`+rep give <@mention> <comments>`\n'
                          f'*It can only be used in <#{CRAFT_REPS_CHANNEL_ID}> or '
                          f'<#{CARRY_SERVICE_REPS_CHANNEL_ID}>*', inline=False)
    embed.add_field(name="Add yourself to the inactivity list.", value="`+inactive add <time>`\n"
                                                                       "*Time is in days, __min 7__, __max 30__\n"
                                                                       "**Ex**: `+inactive add 25d`*", inline=False)
    embed.set_footer(text='Skyblock University Bot')
    await ctx.reply(embed=embed)


@bot.command()
@commands.has_role(JR_MOD_ROLE_ID)
async def modhelp(ctx: commands.Context):
    embed = discord.Embed(
        title='Moderation Commands',
        description='All the moderation commands are listed below.\n'
                    'Options inside "<>" are required while options inside "[]" are optional.',
        colour=SBU_GOLD
    )
    embed.set_footer(text='Skyblock University Bot')
    embed.add_field(name="Ban", value="`+ban <@mention | ID> [reason]`", inline=False)
    embed.add_field(name="Mute", value="`+mute <@mention | ID> <time> [reason]`\n"
                                       "*Max mute duration is 28 days.\n"
                                       "Mods **can** mute each other but **should not** unless "
                                       "specifically asked to*", inline=False)
    embed.add_field(name="Unmute", value="`+unmute <@mention | ID> [reason]`", inline=False)
    embed.add_field(name="Reputation specific commands", value="`+rep help`", inline=False)
    embed.add_field(name="Banlist specific commands", value="`+banlist help`", inline=False)
    embed.add_field(name="Inactives specific commands", value="`+inactive help`", inline=False)
    embed.add_field(name="Suggestions specific commands", value="`+suggestions help`", inline=False)
    embed.add_field(name="Activate crisis mode", value="`+crisis`", inline=False)
    embed.add_field(name="Deactivate crisis mode", value="`+crisisend`", inline=False)
    embed.add_field(name="Add a question to the QOTD list", value="`+qotdadd <question>`", inline=False)
    embed.add_field(name="List all questions", value="`+qotdlist`", inline=False)
    await ctx.reply(embed=embed)


@bot.command()
@commands.has_role(BOT_OWNER_ROLE_ID)
async def dm(ctx: commands.Context, user: discord.User, *, message: str):
    try:
        await user.send(message)
    except Exception as err:
        await ctx.reply('User could not be DMed')
        print(err)
    else:
        await ctx.reply("User DMed")


@bot.event
async def on_command_error(ctx: commands.Context, exception):
    if isinstance(exception, commands.CommandOnCooldown):
        embed = discord.Embed(
            title='Error',
            description='Command is on cooldown',
            colour=0xFF0000
        )
        await ctx.reply(embed=embed)

    elif isinstance(exception, commands.MissingRole):
        embed = discord.Embed(
            title='Error',
            description=f'Insufficient permissions, only members '
                        f'with **{ctx.guild.get_role(exception.missing_role).name}** role can run this command',
            colour=0xFF0000
        )
        await ctx.reply(embed=embed)

    elif isinstance(exception, discord.Forbidden):
        embed = discord.Embed(
            title='Error',
            description='Bot does not have permissions to do this.',
            colour=0xFF0000
        )
        await ctx.reply(embed=embed)
    elif isinstance(exception, (commands.CommandNotFound, commands.MissingRequiredArgument, commands.BadArgument)):
        pass
    else:
        try:
            await log_error(ctx, exception)
        except AttributeError:
            await bot.get_channel(SBU_BOT_LOGS_CHANNEL_ID).send('Exception passed to main:\n' +
                                                                exception_to_string("main", exception))
            return


@bot.event
async def on_message(message: discord.Message):
    # Prevents the bot from going through all the if statements unnecessarily
    if warns.is_warn(message.content):
        await warns.handle_warn(message)
    elif trigger_handler.is_trigger(message.content):
        await trigger_handler.handle_trigger(message)
    elif gtatsu.is_bridge_message(message):
        await gtatsu.handle_gtatsu(message)
    else:
        await bot.process_commands(message)


if __name__ == '__main__':
    run_setup()
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
    asyncio.run(DBConnection().close_db())
