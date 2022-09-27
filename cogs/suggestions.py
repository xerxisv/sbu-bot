import datetime

import discord
import aiosqlite
from discord.ext import commands
from math import ceil

from utils.constants import ADMIN_ROLE_ID, SBU_LOGO_URL, SUGGESTIONS_CHANNEL_ID, SBU_GOLD
from utils.error_utils import log_error
from utils.schemas import Suggestion


class Suggestions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5)
    async def suggest(self, ctx: commands.Context, *, suggestion_str: str):
        if len(suggestion_str) > 500:
            embed = discord.Embed(
                title='Error',
                description='Suggestion can\'t be longer than 500 character'
            )
            await ctx.reply(embed=embed)
            return
        async with aiosqlite.connect(Suggestion.DB_PATH + Suggestion.DB_NAME + '.db') as db:
            # Fetch new suggestion ID
            cursor = await db.cursor()
            await cursor.execute(Suggestion.get_next_id())
            suggestion_num = (await cursor.fetchone())[0] + 1

            # Create embed
            suggestion_embed = discord.Embed(
                title=f'Suggestion',
                description=f'{suggestion_str}',
                timestamp=datetime.datetime.utcnow(),
                colour=SBU_GOLD
            )

            # Set author icon if there is one
            if ctx.message.author.avatar is not None:
                suggestion_embed.set_author(name=f'Suggested by {ctx.message.author}',
                                            icon_url=ctx.message.author.avatar)
            else:
                suggestion_embed.set_author(name=f'Suggested by {ctx.message.author}')

            suggestion_embed.set_footer(text=f'Suggestion number {suggestion_num}')
            suggestion_embed.set_thumbnail(url=SBU_LOGO_URL)

            channel = self.bot.get_channel(SUGGESTIONS_CHANNEL_ID)
            message = await channel.send(embed=suggestion_embed)

            await ctx.reply(f"Suggestion sent to <#{SUGGESTIONS_CHANNEL_ID}>")
            await message.add_reaction(':white_check_mark:')
            await message.add_reaction(':x:')

            suggestion = Suggestion(suggestion_num, message.id, suggestion_str, ctx.author.id)

            await cursor.execute(*(suggestion.insert()))

            await db.commit()

    @suggest.error
    async def on_suggest_error(self, ctx: commands.Context, exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            await ctx.reply('Incorrect format. Use `+suggest <suggestion: text>`')
            return

        raise exception

    @commands.group(name='suggestion', aliases=['suggestions', 'sg'])
    @commands.has_role(ADMIN_ROLE_ID)
    async def suggestion(self, ctx: commands.Context):
        await ctx.trigger_typing()
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('suggestion help').invoke(ctx)

    @suggestion.command()
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            title='Command Help',
            colour=SBU_GOLD
        )

        embed.add_field(name='Approve a suggestion',
                        value='`+suggestion approve <id: integer> [reason: text]`',
                        inline=False)
        embed.add_field(name='Deny a suggestion',
                        value='`+suggestion deny <id: integer> [reason: text]`',
                        inline=False)
        embed.add_field(name='Delete a suggestion',
                        value='`+suggestion delete <ID: integer>`',
                        inline=False)
        embed.add_field(name='List unanswered suggestions',
                        value='`+suggestion show answered [page: integer]`',
                        inline=False)
        embed.add_field(name='List approved or denied suggestions',
                        value='`+suggestion show approved [flag: bool]`',
                        inline=False)
        embed.add_field(name='List user specific suggestions',
                        value='`+suggestion show ideator <@mention | ID: integer>`',
                        inline=False)
        embed.add_field(name='List all info related to a suggestion',
                        value='`+suggestion show info <ID: integer>`')

        await ctx.reply(embed=embed)

    @suggestion.command(name='approve', aliases=['yes', 'accept'])
    @commands.cooldown(1, 5)
    async def approve(self, ctx: commands.Context, suggestion_id: int, *, reason=None):

        async with aiosqlite.connect(Suggestion.DB_PATH + Suggestion.DB_NAME + '.db') as db:
            cursor = await db.cursor()

            await cursor.execute(Suggestion.select_row_with_id(suggestion_id))
            suggestion_tuple = await cursor.fetchone()

            if suggestion_tuple is None:
                await ctx.reply("Suggestion not found.")
                return

            suggestion = Suggestion.dict_from_tuple(suggestion_tuple)

            suggestion_embed = discord.Embed(
                title=f'Approved',
                description=f"{suggestion['suggestion']}",
                timestamp=datetime.datetime.utcnow(),
                colour=SBU_GOLD
            )

            suggestion_author: discord.User = await self.bot.get_or_fetch_user(suggestion['author_id'])
            suggestion_author = suggestion_author if suggestion_author is not None else suggestion["author_id"]

            suggestion_embed.set_author(name=f'Suggested by {suggestion_author}')
            suggestion_embed.add_field(name="Reason", value=f"{reason}", inline=False)
            suggestion_embed.set_footer(text=f'Suggestion number {suggestion_id} | Approved by {ctx.author}')
            suggestion_embed.set_thumbnail(
                url=SBU_LOGO_URL)

            message: discord.PartialMessage = self.bot \
                .get_channel(SUGGESTIONS_CHANNEL_ID) \
                .get_partial_message(suggestion['message_id'])
            await message.edit(embed=suggestion_embed)

            approved_embed = discord.Embed(
                title=f'Approved',
                description=f'Suggestion number {suggestion_id} approved successfully.',
                timestamp=datetime.datetime.utcnow(),
                colour=0x00FF00
            )
            try:
                # Try DMing the user
                await suggestion_author.send(embed=suggestion_embed)
            except (discord.HTTPException, discord.Forbidden, AttributeError):
                # DMing can throw because: API error, user having DMs closed/ bad intents or suggestion_author is an int
                approved_embed.add_field(name="Direct Message", value=f"User could not be dmed", inline=False)

            except Exception as exception:
                # Any other error will be sent to the logs
                approved_embed.add_field(name="Direct Message", value=f"User could not be dmed", inline=False)
                await log_error(ctx, exception)

            else:
                # If no errors occurred send successful message
                approved_embed \
                    .add_field(name="Direct Message", value=f"{suggestion_author} dmed successfully", inline=False)

            finally:
                # Send the embed regardless of errors
                await ctx.send(embed=approved_embed, delete_after=10)

                set_approved_tuple = Suggestion.set_approved(suggestion_id, True, ctx.author.id, reason)

                await cursor.execute(*set_approved_tuple)
                await db.commit()

            await ctx.message.delete(delay=15)

    @approve.error
    async def on_approve_error(self, ctx: commands.Context, exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            await ctx.reply('Incorrect format. Use `+suggestion approve <suggestion_id: integer> [reason: text]`')
            return

        raise exception

    @suggestion.command(name='deny', aliases=['no', 'decline'])
    @commands.cooldown(1, 5)
    async def deny(self, ctx, suggestion_id: int, *, reason=None):
        async with aiosqlite.connect(Suggestion.DB_PATH + Suggestion.DB_NAME + '.db') as db:
            cursor = await db.cursor()

            await cursor.execute(Suggestion.select_row_with_id(suggestion_id))
            suggestion_tuple = await cursor.fetchone()

            if suggestion_tuple is None:
                await ctx.reply("Suggestion not found.")
                return

            suggestion = Suggestion.dict_from_tuple(suggestion_tuple)

            suggestion_embed = discord.Embed(
                title=f'Denied',
                description=f"{suggestion['suggestion']}",
                timestamp=datetime.datetime.utcnow(),
                colour=0xFF0000
            )

            suggestion_author: discord.User = await self.bot.get_or_fetch_user(suggestion['author_id'])
            suggestion_author = suggestion_author if suggestion_author is not None else suggestion["author_id"]

            suggestion_embed.set_author(name=f'Suggested by {suggestion_author}')
            suggestion_embed.set_footer(text=f'Suggestion number {suggestion_id} | Denied by {ctx.author}')
            suggestion_embed.add_field(name="Reason", value=f"{reason}", inline=False)
            suggestion_embed.set_thumbnail(url=SBU_LOGO_URL)

            message = self.bot.get_channel(SUGGESTIONS_CHANNEL_ID).get_partial_message(suggestion['message_id'])
            await message.edit(embed=suggestion_embed)

            approved_embed = discord.Embed(
                title=f'Denied',
                description=f'Suggestion number {suggestion_id} denied successfully.',
                timestamp=datetime.datetime.utcnow(),
                colour=0x0CE60C
            )

            try:
                # Try DMing the user
                await suggestion_author.send(embed=suggestion_embed)

            except (discord.HTTPException, discord.Forbidden, AttributeError):
                approved_embed.add_field(name="Direct Message", value=f"User could not be dmed", inline=False)

            except Exception as exception:
                # Any other error will be sent to the logs
                approved_embed.add_field(name="Direct Message", value=f"User could not be dmed", inline=False)
                await log_error(ctx, exception)

            else:
                # If no errors occurred send successful message
                approved_embed.add_field(name="Direct Message", value=f"{suggestion_author} dmed successfully",
                                         inline=False)
            finally:
                # Send the embed regardless of errors
                await ctx.reply(embed=approved_embed, delete_after=10)

                set_approved_tuple = Suggestion.set_approved(suggestion_id, False, ctx.author.id, reason)

                await cursor.execute(*set_approved_tuple)
                await db.commit()
            await ctx.message.delete(delay=10)

    @deny.error
    async def on_deny_error(self, ctx: commands.Context, exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            await ctx.reply('Incorrect format. Use `+suggestion deny <suggestion_id: integer> [reason: text]`')
            return

        raise exception

    @suggestion.command(name='delete', aliases=['del', 'remove', 'rm'])
    @commands.cooldown(1, 5)
    async def delete(self, ctx: commands.Context, _id: int):
        async with aiosqlite.connect(Suggestion.DB_PATH + Suggestion.DB_NAME + '.db') as db:
            # Connect to DB
            cursor = await db.cursor()

            await cursor.execute(Suggestion.select_row_with_id(_id))
            res = await cursor.fetchone()
            # Check if suggestion with given ID exists
            if res is None:
                embed = discord.Embed(
                    title='Error',
                    description=f'Suggestion with ID {_id} not found',
                    colour=0xFF0000
                )
                await ctx.reply(embed=embed)
                return

            suggestion = Suggestion.dict_from_tuple(res)

            # Delete suggestion
            await cursor.execute(Suggestion.delete_row_id(suggestion['suggestion_number']))
            await db.commit()

        msg = 'Suggestion deleted'
        try:
            await ctx.guild\
                .get_channel(SUGGESTIONS_CHANNEL_ID)\
                .get_partial_message(suggestion['message_id'])\
                .delete()
        except discord.HTTPException:
            msg = f'Suggestion deleted from database but' \
                  f'was not found in <#{SUGGESTIONS_CHANNEL_ID}>. Please delete manually'

        embed = discord.Embed(
            title='Success',
            description=msg,
            colour=0x00FF00
        )
        await ctx.reply(embed=embed)

    @delete.error
    async def delete_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+suggestion delete <suggestion_id: integer>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        raise exception

    @suggestion.group(name='list', aliases=['show', 'print'])
    async def show(self, ctx):
        pass

    @show.command(name='unanswered', aliases=['un', 'unresolved'])
    @commands.cooldown(1, 5)
    async def unanswered(self, ctx: commands.Context, page: int = 1):
        async with aiosqlite.connect(Suggestion.DB_PATH + Suggestion.DB_NAME + '.db') as db:
            cursor = await db.cursor()

            # Fetch number of unanswered suggestions
            await cursor.execute(Suggestion.count_unanswered_rows())
            rows = (await cursor.fetchone())[0]
            # Return if there are no suggestions to show
            if rows == 0:
                embed = discord.Embed(
                    title='204',
                    description='There are no unanswered suggestions <:mftea:843937999209365515>',
                    colour=0xc0c09e
                )
                await ctx.reply(embed=embed)
                return

            # Calculate max page
            max_page = ceil(rows/10)

            # Check that page is valid
            if page > max_page or page < 1:
                embed = discord.Embed(
                    title='Error',
                    description=f'There is no page {page}. Valid pages are between 1 and {max_page}',
                    colour=0xFF0000
                )
                await ctx.reply(embed=embed)
                return

            # Fetch suggestions, skipping (@page * 10) and limiting to 10
            await cursor.execute(Suggestion.select_unanswered_rows(page))
            res = await cursor.fetchall()

        # Add a field to the embed for every suggestion
        embed = discord.Embed(
            title='Unanswered suggestions'
        )

        for suggestion_tuple in res:
            # Convert response tuple to dictionary
            suggestion = Suggestion.dict_from_tuple(suggestion_tuple)
            # Fetch author
            author = await ctx.bot.get_or_fetch_user(suggestion['author_id'])
            # Add suggestion field
            embed.add_field(name=f"Suggestion __#{suggestion['suggestion_number']}__",
                            value=f"`{suggestion['suggestion']}`" +
                                  (f"\n*By {author.mention}*" if author else ""),
                            inline=False)

        embed.set_footer(text=f'Page: {page}/{max_page}')

        await ctx.reply(embed=embed)

    @unanswered.error
    async def unanswered_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+suggestion list unanswered [page: integer]`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        raise exception

    @show.command(name='approved', aliases=['accepted'])
    @commands.cooldown(1, 5)
    async def approved(self, ctx: commands.Context, flag: bool = True, page: int = 1):
        async with aiosqlite.connect(Suggestion.DB_PATH + Suggestion.DB_NAME + '.db') as db:
            # Connect to db & get cursor
            cursor = await db.cursor()

            # Get number of filtered rows
            await cursor.execute(Suggestion.count_approved(flag))
            rows = (await cursor.fetchone())[0]

            # If there are no rows return
            if rows == 0:
                embed = discord.Embed(
                    title=f'204',
                    description=f'There are no {"approved" if flag else "denied"} suggestions',
                    colour=SBU_GOLD
                )
                await ctx.reply(embed=embed)
                return

            # Calculate max page
            max_page = ceil(rows/10)

            # Check that page is valid
            if page > max_page or page < 1:
                embed = discord.Embed(
                    title='Error',
                    description=f'There is no page {page}. Valid pages are between 1 and {max_page}',
                    colour=0xFF0000
                )
                await ctx.reply(embed=embed)
                return

            # Get filtered rows
            await cursor.execute(Suggestion.select_approved(flag, page))
            res = await cursor.fetchall()

        embed = discord.Embed(
            title=f'{"Approved" if flag else "Denied"} Suggestions',
            colour=SBU_GOLD
        )

        for suggestion_tuple in res:
            # Convert suggestion tuple to dictionary
            suggestion = Suggestion.dict_from_tuple(suggestion_tuple)
            # Fetch author & admin
            author = await ctx.bot.get_or_fetch_user(suggestion['author_id'])
            # Add suggestion field
            embed.add_field(name=f"Suggestion __#{suggestion['suggestion_number']}__",
                            value=f"`{suggestion['suggestion']}`" +
                                  (f"\n*By {author.mention}*" if author else ""),
                            inline=False)

        embed.set_footer(text=f'Page: {page}/{max_page}')

        await ctx.reply(embed=embed)

    @approved.error
    async def approved_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+suggestion list answered <flag: bool>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        raise exception

    @show.command(name='ideator', aliases=['author', 'creator'])
    @commands.cooldown(1, 5)
    async def ideator(self, ctx: commands.Context, suggestion_author: discord.User, page: int = 1):
        async with aiosqlite.connect(Suggestion.DB_PATH + Suggestion.DB_NAME + '.db') as db:
            cursor = await db.cursor()

            await cursor.execute(Suggestion.count_rows_with_author_id(suggestion_author.id))
            rows = (await cursor.fetchone())[0]

            if rows == 0:
                embed = discord.Embed(
                    title='204',
                    description=f'{suggestion_author.mention} has no suggestions',
                    colour=SBU_GOLD
                )
                await ctx.reply(embed=embed)
                return

            max_page = ceil(rows/10)

            if page > max_page or page < 1:
                embed = discord.Embed(
                    title='Error',
                    description=f'There is no page {page}. Valid pages are between 1 and {max_page}',
                    colour=0xFF0000
                )
                await ctx.reply(embed=embed)
                return

            await cursor.execute(Suggestion.select_rows_with_author_id(suggestion_author.id, page))
            res = await cursor.fetchall()

        embed = discord.Embed(
            title=f'{suggestion_author.name}\'s Suggestions',
            description='',
            colour=SBU_GOLD
        )

        for suggestion_tuple in res:
            suggestion = Suggestion.dict_from_tuple(suggestion_tuple)
            embed.add_field(
                name=f"Suggestion __#{suggestion['suggestion_number']}__",
                value=f"`{suggestion['suggestion']}`\n" +
                      f"*Answered*: {'yes' if suggestion['answered'] else 'no'}\n" +
                      (f"*Approved*: {'yes' if suggestion['approved'] else 'no'}" if suggestion['answered'] else ""),
                inline=False)

        embed.set_footer(text=f'Page: {page}/{max_page}')

        await ctx.reply(embed=embed)

    @ideator.error
    async def ideator_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+suggestion show ideator <@mention | ID: integer> [page: integer]`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        raise exception

    @show.command(name='info', aliases=['details'])
    @commands.cooldown(1, 5)
    async def info(self, ctx: commands.Context, suggestion_id: int):
        async with aiosqlite.connect(Suggestion.DB_PATH + Suggestion.DB_NAME + '.db') as db:
            cursor = await db.cursor()

            await cursor.execute(Suggestion.select_row_with_id(suggestion_id))
            res = await cursor.fetchone()

        if res is None:
            embed = discord.Embed(
                title='Error',
                description='Suggestion not found',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        suggestion = Suggestion.dict_from_tuple(res)

        author = await ctx.bot.get_or_fetch_user(suggestion['author_id'])

        embed = discord.Embed(
            title=f'Suggestion #{suggestion_id}',
            description=suggestion['suggestion'],
            color=SBU_GOLD
        )

        embed.add_field(name='Author', value=author.mention if author else suggestion['author_id'], inline=False)
        embed.add_field(name='Answered', value='Yes' if suggestion['answered'] else 'No', inline=False)
        if suggestion['answered']:
            admin = await ctx.bot.get_or_fetch_user(suggestion['approved_by'])
            embed.add_field(name='Approved', value='Yes' if suggestion['approved'] else 'No', inline=False)
            embed.add_field(name='Approved by' if suggestion['approved'] else 'Denied by',
                            value=admin.mention if admin else suggestion['approved_by'], inline=False)
            embed.add_field(name='Reason', value=str(suggestion['reason']), inline=False)

        embed.set_footer(text=f"Created At: "
                              f"{datetime.datetime.fromtimestamp(suggestion['created_at']).strftime('%y-%m-%d %H:%M')}")

        await ctx.reply(embed=embed)

    @info.error
    async def info_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.BadArgument, commands.MissingRequiredArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+suggestion show info <ID: integer>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        raise exception


def setup(bot):
    bot.add_cog(Suggestions(bot))
