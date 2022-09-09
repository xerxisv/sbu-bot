import os
import random

import discord
import discord.utils
from discord.ext import commands
from dotenv import load_dotenv

from utils.constants import BOT_OWNER_ROLE

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="+", intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"{bot.user} is ready")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# bot.load_extension('jishaku')
@bot.command()
async def load(ctx, extension):
    if ctx.message.author.id == BOT_OWNER_ROLE:
        bot.load_extension(f'cogs.{extension}')
        await ctx.reply("Loaded")
    else:
        await ctx.send("Insufficient permissions, only bot owners can run this command")


@bot.command()
@commands.has_permissions(ban_members=True)
async def unload(ctx, extension):
    if ctx.message.author.id == BOT_OWNER_ROLE:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.reply("Unloaded")
    else:
        await ctx.send("Insufficient permissions, only bot owners can run this command")


@bot.command()
async def reload(ctx):
    if ctx.message.author.id == BOT_OWNER_ROLE:
        for filename1 in os.listdir('./cogs'):
            if filename1.endswith('.py'):
                bot.unload_extension(f'cogs.{filename1[:-3]}')

        for filename1 in os.listdir('./cogs'):
            if filename1.endswith('.py'):
                bot.load_extension(f'cogs.{filename1[:-3]}')
        await ctx.reply("All cogs reloaded")
    else:
        await ctx.send("Insufficient permissions, only bot owners can run this command")


# noinspection SpellCheckingInspection
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title='Help',
        description='All the help commands are listed below',
        colour=discord.Colour.red()
    )
    embed.set_footer(text='SBU Custom Bot')
    embed.add_field(name="ping", value="Pong!", inline=False)
    embed.add_field(name="verify", value="Link your discord and hypixel accounts", inline=False)
    embed.add_field(name="unverify", value="UnLink your discord and hypixel accounts", inline=False)
    embed.add_field(name="hypixel", value="Lists hypixel stats", inline=False)
    embed.add_field(name="checkreq", value="Check if you meet reqs for SB Masters \n `+checkreq IGN`", inline=False)
    embed.add_field(name="repgive", value="Give a reputation for a carry \n `+repgive @mention Reason`", inline=False)
    embed.add_field(name="suggest", value="Suggest something \n `+suggest Suggestion`", inline=False)
    embed.add_field(name="Inactive", value="`+inactiveadd IGN Time`", inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_role("Junior Moderator")
async def modhelp(ctx):
    embed = discord.Embed(
        title='Moderation Commands',
        description='All the moderation commands are listed below',
        colour=discord.Colour.red()
    )
    embed.set_footer(text='SBU Custom Bot')
    embed.add_field(name="ban", value="`+ban User Reason`", inline=False)
    embed.add_field(name="mute", value="`+mute User Time Reason`", inline=False)
    embed.add_field(name="unmute", value="`+unmute User Reason`", inline=False)
    embed.add_field(name="Lookup section for Rank Academy ", value="`+lookupsection`", inline=False)
    embed.add_field(name="Shortened questions for promo for Instr and higher", value="`+ras`", inline=False)
    embed.add_field(name="Add a banned member to banned list", value="`+banlist IGN`", inline=False)
    embed.add_field(name="Activate SBU's Crisis Mode", value="`+crisis`", inline=False)
    embed.add_field(name="Deactivate SBU's Crisis Mode", value="`+crisisend`", inline=False)
    embed.add_field(name="Check inactive kicks for a guild", value="`+inactive GUILDNAME`", inline=False)
    embed.add_field(name="QOTD", value="`+qotdadd QOTD`", inline=False)
    embed.add_field(name="Inactives", value="`+inactive GUILD`", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def dm(ctx, member: discord.Member, *, message: str):
    if ctx.message.author.id == BOT_OWNER_ROLE:
        await member.send(message)
        await ctx.send("User Dmed")
    else:
        await ctx.send("Insufficient permissions, only bot owners can run this command")


@bot.event
async def on_message(message):
    if message.content.upper() == "MEOW":
        if message.author.id == 397389995113185293:
            await message.reply("Meow")
    elif message.content.upper() == "MEOWO":
        if message.author.id in [397389995113185293, 462940637595959296]:
            await message.reply("UwU meow")
    elif message.content.upper() == "FLOP":
        if message.author.id in [615987518890049555, 462940637595959296]:
            array = ["<:turtlefire:945023173353697320>", "Fleee", "All hail King Flop"]
            random_message = random.sample(range(0, len(array)), 1)
            await message.reply(array[random_message[0]])
    elif message.content.upper() == "PINGU":
        if message.author.id in [381494697073573899, 462940637595959296]:
            array = ["<:poguin:933279319579561986>", "<a:pingupat:932962348908560417>", "UwU",
                     "https://tenor.com/view/noot-noot-apocalypse-gif-25788876"]
            random_message = random.sample(range(0, len(array)), 1)
            await message.reply(array[random_message[0]])
    elif message.content.upper() == "JACK":
        if message.author.id in [358670711109320705, 462940637595959296, 397389995113185293, 438529479355400194]:
            await message.reply("Go play <@909802667495268372> in <#910961553480765440>")
    elif message.content.upper() == "NEO":
        if message.author.id in [566329261535920175]:
            await message.reply("op")
    elif message.content.upper() == "WINDOW":
        if message.author.id in [797274543042986024]:
            await message.reply("https://tenor.com/view/monkey-gif-8660294")
    elif message.content.upper() == "PLEB":
        if message.author.id in [519985798393626634, 462940637595959296]:
            await message.reply("shitting on the bw gamers.")
    elif message.content.upper() == "MEEP":
        if message.author.id in [681475158975971329, 462940637595959296]:
            await message.reply("https://tenor.com/view/meap-phineas-and-ferb-phineas-and-ferb-meap-meep-gif-14038245")
    elif message.content.upper() == "MEGA":
        if message.author.id in [675106662302089247, 462940637595959296]:
            await message.reply("https://tenor.com/view/megalorian-tykhe-gif-24043314")
    elif message.content.upper() == "HMM":
        if message.author.id in [283326249735028736]:
            await message.reply("mhm")
    await bot.process_commands(message)


load_dotenv()
bot.run(os.getenv("TOKEN"))
