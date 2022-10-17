import os
from random import choice

import discord
import discord.utils
from discord.ext import commands
from dotenv import load_dotenv

from utils.constants import ADMIN_CHAT_CHANNEL_ID, BOT_OWNER_ROLE_ID, CARRY_SERVICE_REPS_CHANNEL_ID, \
    CRAFT_REPS_CHANNEL_ID, JR_MOD_ROLE_ID, SBU_BOT_LOGS_CHANNEL_ID, SBU_GOLD
from utils.error_utils import exception_to_string, log_error
from utils.setup import run_setup

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="+", intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"{bot.user} is ready")
    channel = bot.get_channel(ADMIN_CHAT_CHANNEL_ID)
    await channel.send(f"<@&{BOT_OWNER_ROLE_ID}> The Bot has been recently rebooted. "
                       "Please enable all the necessary cogs.\nhttps://tenor.com/view/hacker-gif-19246062")


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
    elif isinstance(exception, commands.CommandNotFound):
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
    # Prevents the bot from going through the if statements unnecessarily when the message is a command or a bot reply
    if message.content.startswith('+') or message.author == bot.user:
        pass
    elif message.content.upper() == "MEOW":
        if message.author.id == 397389995113185293:
            await message.reply("Meow")
    
    elif message.content.upper() == "IMPLINKS":
        if message.author.id in ['491654047741509633','351827324758523905','309231901212672001','606917358438580224','519985798393626634','241589674131456000']:
            await message.reply("MEE6 Dashboard: https://mee6.xyz/dashboard/\nTicket Tool: https://tickettool.xyz/manage-servers\nYAGPDB: https://yagpdb.xyz/\nGiveaway Boat: https://giveaway.boats/dashboard/\nTatsu Dashboard: https://tatsu.gg/\nDyno: https://dyno.gg/\nWick Dashboard: https://wickbot.com/\nSBU Bot: https://github.com/xerxisv/sbu-bot/

    elif message.content.upper() == "MEOWO":
        if message.author.id == 397389995113185293:
            await message.reply("UwU meow")

    elif message.content.upper() == "FLOP":
        if message.author.id == 615987518890049555:
            array = ["<:turtleonfire:1021834121347084309>", "Fleee", "All hail King Flop",
                     "https://i.imgur.com/pnruanZ.png"]
            await message.reply(choice(array))

    elif message.content.upper() == "PINGU":
        if message.author.id == 381494697073573899:
            array = [
                "<a:poguin:933279319579561986>", "<a:pingupat:932962348908560417>", "UwU",
                "https://tenor.com/view/noot-noot-apocalypse-gif-25788876"]
            await message.reply(choice(array))

    elif message.content.upper() == "NEO":
        if message.author.id == 566329261535920175:
            await message.reply("op")

    elif message.content.upper() == "WINDOW":
        if message.author.id == 797274543042986024:
            await message.reply("https://tenor.com/view/monkey-gif-8660294")

    elif message.content.upper() == "PLEB":
        if message.author.id == 519985798393626634:
            await message.reply("shitting on the bw gamers.")

    elif message.content.upper() == "MEEP":
        if message.author.id == 681475158975971329:
            await message.reply("https://tenor.com/view/meap-phineas-and-ferb-phineas-and-ferb-meap-meep-gif-14038245")

    elif message.content.upper() == "MEGA":
        if message.author.id == 675106662302089247:
            await message.reply("https://tenor.com/view/megalorian-tykhe-gif-24043314")

    elif message.content.upper() == "HMM":
        if message.author.id == 283326249735028736:
            await message.reply("mhm")

    elif message.content.upper() == "CHOMP":
        if message.author.id == 241589674131456000:
            await message.reply("https://tenor.com/view/cat-bite-funny-chomp-gif-16986241")

    elif message.content.upper() in ["AGREED", 'I AGREE']:
        if message.author.id == 309231901212672001:
            await message.reply("https://tenor.com/view/metal-gear-rising-gif-25913914")

    elif message.content.upper() == "CANNIBALISM":
        if message.author.id in [606917358438580224, 241589674131456000]:
            array = ["Pog!", "Noses!", "Toes!", "Fungus!", "https://i.imgur.com/IJ8URxl.jpg"]
            await message.reply(choice(array))

    elif message.content.upper() == "MUDKIP":
        if message.author.id == 895488539775598603:
            await message.reply("https://tenor.com/view/mudkip-spin-gif-24834722")
        
    elif message.content == "RANDOM":
        if message.author.id == 491654047741509633:
            await message.reply("https://cdn.discordapp.com/emojis/967203616966459412")
    elif message.content == "FIRE":
        if message.author.id == 856492201529835521:
            await message.reply("https://cdn.discordapp.com/emojis/943095611161460739.webp?size=128&quality=lossless")
    elif message.content.upper() == "ZMAJ":
        if message.author.id == 852647923875446816:
            await message.reply("https://media.discordapp.net/attachments/1027212487008989284/1027212547591508070/cat-angry-cat.gif")

    await bot.process_commands(message)


if __name__ == '__main__':
    run_setup()
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
