import sqlite3

import discord
from discord.ext import commands

from utils.constants import ADMIN_ROLE_ID, CARRY_SERVICE_REPS_CHANNEL_ID, SBU_LOGO_URL
from utils.error_utils import log_error
from utils.schemas.RepCommandSchema import RepCommand


class Reputations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5)
    async def repgive(self, ctx: commands.Context, receiver: discord.Member, *, comments):
        if ctx.author.id == receiver.id:
            await ctx.send("You can't rep yourself.")
            return

        db = sqlite3.connect(RepCommand.DB_PATH + RepCommand.DB_NAME + '.db')
        cursor = db.cursor()
        cursor.execute(RepCommand.get_max_rep_id())
        rep_id = cursor.fetchone()[0] + 1

        rep = RepCommand(rep_id, receiver.id, ctx.author.id, comments)

        insertion_query = rep.insert()
        cursor.execute(insertion_query[0], insertion_query[1])
        db.commit()

        cursor.execute(RepCommand.count_rows())
        global_reps = cursor.fetchone()[0]

        rep_embed = discord.Embed(
            title='Reputation Given',
            colour=0x8F49EA
        )

        rep_embed.set_author(name=f'Reputation by {ctx.message.author.name}')
        rep_embed.add_field(name='Receiver', value=receiver.mention, inline=True)
        rep_embed.add_field(name='Comments', value=comments, inline=False)
        rep_embed.set_footer(text=f'Global reps given: {global_reps}| Rep ID: {rep_id}')
        rep_embed.set_thumbnail(url=SBU_LOGO_URL)

        message = await ctx.guild \
            .get_channel(CARRY_SERVICE_REPS_CHANNEL_ID) \
            .send(embed=rep_embed)

        cursor.execute(rep.set_message(message.id))

        db.commit()
        db.close()
        await ctx.reply(f"Reputation given to {receiver.name}")

    @repgive.error
    async def repgive_error(self, ctx, exception):
        if isinstance(exception, commands.MissingRequiredArgument) or isinstance(exception, commands.MemberNotFound):
            await ctx.send("Incorrect format. Use `+repgive <@mention> <comments>`")
            return

        raise exception

    @commands.command()
    @commands.has_role(ADMIN_ROLE_ID)
    async def repdel(self, ctx: commands.Context, rep_id: int):

        db = sqlite3.connect(RepCommand.DB_PATH + RepCommand.DB_NAME + '.db')

        cursor = db.cursor()
        cursor.execute(RepCommand.select_row_with_id(rep_id))
        rep_tuple = cursor.fetchone()

        if rep_tuple is None:
            embed = discord.Embed(title='Error',
                                  description=f'Reputation with id {rep_id} not found.',
                                  colour=0xFF0000)
            await ctx.send(embed=embed, delete_after=15)
            await ctx.message.delete(delay=15)
            return

        rep = RepCommand.dict_from_tuple(rep_tuple)

        cursor.execute(RepCommand.delete_row_with_id(rep_id))

        try:
            await ctx.guild \
                .get_channel(CARRY_SERVICE_REPS_CHANNEL_ID) \
                .get_partial_message(rep['message']) \
                .delete()
        except discord.NotFound as exception:
            await log_error(ctx, 'repdel', exception)

        embed = discord.Embed(title=f'Successful Deletion', description=f'Reputation with id {rep_id} removed.',
                              colour=0xFF0000)
        await ctx.send(embed=embed, delete_after=15)
        await ctx.message.delete(delay=15)

        db.commit()
        db.close()

    @repdel.error
    async def repgive_error(self, ctx: commands.Context, exception):
        if isinstance(exception, commands.MissingRequiredArgument) or isinstance(exception, commands.BadArgument):
            message = await ctx.send("Incorrect format. Use `+repdel <rep_id: integer>`")
            await message.delete(delay=15)
            await ctx.message.delete(delay=15)
            return

        raise exception


def setup(bot):
    bot.add_cog(Reputations(bot))
