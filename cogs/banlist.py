import aiosqlite
import discord
import requests
from discord.ext import commands

from utils.constants import BANNED_LIST_CHANNEL_ID, MODERATOR_ROLE_ID
from utils.schemas.BannedMember import BannedMember


class BanList(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Group
    async def banlist(self, ctx: commands.Context):
        return

    @banlist.command()
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title='Command help',
            colour=0xc0c09e
        )
        embed.add_field(name=f'Add a user to banned-list',
                        value='`+banlist add <IGN: text> [reason: text]`',
                        inline=False)
        embed.add_field(name=f'Remove a user from banned-list',
                        value='`+banlist remove <IGN: text>`',
                        inline=False)
        embed.add_field(name='Check if a user if banned',
                        value='`+banlist check <IGN: text>`')
        embed.add_field(name='List all info related to the ban of the user',
                        value='`+banlist info <IGN: text>`',
                        inline=False)

        await ctx.reply(embed=embed)

    @banlist.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def add(self, ctx: commands.Context, banned_ign: str, *, reason: str = 'None'):
        banned_id = extract_uuid(banned_ign)

        if banned_id is None:
            embed = discord.Embed(
                title='Error',
                description='Invalid IGN',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        db = await aiosqlite.connect(BannedMember.DB_PATH + BannedMember.DB_NAME + '.db')
        cursor = await db.cursor()

        # Check if user is already banned
        await cursor.execute(BannedMember.select_row_with_id(banned_id))

        if await cursor.fetchone() is not None:
            embed = discord.Embed(
                title='Operation Canceled',
                description='User is already banned',
                colour=0xFFFF00
            )
            await ctx.reply(embed=embed)
            await db.close()
            return

        banned_member = BannedMember(banned_id, reason, ctx.author.id)  # Create banned member instance

        # Save banned member to database
        await cursor.execute(*(banned_member.insert()))

        # Send response
        banned_embed = discord.Embed(
            title='Banned Member',
            description='',
            colour=discord.Colour.light_gray()
        )

        banned_embed.set_footer(text='SBU Banned List')
        banned_embed.add_field(name='User IGN', value=f'`{banned_ign}`', inline=False)
        banned_embed.add_field(name='Reason', value=reason, inline=False)
        banned_embed.add_field(name='UUID Converter', value=f'https://mcuuid.net/?q={banned_id}', inline=False)

        msg = await ctx.guild \
            .get_channel(BANNED_LIST_CHANNEL_ID) \
            .send(embed=banned_embed)

        response_embed = discord.Embed(
            title='Success',
            description=f'User `{banned_ign}` added to <#{BANNED_LIST_CHANNEL_ID}>',
            colour=0x00FF00
        )

        await cursor.execute(banned_member.insert_msg(msg.id))

        await ctx.reply(embed=response_embed)
        await db.commit()
        await db.close()

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Incorrect format. Use `+banlist add <IGN: text> [Reason: text]`")

    @banlist.command()
    async def check(self, ctx: commands.Context, banned_ign: str):

        banned_id = extract_uuid(banned_ign)

        if banned_id is None:
            embed = discord.Embed(
                title='Error',
                description='Invalid IGN',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        db = await aiosqlite.connect(BannedMember.DB_PATH + BannedMember.DB_NAME + '.db')
        cursor = await db.cursor()
        await cursor.execute(BannedMember.select_row_with_id(banned_id))
        banned = await cursor.fetchone()
        await db.close()

        embed: discord.Embed

        if banned is None:
            embed = discord.Embed(
                title='Clear',
                description='User is not present in our banned list',
                colour=0x00FF00
            )
        else:
            banned = BannedMember.dict_from_tuple(banned)
            mod = await self.bot.get_or_fetch_user(banned['moderator'])

            embed = discord.Embed(
                title='Not clear',
                description='User is present in our banned list',
                colour=0xFF0000
            )
            embed.add_field(name='Reason', value=f'{banned["reason"]}', inline=False)
            embed.set_footer(text=f'Banned by {mod if mod is not None else banned["moderator"]}')

        await ctx.reply(embed=embed)

    @check.error
    async def check_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+banlist check <IGN: text>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)

    @banlist.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def remove(self, ctx: commands.Context, ign: str):
        banned_uuid = extract_uuid(ign)

        if banned_uuid is None:
            embed = discord.Embed(
                title='Error',
                description='Invalid IGN',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        banned = await fetch_user_from_db(banned_uuid)

        if banned is None:
            embed = discord.Embed(
                title='Error',
                description='User is not present in our database',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        msg_id = banned['message']
        try:
            await ctx.guild.get_channel(BANNED_LIST_CHANNEL_ID).get_partial_message(msg_id).delete()
        except discord.HTTPException:
            pass

        db = await aiosqlite.connect(BannedMember.DB_PATH + BannedMember.DB_NAME + '.db')
        cursor = await db.cursor()

        await cursor.execute(BannedMember.delete_row_with_id(banned_uuid))

        embed = discord.Embed(
            title='Success',
            description=f'User `{ign}` was removed from <#{BANNED_LIST_CHANNEL_ID}>',
            colour=0x00FF00
        )

        await db.commit()
        await db.close()

        await ctx.reply(embed=embed)

    @remove.error
    async def remove_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+banlist remove <IGN: text>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)

    @banlist.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def info(self, ctx: commands.Context, ign: str):
        banned_uuid = extract_uuid(ign)

        if banned_uuid is None:
            embed = discord.Embed(
                title='Error',
                description='Invalid IGN',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        banned = await fetch_user_from_db(banned_uuid)

        if banned is None:
            embed = discord.Embed(
                title='Error',
                description='User is not present in our database',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        embed = discord.Embed(
            title='Banned User Info',
            colour=0xFFFF00
        )

        moderator = await self.bot.get_or_fetch_user(banned['moderator'])

        embed.add_field(name='IGN', value=ign, inline=False)
        embed.add_field(name='UUID', value=banned_uuid, inline=False)
        embed.add_field(name='Banned by', value=f'{moderator.mention}', inline=False)
        embed.add_field(name='Reason', value=banned['reason'], inline=False)
        embed.add_field(name='Ban Date', value=f'<t:{banned["banned_at"]}>', inline=False)

        await ctx.reply(embed=embed)

    @info.error
    async def info_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+banlist check <IGN: text>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)


async def fetch_user_from_db(uuid: str):
    db = await aiosqlite.connect(BannedMember.DB_PATH + BannedMember.DB_NAME + '.db')
    cursor = await db.cursor()

    await cursor.execute(BannedMember.select_row_with_id(uuid))
    res = await cursor.fetchone()

    if res is None:
        return None

    return BannedMember.dict_from_tuple(res)


def extract_uuid(ign: str):
    # Fetch user info
    res = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}')

    if res.status_code != 200:  # Ensure that the request returned a user
        return None

    return res.json()['id']  # Return user's UUID


def setup(bot):
    bot.add_cog(BanList(bot))
