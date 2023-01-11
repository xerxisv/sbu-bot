import discord
from discord.ui import Button, Select, View

from utils.constants import SBU_GOLD

class info_button(Button):
    def __init__(self, bot, label, description, view, image, row):
        super().__init__(label=label, style=discord.ButtonStyle.blurple, row=row)
        self.bot = bot
        self.description = description
        self.embed_view = view
        self.image = image

    async def callback(self, interaction):
        embed = discord.Embed(title=self.label, description=self.description, color=SBU_GOLD)
        if self.image is not None:
            embed.set_image(url=self.image)

        if self.embed_view is not None:
            view = View(timeout=360.0)
            for component in self.embed_view:
                if component == "dropdown":
                    options = []
                    for option in self.embed_view[component]:
                        options.append(discord.SelectOption(label=option))

                    select = info_select(self.bot, options, self.embed_view[component])

                    view.add_item(select)
                elif component == "button":
                    button = info_button(self.bot, self.embed_view[component]["label"], self.embed_view[component]["description"], self.embed_view[component]["view"])
                    view.add_item(button)
        else:
            view = None

        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

class info_select(Select):
    def __init__(self, bot, options, descriptions):
        super().__init__(options=options, row=4)
        self.bot = bot
        self.descriptions = descriptions

    async def callback(self, interaction):
        embed = discord.Embed(title=self.values[0], description=self.descriptions[self.values[0]]["description"], color=SBU_GOLD)
        embed.set_image(url=self.descriptions[self.values[0]]["image"])
        await interaction.response.edit_message(embed=embed, view=self.view)