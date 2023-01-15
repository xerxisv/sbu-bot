import asyncio
import os

import discord
import discord.utils
from discord.ext import commands
from dotenv import load_dotenv

from utils.config.config import ConfigHandler
from utils.database import DBConnection
from utils.error_utils import exception_to_string, log_error
from utils.setup import run_setup

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="+", intents=intents, case_insensitive=True)
bot.remove_command('help')

ConfigHandler().load_config()
config = ConfigHandler().get_config()


def load_cogs():
    for filename in os.listdir('./cogs'):
        if not filename.endswith('.py'):
            continue

        name = filename[:-3]

        if config['modules'][name] is not True:
            continue

        print(f'\033[1mLoading \033[36;4m{name}\033[0;1m extension...\033[0m')
        bot.load_extension(f'cogs.{name}')


@bot.event
async def on_ready():
    await DBConnection().create_db()

    load_cogs()
    print(f"\033[1;4;34m{bot.user} is ready\033[0m")


@bot.command()
@commands.has_role(config['admin_role_id'])
async def load_all(ctx: commands.Context):
    for filename in os.listdir('./cogs'):
        if not filename.endswith('.py'):
            continue

        bot.load_extension(f'cogs.{filename[:-3]}')

    await ctx.reply('Cogs loaded successfully')


@bot.command()
@commands.has_role(config['admin_role_id'])
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
@commands.has_role(config['admin_role_id'])
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
@commands.has_role(config['admin_role_id'])
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
        color=config['colors']['primary']
    )
    embed.add_field(name="Ping the bot.", value="`+ping`", inline=False)
    embed.add_field(name="Link your discord and hypixel accounts.", value="`+verify <IGN>`", inline=False)
    embed.add_field(name="UnLink your discord and hypixel accounts.", value="`+unverify`", inline=False)
    embed.add_field(name="Lists hypixel stats.", value="`+hypixel <IGN>`", inline=False)
    embed.add_field(name="Check if you meet reqs for SB Masters.", value="`+checkreq <IGN>`", inline=False)
    embed.add_field(name="Suggest something.", value="`+suggest <suggestion>`", inline=False)
    embed.add_field(name="Give reputation to a user.", value='`+rep give <@mention> <comments>`\n', inline=False)
    embed.add_field(name="Add yourself to the inactivity list.", value="`+inactive add <time>`\n"
                                                                       "*Time is in days, __min 7__, __max 30__\n"
                                                                       "**Ex**: `+inactive add 25d`*", inline=False)
    embed.set_footer(text='Skyblock University Bot')
    await ctx.reply(embed=embed)


@bot.command()
@commands.has_role(config['jr_mod_role_id'])
async def modhelp(ctx: commands.Context):
    embed = discord.Embed(
        title='Moderation Commands',
        description='All the moderation commands are listed below.\n'
                    'Options inside "<>" are required while options inside "[]" are optional.',
        color=config['colors']['primary']
    )
    embed.set_footer(text='Skyblock University Bot')
    embed.add_field(name="Ban", value="`+ban <@mention> [reason]`", inline=False)
    embed.add_field(name="Mute", value="`+mute <@mention> <time> [reason]`\n"
                                       "*Max mute duration is 28 days.\n"
                                       "Mods can mute themselves.*", inline=False)
    embed.add_field(name="Unmute", value="`+unmute <@mention> [reason]`", inline=False)
    embed.add_field(name="Reputation specific commands", value="`+rep help`", inline=False)
    embed.add_field(name="Banlist specific commands", value="`+banlist help`", inline=False)
    embed.add_field(name="Inactives specific commands", value="`+inactive help`", inline=False)
    embed.add_field(name="Suggestions specific commands", value="`+suggestions help`", inline=False)
    embed.add_field(name="Crisis specific commands", value="`+crisis help`", inline=False)
    embed.add_field(name="Qotd specific commands", value="`+qotd help`", inline=False)
    embed.add_field(name="Triggers specific commands", value='`+trigger help`', inline=False)
    await ctx.reply(embed=embed)


@bot.command()
@commands.has_role(config['admin_role_id'])
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
            description=f'Command is on cooldown. Try again in {int(exception.retry_after)} seconds',
            color=config['colors']['error']
        )
        await ctx.reply(embed=embed)

    elif isinstance(exception, commands.MissingRole):
        embed = discord.Embed(
            title='Error',
            description=f'Insufficient permissions, only members '
                        f'with **{ctx.guild.get_role(exception.missing_role).name}** role can run this command',
            color=config['colors']['error']
        )
        await ctx.reply(embed=embed)

    elif isinstance(exception, discord.Forbidden):
        embed = discord.Embed(
            title='Error',
            description='Bot does not have permissions to do this.',
            color=config['colors']['error']
        )
        await ctx.reply(embed=embed)
    elif isinstance(exception, (commands.CommandNotFound, commands.MissingRequiredArgument, commands.BadArgument)):
        pass
    else:
        try:
            await log_error(ctx, exception)
        except AttributeError:
            await bot.get_channel(config['bot_log_channel_id']).send('Exception passed to main:\n' +
                                                                     exception_to_string("main", exception))
            return


@bot.event
async def on_message(message: discord.Message):
    await bot.process_commands(message)


if __name__ == '__main__':
    run_setup()
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
    asyncio.run(DBConnection().close_db())
