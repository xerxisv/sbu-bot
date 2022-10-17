import discord
from discord.ext import commands
from discord.ui import View, Button

import aiosqlite
import random

from utils.constants import BRIDGE_BOT_IDS, BRIDGE_CHANNEL_IDS, JR_ADMIN_ROLE_ID, ADMIN_ROLE_ID, SBU_GOLD
from utils.database import DBConnection
from utils.database.schemas import User

class GTatsu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db: aiosqlite.Connection = DBConnection().get_db()
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in BRIDGE_BOT_IDS and message.channel.id in BRIDGE_CHANNEL_IDS:
            cursor: aiosqlite.Cursor = await self.db.cursor()
            await cursor.execute(User.select_row_with_ign(message.embeds[0].title))
            user = await cursor.fetchone()
            if user is not None:
                user = User.dict_from_tuple(user)
                tatsu = random.randint(2, 5) + int(user["tatsu_score"])
                await self.db.execute(User.set_tatsu(user["ign"], tatsu))
                await self.db.commit()
            
    
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
        embed.add_field(name="Add gtatsu", value="`gtatsu add <IGN> <tatsu>`", inline=False)
        embed.add_field(name="Remove gtatsu", value="`gtatsu remove <IGN> <tatsu>`", inline=False)
        embed.add_field(name="Set gtatsu", value="`gtatsu set <IGN> <tatsu>`", inline=False)
    
        await ctx.reply(embed=embed)
    
    @gtatsu.command(name="set")
    @commands.has_role(JR_ADMIN_ROLE_ID)
    async def set_(self, ctx, ign: str, tatsu: int):
        await self.db.execute(User.set_tatsu(ign, tatsu))

        await ctx.reply(f"{ign} now has {tatsu} gtatsu")
    
    @gtatsu.command(name="add")
    @commands.has_role(JR_ADMIN_ROLE_ID)
    async def add(self, ctx, ign: str, tatsu: int):
        cursor: aiosqlite.Cursor = await self.db.cursor()
        await cursor.execute(User.select_row_with_ign(message.embeds[0].title))
        user = await cursor.fetchone()
        user = User.dict_from_tuple(user)
        tatsu = tatsu + user["tatsu_score"]

        await self.db.execute(User.set_tatsu(ign, tatsu))
        await self.db.commit()

        await ctx.reply(f"{ign} now has {tatsu} gtatsu")
    

    @gtatsu.command(name="remove")
    @commands.has_role(JR_ADMIN_ROLE_ID)
    async def remove(self, ctx, ign: str, tatsu: int):
        cursor: aiosqlite.Cursor = await self.db.cursor()
        await cursor.execute(User.select_row_with_ign(message.embeds[0].title))
        user = await cursor.fetchone()
        user = User.dict_from_tuple(user)
        tatsu = tatsu - user["tatsu_score"]

        await self.db.execute(User.set_tatsu(ign, tatsu))
        await self.db.commit()

        await ctx.reply(f"{ign} now has {tatsu} gtatsu")
        
    @gtatsu.command(name="rank", aliases=["r"])
    async def rank(self, ctx, ign=None):
        cursor: aiosqlite.Cursor = await self.db.cursor()
        if ign is None:
            await cursor.execute(User.select_row_with_id(ctx.author.id))
            user = await cursor.fetchone()
            user = User.dict_from_tuple(user)
            ign = user["ign"]
        else:
            await cursor.execute(User.select_row_with_ign(ign))
            user = await cursor.fetchone()
            user = User.dict_from_tuple(user)
        
        tatsu = user["tatsu_score"]
        await ctx.reply(f"{ign}'s gtatsu: {tatsu}")
    
    @gtatsu.command(name="leaderboard", aliases=["l"])
    async def leaderboard(self, ctx):
        cursor: aiosqlite.Cursor = await self.db.cursor()
        await cursor.execute(User.select_top_tatsu())
        users = await cursor.fetchall()
        users = users[:10]
        temp = []
        for user in users:
            user = User.dict_from_tuple(user)
            temp.append(user)
        users = temp

        top_weekly=[]
        for u in users:
            top = {
                "this_week_tatsu_score": 0
            }
            for user in users:
                if user in top_weekly:
                    continue
                if user["this_week_tatsu_score"] >= top["this_week_tatsu_score"]:
                    top = user
            top_weekly.append(top)
            

        embed = discord.Embed(title="GTatsu Leaderboard", color=SBU_GOLD)

        for user in users:
            ign = user["ign"]
            tatsu = user["tatsu_score"]
            weekly_tatsu = user["tatsu_score"] - user["weekly_tatsu_score"]
            embed.add_field(name=ign, value=f"**Total GTatsu:** {tatsu}  |  **Weekly GTatsu:** {weekly_tatsu}", inline=False)
        
        view = leaderboard_view(users, top_weekly, True)

        await ctx.reply(embed=embed, view = view)

    @gtatsu.command()
    @commands.has_role(ADMIN_ROLE_ID)
    async def update_tables(self, ctx):
        await self.db.execute('''ALTER TABLE "USERS" ADD COLUMN "last_week_tatsu" INTEGER DEFAULT 0''')
        await self.db.commit()

class leaderboard_view(View):
    def __init__(self, top_total, top_weekly, total_disabled):
        super().__init__(timeout=None)
        self.add_item(total_button(top_total, top_weekly, total_disabled))
        self.add_item(weekly_button(top_total, top_weekly, total_disabled))

class total_button(Button):
    def __init__(self, top_total, top_weekly, total_disabled):
        super().__init__(label="Total", style=discord.ButtonStyle.blurple, disabled=total_disabled)
        self.top_total = top_total
        self.top_weekly = top_weekly
        self.total_diabled = total_disabled
    async def callback(self, interaction):
        embed = discord.Embed(title="GTatsu Leaderboard", color=SBU_GOLD)

        for user in self.top_total:
            ign = user["ign"]
            tatsu = user["tatsu_score"]
            weekly_tatsu = user["tatsu_score"] - user["weekly_tatsu_score"]
            embed.add_field(name=ign, value=f"**Total GTatsu:** {tatsu}  |  **Weekly GTatsu:** {weekly_tatsu}", inline=False)
        
        view = leaderboard_view(self.top_total, self.top_weekly, not self.total_diabled)

        await interaction.response.edit_message(embed=embed, view=view)

class weekly_button(Button):
    def __init__(self, top_total, top_weekly, total_disabled):
        super().__init__(label="Weekly", style=discord.ButtonStyle.blurple, disabled=not total_disabled)
        self.top_total = top_total
        self.top_weekly = top_weekly
        self.total_diabled = total_disabled
    async def callback(self, interaction):
        embed = discord.Embed(title="GTatsu Leaderboard", color=SBU_GOLD)

        for user in self.top_weekly:
            ign = user["ign"]
            tatsu = user["tatsu_score"]
            weekly_tatsu = user["tatsu_score"] - user["weekly_tatsu_score"]
            embed.add_field(name=ign, value=f"**Weekly GTatsu:** {weekly_tatsu}  |  **Total GTatsu:** {tatsu}", inline=False)
        
        view = leaderboard_view(self.top_total, self.top_weekly, not self.total_diabled)

        await interaction.response.edit_message(embed=embed, view=view)
    


    
def setup(bot):
    bot.add_cog(GTatsu(bot))