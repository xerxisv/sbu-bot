import discord
from discord.ext import commands
from discord.ui import View

from utils.constants import INFO_EMBED_DESCRIPTION, INFO_CHANNEL_ID, BUTTON_STRINGS, ADMIN_ROLE_ID, SBU_GOLD
from utils.components import info_button

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='info', aliases=[], case_insensitive=True)
    @commands.has_role(ADMIN_ROLE_ID)
    async def info(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('info help').invoke(ctx)
            return
        await ctx.trigger_typing()
    
    @info.command(name='load', aliases=['reload'])
    async def load(self, ctx: commands.Context):
        channel = await self.bot.fetch_channel(INFO_CHANNEL_ID)
        if channel.last_message_id is not None:
            message = await channel.fetch_message(channel.last_message_id)
        else:
            message = None
        

        embed = discord.Embed(title="Info", description=INFO_EMBED_DESCRIPTION, color=SBU_GOLD)
        
        view = View()
        i = 0
        j = 0
        for button in BUTTON_STRINGS:
            i += 1
            label = button
            description = BUTTON_STRINGS[button]["description"]
            button_view = BUTTON_STRINGS[button]["view"]
            image = BUTTON_STRINGS[button]["image"]

            view.add_item(info_button(self.bot, label, description, button_view, image, row=j))
            if i == 5:
                i = 0
                j += 1
        
        try:
            if message is not None:
                await message.edit(embed=embed, view=view)
            else: 
                await channel.send(embed=embed, view=view)
        except discord.Forbidden:
            await channel.send(embed=embed, view=view)
        
        await ctx.send("Successfuly reloaded info buttons")

    @info.command(name="unload", aliases=["ul"])
    async def unload(self, ctx: commands.Context):
        channel = await self.bot.fetch_channel(INFO_CHANNEL_ID)
        if channel.last_message_id is not None:
            message = await channel.fetch_message(channel.last_message_id)
        else:
            message = None

        try:
            await message.edit(view=None)
            await ctx.send("Successfuly unloaded info buttons")
        except discord.Forbidden:
            await ctx.send("Failed to unload info buttons")
        
    

def setup(bot):
    bot.add_cog(Info(bot))