import discord
from discord.ext import commands
from discord.ui import View, Button, Select

import aiosqlite

from utils.constants import GUILDS_INFO, JR_ADMIN_ROLE_ID, SBU_GOLD
from utils.database import DBConnection
from utils.database.schemas import User


class GTatsu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db: aiosqlite.Connection = DBConnection().get_db()

    @commands.group(name="gtatsu", aliases=["gt"])
    async def gtatsu(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('gtatsu help').invoke(ctx)
            return
        await ctx.trigger_typing()

    @gtatsu.command(name="help", aliases=["commands"])
    async def help(self, ctx):
        embed = discord.Embed(
            title='Command help',
            colour=SBU_GOLD
        )

        embed.add_field(name="Check your gtatsu", value="`gtatsu rank <IGN>`", inline=False)
        embed.add_field(name="Add gtatsu", value="`gtatsu add <IGN> <tatsu>`\n"
                                                 "*__Jr. Admin__ command*", inline=False)
        embed.add_field(name="Remove gtatsu", value="`gtatsu remove <IGN> <tatsu>`\n"
                                                    "*__Jr. Admin__ command*", inline=False)
        embed.add_field(name="Set gtatsu", value="`gtatsu set <IGN> <tatsu>`\n"
                                                 "*__Jr. Admin__ command*", inline=False)
    
        await ctx.reply(embed=embed)
    
    @gtatsu.command(name="set")
    @commands.has_role(JR_ADMIN_ROLE_ID)
    async def set_(self, ctx, ign: str, tatsu: int):
        await self.db.execute(User.set_tatsu(ign, tatsu))

        embed = discord.Embed(
            title='Success',
            description=f'{ign} now has {tatsu} gtatsu',
            colour=0x00FF00
        )
        await ctx.reply(embed=embed)

    @set_.error
    async def set_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.MissingRequiredArgument, commands.BadArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+gtatsu set <IGN> <amount>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

    @gtatsu.command(name="add")
    @commands.has_role(JR_ADMIN_ROLE_ID)
    async def add(self, ctx, ign: str, tatsu: int):
        await self.db.execute(User.add_to_tatsu_static(ign, tatsu))
        await self.db.commit()

        embed = discord.Embed(
            title='Success',
            description=f'{tatsu} gtatsu points added to {ign}',
            colour=0x00FF00
        )
        await ctx.reply(embed=embed)

    @add.error
    async def add_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.MissingRequiredArgument, commands.BadArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+gtatsu add <IGN> <amount>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

    @gtatsu.command(name="remove")
    @commands.has_role(JR_ADMIN_ROLE_ID)
    async def remove(self, ctx, ign: str, tatsu: int):
        await self.db.execute(User.add_to_tatsu_static(ign, -tatsu))
        await self.db.commit()

        embed = discord.Embed(
            title='Success',
            description=f'{tatsu} gtatsu points removed from {ign}',
            colour=0x00FF00
        )
        await ctx.reply(embed=embed)

    @remove.error
    async def remove_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.MissingRequiredArgument, commands.BadArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+gtatsu remove <IGN> <amount>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

    @gtatsu.command(name='modifier')
    @commands.has_role(JR_ADMIN_ROLE_ID)
    async def modifier(self, ctx: commands.Context, ign: str, modifier: float):
        await self.db.execute(User.set_modifier(ign, modifier))
        await self.db.commit()

        embed = discord.Embed(
            title='Success',
            description=f'{ign}\'s modifier has been set to {modifier}',
            colour=0x00FF00
        )
        await ctx.reply(embed=embed)

    @modifier.error
    async def modifier_error(self, ctx: commands.Context, exception: Exception):
        if isinstance(exception, (commands.MissingRequiredArgument, commands.BadArgument)):
            embed = discord.Embed(
                title='Error',
                description='Invalid format. Use `+gtatsu modifier <IGN> <modifier>`',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

    @gtatsu.command(name="rank", aliases=["r"])
    async def rank(self, ctx: commands.Context, ign: str = None):
        cursor: aiosqlite.Cursor = await self.db.cursor()
        if ign is None:
            await cursor.execute(User.select_row_with_id(ctx.author.id))
            res = await cursor.fetchone()
        else:
            await cursor.execute(User.select_row_with_ign(ign))
            res = await cursor.fetchone()

        if res is None:
            embed = discord.Embed(
                title='Error',
                description=f'User with IGN `{ign}` not found.',
                colour=0xFF0000
            )
            await ctx.reply(embed=embed)
            return

        user = User.dict_from_tuple(res)
        ign = user["ign"] + ("'s" if not user['ign'].endswith('s') else '')

        embed = discord.Embed(
            title=f'{ign} GTatsu Score',
            description=f"All time: {user['tatsu_score']}\nThis week: {user['weekly_tatsu_score']}",
            colour=SBU_GOLD
        )
        await ctx.reply(embed=embed)
    
    @gtatsu.command(name="leaderboard", aliases=["l"])
    async def leaderboard(self, ctx: commands.Context):

        users = await get_users('Global', True)

        embed = discord.Embed(title='Global GTatsu Leaderboard', color=SBU_GOLD)

        for user in users:
            embed.add_field(name=user['ign'],
                            value=f"*Weekly GTatsu:* **{user['tatsu_score'] - user['weekly_tatsu_score']}**",
                            inline=False)
        if len(users) < 1:
            embed.description = "Nothing to display"

        view = LeaderboardView('Global', False)

        await ctx.reply(embed=embed, view=view)


class LeaderboardView(View):
    def __init__(self, guild: str, total_disabled: bool):
        super().__init__(timeout=120, disable_on_timeout=True)
        self.add_item(TotalButton(guild, total_disabled))
        self.add_item(WeeklyButton(guild, total_disabled))
        self.add_item(SisterhoodSelectionMenu(guild, total_disabled))


class TotalButton(Button):
    def __init__(self, guild: str, total_disabled):
        super().__init__(label="Total", style=discord.ButtonStyle.blurple, disabled=total_disabled)
        self.guild = guild
        self.total_disabled = total_disabled

    async def callback(self, interaction):
        embed = discord.Embed(title=f'{self.guild} GTatsu Leaderboard', color=SBU_GOLD)

        users = await get_users(self.guild, False)
        if len(users) < 1:
            embed = discord.Embed(title=f'{self.guild} GTatsu Leaderboard',
                                  description='Nothing to display',
                                  color=SBU_GOLD)

            view = LeaderboardView(self.guild, not self.total_disabled)
            await interaction.response.edit_message(embed=embed, view=view)
            return

        for user in users:
            embed.add_field(name=user["ign"], value=f"*Total GTatsu:* **{user['tatsu_score']}**",
                            inline=False)

        view = LeaderboardView(self.guild, not self.total_disabled)
        await interaction.response.edit_message(embed=embed, view=view)


class WeeklyButton(Button):
    def __init__(self, guild: str, total_disabled):
        super().__init__(label="Weekly", style=discord.ButtonStyle.blurple, disabled=not total_disabled)
        self.guild = guild
        self.total_disabled = total_disabled

    async def callback(self, interaction):
        embed = discord.Embed(title=f'{self.guild} GTatsu Leaderboard', color=SBU_GOLD)

        users = await get_users(self.guild, True)
        if len(users) < 1:
            embed = discord.Embed(title=f'{self.guild} GTatsu Leaderboard',
                                  description='Nothing to display',
                                  color=SBU_GOLD)

            view = LeaderboardView(self.guild, not self.total_disabled)
            await interaction.response.edit_message(embed=embed, view=view)
            return

        for user in users:
            embed.add_field(name=user['ign'],
                            value=f"*Weekly GTatsu:* **{user['tatsu_score'] - user['weekly_tatsu_score']}**",
                            inline=False)

        view = LeaderboardView(self.guild, not self.total_disabled)
        await interaction.response.edit_message(embed=embed, view=view)


class SisterhoodSelectionMenu(Select):
    def __init__(self, guild, total_disabled):
        super().__init__(placeholder='Select Guild',
                         options=[
                             discord.SelectOption(label='Global', default=guild == 'Global'),
                             discord.SelectOption(label='SB University', default=guild == 'SB Uni'),
                             discord.SelectOption(label='SB Alpha Psi', default=guild == 'SB Alpha Psi'),
                             discord.SelectOption(label='SB Lambda Pi', default=guild == 'SB Lambda Pi'),
                             discord.SelectOption(label='SB Masters', default=guild == 'SB Masters'),
                         ])
        self.guild = guild
        self.total_disabled = total_disabled

    async def callback(self, interaction):
        embed = discord.Embed(title=f'{self.values[0]} GTatsu Leaderboard', color=SBU_GOLD)

        users = await get_users(self.values[0], not self.total_disabled)
        if len(users) < 1:
            embed = discord.Embed(title=f'{self.values[0]} GTatsu Leaderboard',
                                  description='Nothing to display',
                                  color=SBU_GOLD)

            view = LeaderboardView(self.values[0], self.total_disabled)
            await interaction.response.edit_message(embed=embed, view=view)
            return

        for user in users:
            embed.add_field(name=user['ign'],
                            value=f"*Total GTatsu:* **{user['tatsu_score']}**" if self.total_disabled else
                            f"*Weekly GTatsu:* **{user['tatsu_score'] - user['weekly_tatsu_score']}**",
                            inline=False)

        view = LeaderboardView(self.values[0], self.total_disabled)
        await interaction.response.edit_message(embed=embed, view=view)


async def get_users(guild: str, weekly: bool):
    cursor: aiosqlite.Cursor = await DBConnection().get_db().cursor()
    await cursor.execute(User.select_top_tatsu(None if guild == 'Global' else GUILDS_INFO[guild.upper()]['guild_uuid'],
                                               weekly))
    users = await cursor.fetchall()

    return [User.dict_from_tuple(user) for user in users]


def setup(bot):
    bot.add_cog(GTatsu(bot))
