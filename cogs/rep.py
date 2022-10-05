from math import ceil

import aiosqlite
import discord
from discord.ext import commands

from utils.constants import ADMIN_ROLE_ID, CARRY_SERVICE_REPS_CHANNEL_ID, CRAFT_REPS_CHANNEL_ID, SBU_GOLD, \
    SBU_LOGO_URL, SBU_PURPLE
from utils.error_utils import log_error
from utils.database.schemas import RepCommand


class Reputations(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name='rep', aliases=['reputation'])
    async def rep(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('rep help').invoke(ctx)
            return
        await ctx.trigger_typing()

    @rep.command(name='help', aliases=['commands'])
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title='Command Help',
            colour=SBU_GOLD
        )
        embed.add_field(name='Give reputation to a user.',
                        value='`+rep give <@mention | ID> <comments>`\n'
                              f'*It can only be used in <#{CRAFT_REPS_CHANNEL_ID}> or '
                              f'<#{CARRY_SERVICE_REPS_CHANNEL_ID}>*',
                        inline=False)
        embed.add_field(name='Remove a reputation from a user.',
                        value='`+rep remove <rep_ID>`\n'
                              '*__Administrator__ command*',
                        inline=False)
        embed.add_field(name='Show the reputation a user has received.',
                        value='`+rep show receiver <@mention | ID> [page]`\n'
                              '*__Administrator__ command*',
                        inline=False)
        embed.add_field(name='Show the reputation a user has given.',
                        value='`+rep show provider <@mention | ID:> [page]`\n'
                              '*__Administrator__ command*',
                        inline=False)
        embed.add_field(name='Give reputation to a user as another user',
                        value='`+rep admin give <@mention | ID> <@mention | ID> '
                              '<type: craft | carry> <comments>`\n'
                              '*__Administrator__ command*',
                        inline=False)
        embed.add_field(name='Command aliases list',
                        value='`+rep aliases`',
                        inline=False)

        await ctx.reply(embed=embed)

    @rep.command(name='alias', aliases=['aliases'])
    async def alias(self, ctx: commands.Context):
        embed = discord.Embed(
            title='Command aliases',
            colour=SBU_GOLD
        )

        embed.add_field(name='rep', value='"reputation"', inline=False)
        embed.add_field(name='give', value='"add"', inline=False)
        embed.add_field(name='remove', value='"rm", "delete", "del"', inline=False)
        embed.add_field(name='show', value='"list", "print"', inline=False)
        embed.add_field(name='receiver', value='"getter"', inline=False)
        embed.add_field(name='provider', value='"giver"', inline=False)
        embed.add_field(name='admin', value='"administrator"', inline=False)

        await ctx.reply(embed=embed)

    @rep.command(aliases=['add'])
    @commands.cooldown(1, 5)
    async def give(self, ctx: commands.Context, receiver: discord.Member, *, comments: str):
        if ctx.channel.id not in [CRAFT_REPS_CHANNEL_ID, CARRY_SERVICE_REPS_CHANNEL_ID]:
            embed = discord.Embed(
                title='Error',
                description='This command cannot be used here.\n'
                            f'Use in <#{CARRY_SERVICE_REPS_CHANNEL_ID}> if you want to give rep for a carry,\n'
                            f'or in <#{CRAFT_REPS_CHANNEL_ID}> for crafting/lending/reforging.',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        if ctx.author.id == receiver.id:
            embed = discord.Embed(
                title='Error',
                description='You can\'t rep yourself.',
                colour=0xFF0000
            )
            await ctx.send(embed=embed, delete_after=15)
            await ctx.message.delete(delay=15)
            return

        if len(comments) > 500:
            embed = discord.Embed(
                title='Error',
                description='Rep can\'t be longer than 500 characters.',
                colour=0xFF0000
            )
            await ctx.send(embed=embed, delete_after=15)
            await ctx.message.delete(delay=15)
            return

        async with aiosqlite.connect(RepCommand.DB_PATH + RepCommand.DB_NAME + '.db') as db:
            cursor = await db.cursor()
            await cursor.execute(RepCommand.get_max_rep_id())

            rep_id = (await cursor.fetchone())[0] + 1
            rep_type = 'carry' if ctx.channel.id == CARRY_SERVICE_REPS_CHANNEL_ID else 'craft'

            rep = RepCommand(rep_id, receiver.id, ctx.author.id, comments, rep_type)

            await cursor.execute(*(rep.insert()))
            await db.commit()

            rep_embed = discord.Embed(
                title=f'{rep_type.title()} Reputation Given',
                colour=SBU_PURPLE
            )

            rep_embed.set_author(name=f'Reputation by {ctx.message.author.name}')
            rep_embed.add_field(name='Receiver', value=receiver.mention, inline=True)
            rep_embed.add_field(name='Comments', value=comments, inline=False)
            rep_embed.set_footer(text=f'Rep ID: {rep_id}')
            rep_embed.set_thumbnail(url=SBU_LOGO_URL)

            message = await ctx.message.channel \
                .send(embed=rep_embed)

            await cursor.execute(rep.set_message(message.id))
            await db.commit()

        embed = discord.Embed(
            title='Success',
            description=f'Successfully gave rep to {receiver.mention}',
            colour=0x00FF00
        )

        await ctx.reply(embed=embed, delete_after=15)
        await ctx.message.delete(delay=15)

    @give.error
    async def give_error(self, ctx: commands.Context, exception):
        if isinstance(exception, (commands.MissingRequiredArgument, commands.BadArgument)):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+rep give <@mention | ID: integer> <comments: text>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed, delete_after=15)
            await ctx.message.delete(delay=15)

        elif isinstance(exception, commands.UserNotFound):
            embed = discord.Embed(
                title='Error',
                description='Invalid user. Use `+rep show provider <@mention | ID: integer> [page: integer]`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed, delete_after=15)
            await ctx.message.delete(delay=15)

    @rep.command(name='remove', aliases=['rm', 'delete', 'del'])
    @commands.has_role(ADMIN_ROLE_ID)
    @commands.cooldown(1, 5)
    async def remove(self, ctx: commands.Context, rep_id: int):
        async with aiosqlite.connect(RepCommand.DB_PATH + RepCommand.DB_NAME + '.db') as db:
            cursor = await db.cursor()
            await cursor.execute(RepCommand.select_row_with_id(rep_id))
            rep_tuple = await cursor.fetchone()

            if rep_tuple is None:
                embed = discord.Embed(title='Error',
                                      description=f'Reputation with id {rep_id} not found.',
                                      colour=0xFF0000)
                await ctx.send(embed=embed, delete_after=15)
                await ctx.message.delete(delay=15)
                await db.close()
                return

            rep = RepCommand.dict_from_tuple(rep_tuple)

            await cursor.execute(RepCommand.delete_row_with_id(rep_id))

            embed = None
            channel_id = CARRY_SERVICE_REPS_CHANNEL_ID if rep['type'] == 'carry' else CRAFT_REPS_CHANNEL_ID

            try:
                await ctx.guild \
                    .get_channel(channel_id) \
                    .get_partial_message(rep['msg_id']) \
                    .delete()
            except discord.NotFound as exception:
                await log_error(ctx, exception)
                embed = discord.Embed(title=f'Partial Deletion', description=f'Reputation with id {rep_id} removed from'
                                                                             f' database but not from <#{channel_id}>.',
                                      colour=0xFFFF00)
            else:
                embed = discord.Embed(title=f'Successful Deletion', description=f'Reputation with id {rep_id} removed'
                                                                                f' from <#{channel_id}>.',
                                      colour=0x00FF00)
            finally:
                delete = ctx.message.channel.id in [CRAFT_REPS_CHANNEL_ID, CARRY_SERVICE_REPS_CHANNEL_ID]

                await ctx.send(embed=embed, delete_after=15 if delete else None)
                if delete:
                    await ctx.message.delete(delay=15)

    @remove.error
    async def remove_error(self, ctx: commands.Context, exception):
        if isinstance(exception, (commands.MissingRequiredArgument, commands.MemberNotFound)):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+rep remove <rep_id: integer>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed, delete_after=15)
            await ctx.message.delete(delay=15)

    @rep.group(name='show', aliases=['list', 'print'])
    async def show(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('rep help').invoke(ctx)

    @show.command(name='receiver', aliases=['getter'])
    @commands.cooldown(1, 5)
    async def receiver(self, ctx: commands.Context, receiver: discord.User, page: int = 1):
        async with aiosqlite.connect(RepCommand.DB_PATH + RepCommand.DB_NAME + '.db') as db:
            cursor: aiosqlite.Cursor = await db.cursor()

            await cursor.execute(RepCommand.count_rows_with_receiver(receiver.id))
            rows = (await cursor.fetchone())[0]

            if rows == 0:
                embed = discord.Embed(
                    title='204',
                    description='User has not received any reps <a:confusion:1023126211586707547>',
                    colour=SBU_GOLD
                )
                await ctx.reply(embed=embed)
                return

            max_page = ceil(rows / RepCommand.LIMIT)

            if page > max_page or page < 1:
                embed = discord.Embed(
                    title='Error',
                    description=f'There is no page {page}. Valid pages are between 1 and {max_page}',
                    colour=0xFF0000
                )
                await ctx.reply(embed=embed)
                return

            await cursor.execute(RepCommand.select_rows_with_receiver(receiver.id, page))
            res = await cursor.fetchall()

            embed = discord.Embed(
                title=f'Reps Received by {receiver.display_name}',
                colour=SBU_GOLD
            )

            for rep_tuple in res:
                rep = RepCommand.dict_from_tuple(rep_tuple)
                provider = await ctx.bot.get_or_fetch_user(rep['provider'])

                embed.add_field(name=f"__Rep #{rep['rep_id']}__",
                                value=f"`{rep['comments']}`\n"
                                      f"*Type: {rep['type'].title()}*\n"
                                      f"*By: {provider.mention}*",
                                inline=False)

            embed.set_footer(text=f'Page: {page}/{max_page}')

            await ctx.reply(embed=embed)

    @receiver.error
    async def receiver_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+rep show receiver <@mention | ID: integer> [page: integer]`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
        elif isinstance(exception, commands.UserNotFound):
            embed = discord.Embed(
                title='Error',
                description='Invalid user. Use `+rep show receiver <@mention | ID: integer> [page: integer]`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)

    @show.command(name='provider', aliases=['giver'])
    @commands.cooldown(1, 5)
    async def provider(self, ctx: commands.Context, provider: discord.User, page: int = 1):
        async with aiosqlite.connect(RepCommand.DB_PATH + RepCommand.DB_NAME + '.db') as db:
            cursor: aiosqlite.Cursor = await db.cursor()

            await cursor.execute(RepCommand.count_rows_with_provider(provider.id))
            rows = (await cursor.fetchone())[0]

            if rows == 0:
                embed = discord.Embed(
                    title='204',
                    description='User has not provided any reps <a:confusion:1023126211586707547>',
                    colour=SBU_GOLD
                )
                await ctx.reply(embed=embed)
                return

            max_page = ceil(rows / RepCommand.LIMIT)

            if page > max_page or page < 1:
                embed = discord.Embed(
                    title='Error',
                    description=f'There is no page {page}. Valid pages are between 1 and {max_page}',
                    colour=0xFF0000
                )
                await ctx.reply(embed=embed)
                return

            await cursor.execute(RepCommand.select_rows_with_provider(provider.id, page))
            res = await cursor.fetchall()

            embed = discord.Embed(
                title=f'Reps Given by {provider.display_name}',
                colour=SBU_GOLD
            )

            for rep_tuple in res:
                rep = RepCommand.dict_from_tuple(rep_tuple)
                receiver = await ctx.bot.get_or_fetch_user(rep['receiver'])

                embed.add_field(name=f"__Rep #{rep['rep_id']}__",
                                value=f"`{rep['comments']}`\n"
                                      f"*Type: {rep['type'].title()}*\n"
                                      f"*To: {receiver.mention}*",
                                inline=False)

            embed.set_footer(text=f'Page: {page}/{max_page}')

            await ctx.reply(embed=embed)

    @provider.error
    async def provider_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format. Use `+rep show provider <@mention | ID: integer> [page: integer]`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
        elif isinstance(exception, commands.UserNotFound):
            embed = discord.Embed(
                title='Error',
                description='Invalid user. Use `+rep show provider <@mention | ID: integer> [page: integer]`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)

    @rep.group(name='admin', aliases=['administrator', 'fatman'])
    @commands.has_role(ADMIN_ROLE_ID)
    async def admin(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('rep help').invoke(ctx)

    @admin.command(name='give', aliases=['add'])
    @commands.cooldown(1, 5)
    async def give_from(self, ctx: commands.Context, receiver: discord.User, provider: discord.User, rep_type: str, *,
                        comments: str):
        rep_type = rep_type.lower()
        if rep_type not in ['craft', 'carry']:
            embed = discord.Embed(
                title='Error',
                description='Invalid rep type. Must be either `carry` or `craft`.\n'
                            'Run `+rep help` for more information.',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        if len(comments) > 500:
            embed = discord.Embed(
                title='Error',
                description='Rep can\'t be longer than 500 characters.',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        async with aiosqlite.connect(RepCommand.DB_PATH + RepCommand.DB_NAME + '.db') as db:
            cursor: aiosqlite.Cursor = await db.cursor()

            await cursor.execute(RepCommand.get_max_rep_id())
            rep_id = (await cursor.fetchone())[0] + 1

            rep = RepCommand(rep_id, receiver.id, provider.id, comments, rep_type)

            await cursor.execute(*(rep.insert()))
            await db.commit()

            rep_embed = discord.Embed(
                title=f'{rep_type.title()} Reputation Given',
                colour=SBU_PURPLE
            )

            rep_embed.set_author(name=f'Reputation by {provider.display_name}')
            rep_embed.add_field(name='Receiver', value=receiver.mention, inline=False)
            rep_embed.add_field(name='Comments', value=comments, inline=False)
            rep_embed.set_footer(text=f'Rep ID: {rep_id}')
            rep_embed.set_thumbnail(url=SBU_LOGO_URL)

            msg = await ctx.guild \
                .get_channel(CARRY_SERVICE_REPS_CHANNEL_ID if rep_type == 'carry' else CRAFT_REPS_CHANNEL_ID) \
                .send(embed=rep_embed)

            await cursor.execute(rep.set_message(msg.id))
            await db.commit()

            embed = discord.Embed(
                title='Success',
                description=f'Rep added successfully for {receiver.mention} by {provider.mention}',
                colour=0x00FF00
            )

            await ctx.reply(embed=embed)

    @give_from.error
    async def give_from_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.MissingRequiredArgument, commands.BadArgument)):
            embed = discord.Embed(
                title='Error',
                description='Incorrect format.\n'
                            'Use `+rep admin give <@mention | ID: integer> <@mention | ID: integer> '
                            '<type: craft | carry> <comments: text>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
        elif isinstance(exception, commands.UserNotFound):
            embed = discord.Embed(
                title='Error',
                description='Invalid user.\n'
                            'Use `+rep admin give <@mention | ID: integer> <@mention | ID: integer> '
                            '<type: craft | carry> <comments: text>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Reputations(bot))
