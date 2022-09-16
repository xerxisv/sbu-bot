import sqlite3

import discord
import requests
from discord.ext import commands

from utils.constants import BANNED_LIST_CHANNEL_ID, MODERATOR_ROLE_ID
from utils.schemas.BannedMember import BannedMember


class BanList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def banlist(self, ctx: commands.Context, banned_ign: str, *, reason: str = 'None'):
        banned_id = BanList.extract_id(banned_ign)

        if banned_id is None:
            embed = discord.Embed(
                title='Error',
                description='Invalid IGN',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        db = sqlite3.connect(BannedMember.DB_PATH + BannedMember.DB_NAME + '.db')
        cursor = db.cursor()

        # Check if user is already banned
        cursor.execute(BannedMember.select_row_with_id(banned_id))

        if cursor.fetchone() is not None:
            embed = discord.Embed(
                title='Operation Canceled',
                description='User is already banned',
                colour=0xFFFF00
            )
            await ctx.reply(embed=embed)
            return

        banned_member = BannedMember(banned_id, reason, ctx.author.id)  # Create banned member instance

        # Save banned member to database
        cursor.execute(*(banned_member.insert()))
        db.commit()
        db.close()

        # Send response
        banned_embed = discord.Embed(
            title='Banned Member',
            description='',
            colour=discord.Colour.light_gray()
        )

        banned_embed.set_footer(text='SBU Banned List')
        banned_embed.add_field(name='User UUID', value=banned_ign, inline=False)
        banned_embed.add_field(name='Reason', value=reason, inline=False)
        banned_embed.add_field(name='UUID Converter', value=f'https://mcuuid.net/?q={banned_ign}', inline=False)

        await ctx.guild \
            .get_channel(BANNED_LIST_CHANNEL_ID) \
            .send(embed=banned_embed)

        response_embed = discord.Embed(
            title='Success',
            description=f'User *{banned_ign}* added to <#{BANNED_LIST_CHANNEL_ID}>',
            colour=0x00FF00
        )

        await ctx.reply(embed=response_embed)

    @banlist.error
    async def banlist_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Insufficient Permissions")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Incorrect format. Use `+banlist <IGN: text> [Reason: text]`")

    @commands.command()
    async def bancheck(self, ctx: commands.Context, banned_ign: str):

        banned_id = BanList.extract_id(banned_ign)

        if banned_id is None:
            embed = discord.Embed(
                title='Error',
                description='Invalid IGN',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        db = sqlite3.connect(BannedMember.DB_PATH + BannedMember.DB_NAME + '.db')
        cursor = db.cursor()
        cursor.execute(BannedMember.select_row_with_id(banned_id))
        banned = cursor.fetchone()
        db.close()

        embed: discord.Embed

        if banned is None:
            embed = discord.Embed(
                title='User not found',
                description='User is not present in our banned list',
                colour=0x00FF00
            )
        else:
            banned = BannedMember.dict_from_tuple(banned)
            embed = discord.Embed(
                title='User found',
                description='User is present in our banned list',
                colour=0xFF0000
            )
            embed.add_field(name='Reason', value=f'{banned["reason"]}', inline=False)
            embed.set_footer(text=f'Banned by <@{banned["moderator"]}>')

        await ctx.reply(embed=embed)

    @bancheck.error
    async def ban_check_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+bancheck <IGN: text>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)

    @staticmethod
    def extract_id(ign: str):
        # Fetch user info
        res = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}')

        if res.status_code != 200:  # Ensure that the request returned a user
            return None

        return res.json()['id']  # Return user's UUID


def setup(bot):
    bot.add_cog(BanList(bot))
