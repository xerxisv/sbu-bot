import aiosqlite
import discord
from discord.ext import commands

from utils import extract_uuid
from utils.config.config import ConfigHandler
from utils.database import DBConnection
from utils.database.schemas import BannedMember

config = ConfigHandler().get_config()


class BanList(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.db: aiosqlite.Connection = DBConnection().get_db()

    @commands.group(name='banlist', aliases=['bl'], case_insensitive=True)
    async def banlist(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('banlist help').invoke(ctx)
            return
        await ctx.trigger_typing()

    @banlist.command(name='help', aliases=['commands'])
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title='Command help',
            color=config['colors']['primary']
        )
        embed.add_field(name='Check if a user if banned',
                        value='`+banlist check <IGN>`')
        embed.add_field(name=f'Add a user to banned-list',
                        value='`+banlist add <IGN> [reason]`\n'
                              '*__Moderator__ command.*',
                        inline=False)
        embed.add_field(name=f'Remove a user from banned-list',
                        value='`+banlist remove <IGN>`\n'
                              '*__Moderator__ command.*',
                        inline=False)
        embed.add_field(name='List all info related to the ban of the user',
                        value='`+banlist info <IGN>`\n'
                              '*__Moderator__ command.*',
                        inline=False)
        embed.add_field(name='Command aliases list',
                        value='`+banlist aliases`',
                        inline=False)

        await ctx.reply(embed=embed)

    @banlist.command(name='alias', aliases=['aliases'])
    async def alias(self, ctx: commands.Context):
        embed = discord.Embed(
            title='Command aliases',
            color=config['colors']['primary']
        )

        embed.add_field(name='banlist', value='"bl"', inline=False)
        embed.add_field(name='check', value='"c"', inline=False)
        embed.add_field(name='add', value='None', inline=False)
        embed.add_field(name='remove', value='"rm", "delete", "del"', inline=False)

        await ctx.reply(embed=embed)

    @banlist.command(name='add')
    @commands.has_role(config['mod_role_id'])
    @commands.cooldown(1, 5)
    async def add(self, ctx: commands.Context, banned_ign: str, *, reason: str = 'None'):
        banned_id = extract_uuid(banned_ign)

        if banned_id is None:
            embed = discord.Embed(
                title='Error',
                description='Invalid IGN',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        cursor: aiosqlite.Cursor = await self.db.cursor()

        # Check if user is already banned
        await cursor.execute(BannedMember.select_row_with_id(banned_id))

        if await cursor.fetchone() is not None:
            embed = discord.Embed(
                title='Operation Canceled',
                description='User is already banned',
                color=config['colors']['secondary']
            )
            await ctx.reply(embed=embed)
            return

        # Send response
        banned_embed = discord.Embed(
            title='Banned Member',
            description='',
            color=config['colors']['secondary']
        )

        banned_embed.set_footer(text='SBU Banned List')
        banned_embed.add_field(name='User IGN', value=f'`{banned_ign}`', inline=False)
        banned_embed.add_field(name='Reason', value=reason, inline=False)
        banned_embed.add_field(name='UUID Converter', value=f'https://mcuuid.net/?q={banned_id}', inline=False)

        msg = await ctx.guild \
            .get_channel(config['banlist']['channel_id']) \
            .send(embed=banned_embed)

        response_embed = discord.Embed(
            title='Success',
            description=f"User `{banned_ign}` added to <#{config['banlist']['channel_id']}>",
            color=config['colors']['success']
        )

        banned_member = BannedMember(banned_id, reason, ctx.author.id, msg.id)  # Create banned member instance

        # Save banned member to database
        await cursor.execute(*(banned_member.insert()))

        await ctx.reply(embed=response_embed)
        await cursor.close()
        await self.db.commit()

    @add.error
    async def add_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+banlist add <IGN> [reason]`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)

    @banlist.command(name='check', aliases=['c'])
    async def check(self, ctx: commands.Context, banned_ign: str):
        banned_id = extract_uuid(banned_ign)

        if banned_id is None:
            embed = discord.Embed(
                title='Error',
                description='Invalid IGN',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        banned = await fetch_user_from_db(banned_id)

        embed: discord.Embed

        if banned is None:
            embed = discord.Embed(
                title='Clear',
                description='User is not present in our banned list',
                color=config['colors']['success']
            )
        else:
            mod = await self.bot.get_or_fetch_user(banned['moderator'])

            embed = discord.Embed(
                title='Not clear',
                description='User is present in our banned list',
                color=config['colors']['error']
            )
            embed.add_field(name='Reason', value=f'{banned["reason"]}', inline=False)
            embed.set_footer(text=f'Banned by {mod if mod is not None else banned["moderator"]}')

        await ctx.reply(embed=embed)

    @check.error
    async def check_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+banlist check <IGN>`\nEx: `+banlist check RealMSpeed`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)

    @banlist.command(name='remove', aliases=['del', 'delete', 'rm'])
    @commands.has_role(config['mod_role_id'])
    @commands.cooldown(1, 5)
    async def remove(self, ctx: commands.Context, ign: str):
        banned_uuid = extract_uuid(ign)

        if banned_uuid is None:
            embed = discord.Embed(
                title='Error',
                description='Invalid IGN',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        banned = await fetch_user_from_db(banned_uuid)

        if banned is None:
            embed = discord.Embed(
                title='Error',
                description='User is not present in our database',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        msg_id = banned['message']
        try:
            await ctx.guild.get_channel(config['banlist']['channel_id']).get_partial_message(msg_id).delete()
        except discord.HTTPException:
            pass

        await self.db.execute(BannedMember.delete_row_with_id(banned_uuid))

        embed = discord.Embed(
            title='Success',
            description=f"User `{ign}` was removed from <#{config['banlist']['channel_id']}>",
            color=config['colors']['success']
        )

        await ctx.reply(embed=embed)
        await self.db.commit()

    @remove.error
    async def remove_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+banlist remove <IGN>`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)

    @banlist.command(name='info')
    @commands.has_role(config['mod_role_id'])
    async def info(self, ctx: commands.Context, ign: str):
        banned_uuid = extract_uuid(ign)

        if banned_uuid is None:
            embed = discord.Embed(
                title='Error',
                description='Invalid IGN',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        banned = await fetch_user_from_db(banned_uuid)

        if banned is None:
            embed = discord.Embed(
                title='Error',
                description='User is not present in our database',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)
            return

        embed = discord.Embed(
            title='Banned User Info',
            color=config['colors']['primary']
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
                description='Incorrect format. Use `+banlist check <IGN>`',
                color=config['colors']['error']
            )
            await ctx.reply(embed=embed)


async def fetch_user_from_db(uuid: str):
    cursor: aiosqlite.Cursor = await DBConnection().get_db().cursor()

    await cursor.execute(BannedMember.select_row_with_id(uuid))
    res = await cursor.fetchone()
    await cursor.close()

    if res is None:
        return None

    return BannedMember.dict_from_tuple(res)


def setup(bot: discord.Bot):
    bot.add_cog(BanList(bot))
