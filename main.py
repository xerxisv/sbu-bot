import os

import discord
import discord.utils
from discord.ext import commands
from dotenv import load_dotenv
from random import choice

from utils.constants import BOT_OWNER_ROLE_ID, JR_MOD_ROLE_ID, SBU_BOT_LOGS_CHANNEL_ID, ADMIN_CHAT_CHANNEL_ID
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
async def load_all(ctx: discord.ext.commands.Context):
    for filename in os.listdir('./cogs'):
        if not filename.endswith('.py'):
            continue

        bot.load_extension(f'cogs.{filename[:-3]}')

    await ctx.reply('Cogs loaded successfully')


@bot.command()
@commands.has_role(BOT_OWNER_ROLE_ID)
async def load(ctx: discord.ext.commands.Context, extension):
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
async def unload(ctx, extension):
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
async def reload(ctx):
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
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')


@bot.command()
async def help(ctx: commands.Context):
    embed = discord.Embed(
        title='Help',
        description='All the help commands are listed below',
        colour=discord.Colour.red()
    )
    embed.set_footer(text='Skyblock University Bot')
    embed.add_field(name="ping", value="Pong!", inline=False)
    embed.add_field(name="verify", value="Link your discord and hypixel accounts", inline=False)
    embed.add_field(name="unverify", value="UnLink your discord and hypixel accounts", inline=False)
    embed.add_field(name="hypixel", value="Lists hypixel stats", inline=False)
    embed.add_field(name="checkreq", value="Check if you meet reqs for SB Masters \n `+checkreq IGN`", inline=False)
    embed.add_field(name="repgive", value="Give a reputation for a carry \n `+repgive @mention Reason`", inline=False)
    embed.add_field(name="suggest", value="Suggest something \n `+suggest Suggestion`", inline=False)
    embed.add_field(name="Inactive", value="`+inactiveadd IGN Time`", inline=False)
    await ctx.reply(embed=embed)


@bot.command()
@commands.has_role(JR_MOD_ROLE_ID)
async def modhelp(ctx: commands.Context):
    embed = discord.Embed(
        title='Moderation Commands',
        description='All the moderation commands are listed below',
        colour=discord.Colour.red()
    )
    embed.set_footer(text='Skyblock University Bot')
    embed.add_field(name="ban", value="`+ban User Reason`", inline=False)
    embed.add_field(name="mute", value="`+mute User Time Reason`", inline=False)
    embed.add_field(name="unmute", value="`+unmute User Reason`", inline=False)
    embed.add_field(name="Lookup section for Rank Academy ", value="`+lookupsection`", inline=False)
    embed.add_field(name="Shortened questions for promo for Instr and higher", value="`+ras`", inline=False)
    embed.add_field(name="Add a banned member to banned list", value="`+banlist IGN`", inline=False)
    embed.add_field(name="Removes a banned member from banned list", value="`+bandel IGN`", inline=False)
    embed.add_field(name="Check if user is banned", value="`+bancheck IGN`", inline=False)
    embed.add_field(name="Activate SBU's Crisis Mode", value="`+crisis`", inline=False)
    embed.add_field(name="Deactivate SBU's Crisis Mode", value="`+crisisend`", inline=False)
    embed.add_field(name="Check inactive kicks for a guild", value="`+inactive GUILDNAME`", inline=False)
    embed.add_field(name="QOTD", value="`+qotdadd QOTD`", inline=False)
    embed.add_field(name="Inactives", value="`+inactive GUILD`", inline=False)
    await ctx.reply(embed=embed)


@bot.command()
@commands.has_role(BOT_OWNER_ROLE_ID)
async def dm(ctx: discord.ext.commands.Context, member: discord.Member, *, message: str):
    try:
        await member.send(message)
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

    elif isinstance(exception, commands.BadArgument) or isinstance(exception, commands.MissingRequiredArgument):
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
    if message.content.upper() == "MEOW":
        if message.author.id == 397389995113185293:
            await message.reply("Meow")

    elif message.content.upper() == "MEOWO":
        if message.author.id == 397389995113185293:
            await message.reply("UwU meow")

    elif message.content.upper() == "FLOP":
        if message.author.id == 615987518890049555:
            array = ["<:turtleonfire:1021834121347084309>", "Fleee", "All hail King Flop"]
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

    elif message.content.upper() == "AGREED":  # pleb shush, I need to have my fun as well :)
        if message.author.id == 309231901212672001:
            await message.reply("https://tenor.com/view/metal-gear-rising-gif-25913914")
            
    elif message.content.upper() == "CANNIBALISM": 
        if message.author.id in [606917358438580224, 241589674131456000]:
            array = ["Pog!", "Noses!", "Toes!", "Fungus!"]
            await message.reply(choice(array))

    await bot.process_commands(message)


if __name__ == '__main__':
    run_setup()
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
