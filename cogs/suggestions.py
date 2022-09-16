import datetime
from sqlite3 import connect

import discord
from discord.ext import commands

from utils.constants import ADMIN_ROLE_ID, SBU_LOGO_URL, SUGGESTIONS_CHANNEL_ID
from utils.error_utils import log_error
from utils.schemas.SuggestionSchema import Suggestion


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5)
    async def suggest(self, ctx: commands.Context, *, suggestion_str: str):
        # Fetch new suggestion ID
        db = connect(Suggestion.DB_PATH + Suggestion.DB_NAME + '.db')
        cursor = db.cursor()
        cursor.execute(Suggestion.count_rows())
        suggestion_num = cursor.fetchone()[0]

        # Create embed
        suggestion_embed = discord.Embed(
            title=f'Suggestion',
            description=f'{suggestion_str}',
            timestamp=datetime.datetime.utcnow(),
            colour=0x8F49EA
        )

        # Set author icon if there is one
        if ctx.message.author.avatar is not None:
            suggestion_embed.set_author(name=f'Suggested by {ctx.message.author}', icon_url=ctx.message.author.avatar)
        else:
            suggestion_embed.set_author(name=f'Suggested by {ctx.message.author}')

        suggestion_embed.set_footer(text=f'Suggestion number {suggestion_num}')
        suggestion_embed.set_thumbnail(url=SBU_LOGO_URL)

        channel = self.bot.get_channel(SUGGESTIONS_CHANNEL_ID)
        message = await channel.send(embed=suggestion_embed)

        await ctx.send(f"Suggestion sent to <#{SUGGESTIONS_CHANNEL_ID}>")
        await message.add_reaction('✅')
        await message.add_reaction('❌')

        suggestion = Suggestion(suggestion_num, message.id, suggestion_str, ctx.author.id)

        insertion_tuple = suggestion.insert()
        cursor.execute(insertion_tuple[0], insertion_tuple[1])

        db.commit()
        db.close()

    @suggest.error
    async def on_suggest_error(self, ctx: commands.Context, exception):
        if isinstance(exception, commands.MissingRequiredArgument):
            await ctx.reply('Incorrect format. Use `+suggest <suggestion: text>`')
            return

        raise exception

    @commands.command()
    @commands.has_role(ADMIN_ROLE_ID)
    async def approve(self, ctx: commands.Context, suggestion_id: int, *, reason=None):

        db = connect(Suggestion.DB_PATH + Suggestion.DB_NAME + '.db')
        cursor = db.cursor()

        cursor.execute(Suggestion.select_row_with_id(suggestion_id))
        suggestion_tuple = cursor.fetchone()

        if suggestion_tuple is None:
            await ctx.reply("Suggestion not found.")
            return

        suggestion = Suggestion.dict_from_tuple(suggestion_tuple)

        suggestion_embed = discord.Embed(
            title=f'Approved',
            description=f"{suggestion['suggestion']}",
            timestamp=datetime.datetime.utcnow(),
            colour=0x0CE60C
        )

        suggestion_author: discord.Member = await self.bot.get_or_fetch_user(suggestion['author_id'])
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
            colour=0x0CE60C
        )
        try:
            # Try DMing the user
            await suggestion_author.send(embed=suggestion_embed)
        except (discord.HTTPException, discord.Forbidden, AttributeError):
            # DMing can fail because of: API error, user having DMs closed/ bad intents or suggestion_author is an int
            approved_embed.add_field(name="Direct Message", value=f"User could not be dmed", inline=False)
        except Exception as exception:
            # Any other error will be sent to the logs
            approved_embed.add_field(name="Direct Message", value=f"User could not be dmed", inline=False)
            await log_error(ctx, 'approve', exception)
        else:
            # If no errors occurred send successful message
            approved_embed \
                .add_field(name="Direct Message", value=f"{suggestion_author} dmed successfully", inline=False)
        finally:
            # Send the embed regardless of errors
            await ctx.send(embed=approved_embed)

            set_approved_tuple = Suggestion.set_approved(suggestion_id, True, ctx.author.id, reason)

            cursor.execute(set_approved_tuple[0], set_approved_tuple[1])
            db.commit()

        db.close()
        await ctx.message.delete()

    @approve.error
    async def on_approve_error(self, ctx: commands.Context, exception):
        if isinstance(exception, commands.BadArgument):
            await ctx.reply('Incorrect format. Use `+approve <suggestion_id: integer> [reason: text]`')
            return

        raise exception

    @commands.command()
    @commands.has_role(ADMIN_ROLE_ID)
    async def deny(self, ctx, suggestion_id: int, *, reason=None):
        db = connect(Suggestion.DB_PATH + Suggestion.DB_NAME + '.db')
        cursor = db.cursor()

        cursor.execute(Suggestion.select_row_with_id(suggestion_id))
        suggestion_tuple = cursor.fetchone()

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

        suggestion_author: discord.Member = await self.bot.get_or_fetch_user(suggestion['author_id'])
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
            # DMing can fail because of: API error, user having DMs closed/ bad intents or suggestion_author is an int
            approved_embed.add_field(name="Direct Message", value=f"User could not be dmed", inline=False)
        except Exception as exception:
            # Any other error will be sent to the logs
            approved_embed.add_field(name="Direct Message", value=f"User could not be dmed", inline=False)
            await log_error(ctx, 'deny', exception)

        else:
            # If no errors occurred send successful message
            approved_embed.add_field(name="Direct Message", value=f"{suggestion_author} dmed successfully",
                                     inline=False)
        finally:
            # Send the embed regardless of errors
            await ctx.send(embed=approved_embed)

            set_approved_tuple = Suggestion.set_approved(suggestion_id, True, ctx.author.id, reason)

            cursor.execute(set_approved_tuple[0], set_approved_tuple[1])
            db.commit()

        db.close()
        await ctx.message.delete()

    @deny.error
    async def on_deny_error(self, ctx: commands.Context, exception):
        if isinstance(exception, commands.BadArgument):
            await ctx.reply('Incorrect format. Use `+deny <suggestion_id: integer> [reason: text]`')
            return

        raise exception


def setup(bot):
    bot.add_cog(Suggestions(bot))
