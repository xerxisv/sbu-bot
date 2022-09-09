import discord
from discord.ext import commands
import json
import requests
import time
import dotenv
import os

class AutomaticTutoringSystem(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    key = os.getenv("apikey")
    
    placeholder = 'This section is not ready yet. Thank you for your patience.'
    @bot.command()
    async def autotutor(ctx):
        author = ctx.message.author
        print(f'Command ran by {author} at {date.now()}')
        bazaardata = rq.get("https://sky.shiiyu.moe/api/v2/bazaar").json()
        embed = discord.Embed(title='Auto-Tutor',description='',colour=discord.Color.blue())
        disc = """
        Welcome to the Auto-Tutor, also known as the automatic tutoring system.

        This bot will answer basic and semi-complex questions by answering with articles and guides written by pros who know what they are doing.

        To start please select a catagory to get to the answer you are looking for
        """
        embed.add_field(name="Welcome",value=disc,inline=False)
        message = await ctx.send(embed=embed)
        channel = message.channel
        embed = discord.Embed(title='Main Catagories',description='',colour=discord.Color.blue())
        disc = """
        __Skills__: Information on skills and best practices for grinding experience
        __Dungeons__: Information on dungeon gear for each floor as well as detailed descriptions for each boss and their attacks
        __Slayers__: Information on Slayer Gear for each slayer as well as detailed descriptions for each slayer and their attacks
        __Money Making__: Information on best ways to make money for each stage of the game
        __Other__: Miscellaneous information regarding the game
        """
        embed.add_field(name='Options',value=disc,inline=False)
        embed.set_footer(text='Type in the name of the section you would like to explore')
        await ctx.send(embed=embed)
        def check(m):
            return m.content.lower() in ['skills','dungeons','slayers','money making','other'] and m.channel == channel
        msg = await bot.wait_for('message', check=check)
        if msg.content.lower() == 'skills':
            embed = discord.Embed(title='Skill Catagories',description='',colour=discord.Color.blue())
            disc = """
            __Select a skill below to choose which skill to view information__

            Farming
            Mining
            Combat
            Foraging
            Fishing
            Enchanting
            Alchemy
            Taming
            """
            embed.add_field(name='Options',value=disc,inline=False)
            embed.set_footer(text='Type in the name of the section you would like to explore')
            await ctx.send(embed=embed)
            def check(m):
                return m.content.lower() == 'farming' or m.content.lower() == 'mining' or m.content.lower() == 'combat' or m.content.lower() == 'foraging' or m.content.lower() == 'fishing' or m.content.lower() == 'enchanting' or m.content.lower() == 'alchemy' or m.content.lower() == 'taming' and m.channel == channel
            msg = await bot.wait_for('message', check=check)
            if msg.content.lower() == 'farming':
                embed = discord.Embed(title='Farming Catagories',description='',colour=discord.Color.blue())
                disc = """
                __Select a farming catagory to view information__

                Experience
                Farm Layouts
                Farming Contests
                Locations
                """
                embed.add_field(name='Options',value=disc,inline=False)
                embed.set_footer(text='Type in the name of the section you would like to explore')
                await ctx.send(embed=embed)
                def check(m):
                    return m.content.lower() == 'experience' or m.content.lower() == 'farm layouts' or m.content.lower() == 'farming contests' or m.content.lower() == 'locations' and m.channel == channel
                msg = await bot.wait_for('message', check=check)
                if msg.content.lower() == 'experience':
                    embed = discord.Embed(title='Farming Experience',description='This is a guide on the most common and efficient ways to gain farming experience',colour=discord.Color.blue())
                    disc = """
                    The best way to gain farming xp is a maxed out setup farming pumpkins. Pumpkins provide a base xp of 4.5 xp per pumpkin, the highest out of all crops. For the best pumpkin farming layout see the "Farming Layouts" catagory.

                    The best way to farm pumpkin is to utilize the various stat boosts of items
                    1) Pumpkin Dicer with the Blessed reforge(Blessed Fruit) applied to it - Provides a +4/5 Farming Wisdom bonus depending on the rarity of the Pumpkin Dicer
                    2) Level 100 Epic/Legendary Rabbit Pet - Provides a +30 Farming Wisdom bonus
                    3) Farming XP Boost III Potion - Provides a +20 Farming Wisdom bonus
                    4) Booster Cookie - Provides a +25 Farming Wisdom bonus
                    """
                    disc1 = """
                    Sugarcane is also a common crop often farmed for farming xp. While it does give less farming xp compared to pumpkins, it makes up for that by making alot more money. For the best Sugarcane layout see the "Farming Layouts" catagory.

                    The best way to farm sugarcane is to utilize the various stat boosts of items
                    1) Turing Sugarcane Hoe with the Blessed reforge(Blessed Fruit) applied to it - Provides a + 1/2/3/4/5/6 Farming Wisdom bonus depending on the rarity of the Hoe
                    2) Level 100 Epic/Legendary Rabbit Pet - Provides a +30 Farming Wisdom bonus
                    3) Farming XP Boost III Potion - Provides a +20 Farming Wisdom bonus
                    4) Booster Cookie - Provides a +25 Farming Wisdom bonus
                    """
                    disc2 = """
                    -Any farming tool with the blessed reforge provides a farming xp boost, based on the items rarity
                    -While both Epic and Legendary varients of the Rabbit pet provides a 30% xp boost, the Epic varient levels up faster and is cheaper to buy
                    -A God Potion will achieve the same effects as a Farming XP Boost III Potion
                    -The Booster Cookie provides a 20% bonus to all skills
                    -While the setups listed here are for late game players, it is recomended that players looking to farm for xp do so by buying items that provide more of an xp bonus, making their way to the items that provide less of a bonus
                    """
                    embed.add_field(name='Pumpkins',value=disc,inline=False)
                    embed.add_field(name='Sugarcane',value=disc1,inline=False)
                    embed.add_field(name='Side Notes',value=disc2,inline=False)
                    embed.set_footer(text="Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki",icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 'farm layouts':
                    embed = discord.Embed(title='Farm Layouts',description='',colour=discord.Color.blue())
                    disc = """
                    Wheat
                    Carrot
                    Potato
                    Pumpkin
                    Melon
                    Mushroom
                    Cactus
                    Sugarcane
                    Netherwart
                    Cocoa Beans
                    """
                    embed.add_field(name='Select a crop to view the best layout',value=disc,inline=False)
                    embed.set_footer(text='Type in the name of the section you would like to explore')
                    await ctx.send(embed=embed)
                    def check(m):
                        return m.content.lower() == 'wheat' or m.content.lower() == 'carrot' or m.content.lower() == 'potato' or m.content.lower() == 'pumpkin' or m.content.lower() == 'melon' or m.content.lower() == 'mushroom' or m.content.lower() == 'cactus' or m.content.lower() == 'sugarcane' or m.content.lower() == 'netherwart' or m.content.lower() == 'cocoa beans' and m.channel == channel
                    msg = await bot.wait_for('message', check=check)
                    if msg.content.lower() == 'wheat':
                        embed = discord.Embed(title='Wheat farm layout',description='',colour=discord.Color.blue())
                        disc = """
                        For a horizontal wheat farm the optimal method is a row of water with a light source block directly on top (Such as Sea Lanterns or Glowstone Blocks) followed by 8 rows of tilled dirt repeating till the end of your Private Island. 3 layers of wheat with the first Island size upgrade is considered infinite.\n\nhttps://imgur.com/WE68wf0
                        """
                        disc1 = """
                        For a vertical wheat farm stack 3 or 4 rows of wheat and one row of water with a light source block directly on top (Such as Sea Lanterns or Glowstone Blocks) per layer, with 2-3 blocks between each layer.\n

                        https://imgur.com/DNV2jt0
                        """
                        embed.add_field(name='Horizontal',value=disc,inline=False)
                        embed.add_field(name='Vertical',value=disc1,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'carrot':
                        embed = discord.Embed(title='Carrot farm layout',description='',colour=discord.Color.blue())
                        disc = """
                        For a horizontal carrot farm the optimal method is a row of water with a light source block directly on top (Such as Sea Lanterns or Glowstone Blocks) followed by 8 rows of tilled dirt repeating till the end of your Private Island. 3 layers of carrot with the first Island size upgrade is considered infinite.

                        https://imgur.com/f65cfsE

                        """
                        disc1 = """
                        For a vertical carrot farm stack 3 or 4 rows of carrot and one row of water with a light source block directly on top (Such as Sea Lanterns or Glowstone Blocks) per layer, with 2-3 blocks between each layer.

                        https://imgur.com/wX4kQXS
                        """
                        embed.add_field(name='Horizontal',value=disc,inline=False)
                        embed.add_field(name='Vertical',value=disc1,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'potato':
                        embed = discord.Embed(title='Potato farm layout',description='',colour=discord.Color.blue())
                        disc = """
                        For a horizontal potato farm the optimal method is a row of water with a light source block directly on top (Such as Sea Lanterns or Glowstone Blocks) followed by 8 rows of tilled dirt repeating till the end of your Private Island. 3 layers of potato with the first Island size upgrade is considered infinite.



                        """
                        disc1 = """
                        For a vertical potato farm stack 3 or 4 rows of potato and one row of water with a light source block directly on top (Such as Sea Lanterns or Glowstone Blocks) per layer, with 2-3 blocks between each layer.


                        """
                        embed.add_field(name='Horizontal',value=disc,inline=False)
                        embed.add_field(name='Vertical',value=disc1,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'pumpkin':
                        embed = discord.Embed(title='Pumpkin farm layout',description='',colour=discord.Color.blue())
                        disc = """
                        Horizontal Pumpkin farms have 2 options, with and without water. If you plan to use water then the pattern you will have to follow is a row of water followed by a row of tilled dirt then 2 rows of untilled dirt then 2 rows of tilled dirt then 2 rows of untilled dirt then a row of tilled dirt repeating. All rows with tilled dirt on them should have slabs or light source blocks (Such as Sea Lanterns or Glowstone Blocks) as pumpkin stems require light to grow and grow pumpkins. for a farm without water, you will have to follow the pattern of tilled dirt and 2 rows of untilled dirt repeating. 3 layers of pumpkin with water and 4 layers without water are considered infinite



                        """
                        disc1 = """
                        For a veritcal pumpkin farm using water would be the most efficient method. So use one row of water followed by one row of tilled dirt, 2 rows of untilled dirt, and another row of tilled dirt, stacked on top of each other with 2-3 blocks between each layer.


                        """
                        embed.add_field(name='Horizontal',value=disc,inline=False)
                        embed.add_field(name='Vertical',value=disc1,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'melon':
                        embed = discord.Embed(title='Melon farm layout',description='',colour=discord.Color.blue())
                        disc = """
                        Horizontal Melon farms have 2 options, with and without water. If you plan to use water then the pattern you will have to follow is a row of water followed by a row of tilled dirt then 2 rows of untilled dirt then 2 rows of tilled dirt then 2 rows of untilled dirt then a row of tilled dirt repeating. All rows with tilled dirt on them should have slabs or light source blocks (Such as Sea Lanterns or Glowstone Blocks) as melon stems require light to grow and grow pumpkins. For a farm without water, you will have to follow the pattern of tilled dirt and 2 rows of untilled dirt repeating. 3 layers of melon with water and 4 layers without water are considered infinite



                        """
                        disc1 = """
                        For a veritcal melon farm using water would be the most efficient method. So use one row of water followed by one row of tilled dirt, 2 rows of untilled dirt, and another row of tilled dirt, stacked on top of each other with 2-3 blocks between each layer.


                        """
                        embed.add_field(name='Horizontal',value=disc,inline=False)
                        embed.add_field(name='Vertical',value=disc1,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'mushroom':
                        embed = discord.Embed(title='Mushroom farm layout',description='',colour=discord.Color.blue())
                        disc = """
                        Because mushroom dosen't grow, there are 2 methods people use to farm it. The first method involves making a giant slab of mycellium and using mushroom minions to fill the slab with mushrooms then farming those mushrooms. Because this is a one time use farm it was mainly used for contests. A much better method is using a Mooshroom Cow Pet while farming another crop such as Sugarcane.


                        """
                        disc1 = """
                        For the same reasons as the horizontal farm, vertical mushroom farms are not recomended.


                        """
                        embed.add_field(name='Horizontal',value=disc,inline=False)
                        embed.add_field(name='Vertical',value=disc1,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'cactus':
                        embed = discord.Embed(title='Cactus farm layout',description='',colour=discord.Color.blue())
                        disc = """
                        For a horizontal cactus farm you first want a slab of sand. Then you want a row of divider blocks, an empty row, 4 rows of cactus (Cactus can't be placed next to any block, including itself, so the cactus will have to be placed in a checkerboard pattern), and another empty row. Cactus is only farmed for gold medals so 2/3 of a layer is enough.


                        """
                        disc1 = """
                        Vertical Cactus farms are not recomended.


                        """
                        embed.add_field(name='Horizontal',value=disc,inline=False)
                        embed.add_field(name='Vertical',value=disc1,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'sugarcane':
                        embed = discord.Embed(title='Sugarcane farm layout',description='',colour=discord.Color.blue())
                        disc = """
                        For a horizontal sugarcane farm you will need 1 row of water with a divider block on top and rows of sugarcane repeating. 3 layers of sugarcane is considered infinite. Sugarcane can only be placed next to water so take that into consideration when making your farm



                        """
                        disc1 = """
                        For a vertical sugarcane farm you want a row of water, 2 rows of sugarcane, and another row of water.


                        """
                        embed.add_field(name='Horizontal',value=disc,inline=False)
                        embed.add_field(name='Vertical',value=disc1,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'netherwart':
                        embed = discord.Embed(title='Netherwart farm layout',description='',colour=discord.Color.blue())
                        disc = """
                        For a horizontal netherwart farm you want 6 rows of soul sand and netherwart followed by a gap of air to fly in. 3 layers of netherwart is considered infinite.


                        """
                        disc1 = """
                        For a vertical netherwart farm, 4 rows of soulsand and netherwart with 2 with a block between each layer.


                        """
                        embed.add_field(name='Horizontal',value=disc,inline=False)
                        embed.add_field(name='Vertical',value=disc1,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'cocoa beans':
                        embed = discord.Embed(title='Cocoa Bean farm layout',description='',colour=discord.Color.blue())
                        disc = """
                        For a horizontal cocoa bean farm you want a row of light source blocks (Such as Sea Lanterns or Glowstone Blocks) and 2 empty rows. On top of the light source block place any divider block and on top of that place 4 Jungle Logs. On each side of the Jungle Logs place your Cocoa Beans.



                        """
                        disc1 = """
                        Vertical cocoa bean farms are not recomended.
                        """
                        embed.add_field(name='Horizontal',value=disc,inline=False)
                        embed.add_field(name='Vertical',value=disc1,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                elif msg.content.lower() == 'farming contests':
                    embed = discord.Embed(title="Jacob's Farming Contests",description="The Jacob's Farming Contests are events that occur every 3 minecraft days, or once every real life hour at XX:15 or XX:45 depending on your time zone, and last for 20 minutes. Each event randomly selects 3 crops in which people can compete for medals. People compete in contests by gaining collection of the crop farmed. These medals can be spent at an NPC called Anita, who sells farming items and farming perks that can be useful in gaining higher tier medals",colour=discord.Color.blue())
                    disc = """
                    As decribed above, each contest occurs once every hour, and it lasts 20 minutes. The 3 crops are randomly selected for each contest out of the 10 available crops. You can view what crops the next context is going to include on the calender in game.
                    """
                    disc1 = """
                    Jacobs Tickets are a form or currency used to buy things at Anita, the farm shop NPC. These are earned from contests or can be bought on the bazaar.

                    Tickets are earned based on the medal you get in each contest:
                    __No Medal__: 1 Ticket
                    __Bronze Medal__: 10 Tickets
                    __Silver Medal__: 15 Tickets
                    __Gold Medal__: 25 Tickets
                    """
                    disc2 = f"""
                    Medals are the main thing that people go for when grinding Jacob's Contests.

                    Jacob's Contests are contests after all, and so obtaining medals is a competition. This is how which medal you get is determined:
                    __Bronze Medal__: Place in the top 60% of players
                    __Silver Medal__: Place in the top 25% of players
                    __Gold Medal__: Place in the top 5% of players
                    Your placement in a contest is determined by the amount of crops you are able to farm during the 20 minute time period.

                    Medals can also be taded into other tiers of Medals and tickets:
                    2 Bronze Medals ⇌ 1 Silver Medal
                    4 Silver Medals ⇌ 1 Gold Medals
                    1 Bronze Medal > 1 Ticket
                    1 Silver Medal > 2 Tickets
                    1 Gold Medal > 8 Tickets

                    The current price of tickets on the bazaar is `{bazaardata['JACOBS_TICKET']['buyPrice']}` coins
                    """
                    disc3 = """
                    Anita is the NPC on the second floor of the Farmhouse. She sells Farming Items and Farming Perks that can help with gaining higher tier medals.
                    A short list of what Anita sells includes:
                    Farm Buidling items
                    Farming Tools for each and every crops
                    Perks to increase the Farming Level Cap from 50 to 60 and to increase crop drop rates
                    """
                    embed.add_field(name='Contests',value=disc,inline=False)
                    embed.add_field(name="Jacob's Tickets",value=disc1,inline=False)
                    embed.add_field(name='Medals',value=disc2,inline=False)
                    embed.add_field(name='Anita',value=disc3,inline=False)
                    embed.set_footer(text='Written by plebmaster21#0101',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                    await ctx.send(embed=embed)
            elif msg.content.lower() == 'mining':
                embed = discord.Embed(title='Mining Catagories',description='',colour=discord.Color.blue())
                disc = """
                __Select a mining catagory to view information__

                Experience
                Locations
                Crystal Hollows
                Events
                HOTM
                Gemstones
                """
                embed.add_field(name='Options',value=disc,inline=False)
                embed.set_footer(text='Type in the name of the section you would like to explore')
                await ctx.send(embed=embed)
                def check(m):
                    return m.content.lower() == 'experience' or m.content.lower() == 'locations' or m.content.lower() == 'crystal hollows' or m.content.lower() == 'events' or m.content.lower() == 'hotm' or m.content.lower() == 'gemstones' and m.channel == channel
                msg = await bot.wait_for('message', check=check)
                if msg.content.lower() == 'experience':
                    embed = discord.Embed(title='Mining Experience',description='This is a guide on the most common and efficient ways to gain mining experience',colour=discord.Color.blue())
                    disc = """
                    There are multiple ores in the game when it comes to mining, but the 2 that stand on top are Mithril and Gemstones giving a base xp of 45 and 70 respectively.

                    If you are going to use Mithril as your source of mining xp be sure to only mine the gray wool varient. All the mithril varients found in the Dwarven Mines have different breaking powers, but all of them offer the same amount of xp. Since the gray wool varient has the lowest breaking power it would be the most efficient choice for xp.

                    If you are going to use Gemstones as your source of mining xp be sure to only mine Ruby Gemstones. All the gemstone varients found in the Crystal Hollows have different breaking powers, but all of them offer the same amount of xp. Since Ruby Gemstones has the lowest breaking power it would be the most efficient choice for xp.
                    """
                    disc1 = """
                    1) Level 100 Epic/Legendary Silverfish Pet - Provides a +30 Mining Wisdom bonus
                    2) Compact Enchantment - +1 per level of Compact up to +10
                    3) Booster Cookie - Provides a +25 Mining Wisdom bonus
                    4) Mining XP Boost III Potion - Provides a +20 Mining Wisdom bonus
                    5) Refined Reforge - Grants +1/2/3/4/5/6/7/8/9 bonus Mining Wisdom based on the rarity of the items
                    6) Mayor Cole - Provides a +50 Mining Wisdom bonus if he has the Mining XP Buff perk in the elected year
                    """
                    disc2 = """
                    -While both Epic and Legendary varients of the Silverfish pet provides a 30% xp boost, the Epic varient levels up faster and is cheaper to buy
                    -A God Potion will achieve the same effects as a Mining XP Boost III Potion
                    -The Booster Cookie provides a 20% bonus to all skills
                    -While the setups listed here are for late game players, it is recomended that players looking to mine for xp do so by buying items that provide more of an xp bonus, making their way to the items that provide less of a bonus
                    -While the Refined reforge provides a mining xp boost, it is not recomended to use as a reforge on one's mining tools
                    """
                    embed.add_field(name='Ores',value=disc,inline=False)
                    embed.add_field(name='XP Boosts',value=disc1,inline=False)
                    embed.add_field(name='Side Notes',value=disc2,inline=False)
                    embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 'locations':
                    embed = discord.Embed(title='Mining Locations',description='',colour=discord.Color.blue())
                    hotm1 = (bazaardata['ENCHANTED_COAL']['buyPrice']*10) + ((bazaardata['ENCHANTED_REDSTONE']['buyPrice']*10)) + (bazaardata['ENCHANTED_LAPIS_LAZULI']['buyPrice']*10)
                    disc = """
                    The Coal Mine is the first Mining Location. It is located on the Hub Island. There you can mine cobblestone and coal. This location has no requirements.
                    """
                    disc1 = """
                    The Gold Mine is the second Mining Location. It is located to the north of the Hub Island, and can be accessed by hopping on the jump pad at the end of the Coal Mine. In the Gold Mine you can mine cobblestone, coal, iron, and gold. This location requires mining level 1 to access
                    """
                    disc2 = """
                    The Deep Caverns is the third Mining Location. It is located North of the Gold Mine, and can be accessed by hopping on the jump pad at the end of the Gold Mine. In the Deep Caverns you can mine cobblestone, coal, iron, gold, lapis lazuli, redstone, emerald, diamond, diamond blocks, and Obsidian, but beware as there are Mobs on each of the floors. Once you reach a floor, you can access that floor by talking to the Lift Operator. There is a glitch that can be utilized to unlock all the floors, that video has been linked at the end of this section. This location requires mining level 5 to access
                    """
                    disc3 = f"""
                    The Dwarven Mines is the fourth Mining Location. It is located at the bottom of the Deep Caverns, and can be accessed in the Lift Operator's menu once unlocked. To unlock the Deep Caverns, first you need to reach mining level 12, then you have to talk to an NPC by the name of Rhys. Rhys will ask you to gather 3 different enchanted ores, 10 each. The cheapest ores to do this with would be coal, redstone and lapis lazuli. Currently this would cost a total of `{hotm1}`. Once you give all the items to Rhys, you will unlock HOTM 1 and access to the Dwarven Mines. In the Dwarven Mines, all ores from the previous mines are available, but a few ores unique to the Dwarven Mines include Gold Blocks, Mithril, and Titanium.

                    https://youtu.be/edWzYhtNqpI - Unlocking all the Deep Caverns floors
                    """
                    disc4 = """
                    The Crystal Hollows is the fifth and last Mining Location. To access this location HOTM 3 is required. If you meet that requirment talk to Gwendolyn. For a 10,000 coin fee she will give you access to the Crystal Hollows for 5 hours. The Crystal Hollows is Split up into 5 sections, the Jungle, the Precursor Remenents, the Goblin Holdout, the Mithril Deposits, and the Crystal Nucleus. For a more in-depth guide into the Crystal Hollows please look at the Crystal Hollows page in Mining Catagories.
                    """
                    embed.add_field(name='Coal Mine',value=disc,inline=False)
                    embed.add_field(name='Gold Mine',value=disc1,inline=False)
                    embed.add_field(name='Deep Caverns',value=disc2,inline=False)
                    embed.add_field(name='Dwarven Mines',value=disc3,inline=False)
                    embed.add_field(name='Crystal Hollows',value=disc4,inline=False)
                    embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 'crystal hollows':
                    embed =  discord.Embed(title='Crystal Hollows Guide',description='The Crystal Hollows is a big and complex Mining Location with many features and mechanics. It is split up into 4 quadrents and a center. To access this location HOTM 3 is required. If you meet that requirment talk to Gwendolyn. For a 10,000 coin fee she will give you access to the Crystal Hollows for 5 hours. Below are the 5 sections and some other features explained: ',colour=discord.Color.blue())
                    disc = """
                    Crystal Nucleus
                    Jungle
                    Precursor Remenents
                    Goblin Holdout
                    Mithril Deposits
                    Magma Fields
                    Other
                    """
                    embed.add_field(name='Select a location to view information',value=disc,inline=False)
                    embed.set_footer(text='Type in the name of the section you would like to explore')
                    await ctx.send(embed=embed)
                    def check(m):
                        return m.content.lower() == 'crystal nucleus' or m.content.lower() == 'jungle' or m.content.lower() == 'precursor remenents' or m.content.lower() == 'goblin holdout' or m.content.lower() == 'mithril deposits' or m.content.lower() == 'magma fields' or m.content.lower() == 'other' and m.channel == channel
                    msg = await bot.wait_for('message', check=check)
                    if msg.content.lower() == 'crystal nucleus':
                        embed = discord.Embed(title='Cyrstal Nucleus',description='The Crystal Nucleus is the center of the Crystal Hollows. From here you can take a look at your commissions and refill your drills, as well as access all 4 quadrents, but the main mechanic of the Nucleus is Completing it. Each section has a special Crystal that can be used in the nucleus to unlock rewards, or can be used to forge Perfect Gemstones.',colour=discord.Color.blue())
                        disc = """
                        By gathering and placing the 4 Crystals from each of the 4 quadrents and the Topaz Crystal from defeating Bal you can unlock the Nucleus and gain rewards from it. This mainly includes Fine Gems and some other items, but the reason people run the Nucleus is for Jaderald and Divan's Alloy. Jaderald is the best reforge for Mining Armor and Divan's Alloy is an incredibly rare item used to craft the Divan's Drill, and is very expensive.
                        """
                        embed.add_field(name='Nucleus Runs',value=disc,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'jungle':
                        embed = discord.Embed(title='Jungle',description='The Jungle is home to the Amethyst Gemstone and Amethyst Crystal.',colour=discord.Color.blue())
                        disc = """
                        __Kalhuiki Tribe__ - Neutral mobs with player like appearances. They have 1 billion health and deal 800,000 damage per hit but will not attack unless they are attacked themselves or if a Kalhuiki Tribe Youngling has been attacked nearby
                        __Sludge__ - Hostile slime like mobs with 3 different stages, just like a normal Slime.
                        __Key Guardian__ - Drops a Jungle Key, which is required to access the Jungle Temple.
                        """
                        disc1 = """
                        __Jungle Temple__ - Where the Amethyst Crystal can be found. Bonus Speed and Jump Boost are disabled in this area, but sometimes it bugs out and doesn't get rid of the effects
                        __Key Guardian Temple__ - Where the Key Guardian Can be found.
                        __Odawa's Village__ - Where an NPC named Odawa can be found. Odawa sells multiple items whcih cost Sludge Juice and sometimes other items that can be found in the Jungle.
                        """
                        disc2 = f"""
                        First you will want to get your hands on a Jungle Key. There are a few methods for this. The easiest way to obtain a Jungle Key is to buy it off the Auction House. The second method is to kill the Key Guardian, as doing so will guarantee a Jungle Key to drop. The last method is to buy a Jungle Key from Odawa for 100 Sludge Juice, and this would cost `{round(bazaardata['SLUDGE_JUICE']['buyPrice']*100,2)}`. Once you have obtained a Jungle Key head to the Jungle Temple and use the key at the entrance. What follows is a parkour course that leads to the Amethyst Crystal. If you fail the course by falling or getting hit by a trap, you will need to restart with another Jungle Key. Common methods used to help with the parkour are a Wither Cloak Sword and Black Cat pet, but they aren't necessary. At the end of the Parkour is the Amethyst Crystal, which can be used to gain rewards in the Crystal Nucleus or used to forge a Perfect Amethyst Gemstone.
                        """
                        embed.add_field(name='Mob(s) unique to the Jungle',value=disc,inline=False)
                        embed.add_field(name='Structure(s) unique to the Jungle',value=disc1,inline=False)
                        embed.add_field(name='Obtaining the Amethyst Crystal',value=disc2,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'precursor remenents':
                        embed = discord.Embed(title='Precursor Remenents',description='The Precursor Remenents is home to the Sapphire Gemstone and Sapphire Crystal.',colour=discord.Color.blue())
                        disc = """
                        __Automaton__ - Hostile golem like mobs that shoot powerful lazers and drop the components required to access the Saphire Crystal.
                        """
                        disc1 = """
                        __Lost Precursor City__ - Home to the Sapphire Crystal and Professor Robot. This area has many places for Automatons to spawn.
                        """
                        disc2 = """
                        To get the Sapphire Crystal, you have to give the 6 Automaton Components to Professor Robot. These include the Electron Transmitter, FTX 3070, Robotron Reflector, Superlite Motor, and Control Switch. All of these components can be found on the Auction House, but can also be obtained by killing Automatons or opening Treasure Chests in the Precursor Remenents. Both methods are decent for obtaining the Sapphire Crystal. It's recomended that if you plan to run the Crystal Nucleus multiple times to keep the Automaton Part duplicates that you obtain for the next time you need them.
                        """
                        embed.add_field(name='Mob(s) unique to the Precursor Ruins',value=disc,inline=False)
                        embed.add_field(name='Structure(s) unique to the Precursor Ruins',value=disc1,inline=False)
                        embed.add_field(name='Obtaining the Sapphire Crystal',value=disc2,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'goblin holdout':
                        embed = discord.Embed(title='Goblin Holdout',description='The Goblin Holdout is home to the Amber Gemstone and Amber Crystal, as well as a bunch of goblins',colour=discord.Color.blue())
                        disc = """
                        __Goblins__ - Most if not all Goblin varaities can be found in the Goblin Holdout. All of them have player like appearances with green skin and yellowing teeth.
                        """
                        disc1 = """
                        __Goblin Queen's Den__ - Where the Amber Crystal is located.
                        _King Yolkar's Tower__ (Unofficial Name) - Where King Yolkar is located.
                        """
                        disc2 = f"""
                        To obtain the Amber Crystal, you will first want to talk to King Yolkar and give him 3 Goblin Eggs. There are 5 types of Goblin Egg but the cheapest ones to use would be the Uncommon and Rare Goblin Eggs, which cost {round(bazaardata['GOBLIN_EGG_GREEN']['buyPrice']*3,2)} and {round(bazaardata['GOBLIN_EGG']['buyPrice']*3,2)} respectively. Once you give the 3 Goblin Eggs to King Yolkar, you will obtain the King Scent which you can use to bypass the guards guarding the Amber Crystal.
                        """
                        embed.add_field(name='Mob(s) unique to the Goblin Holdout',value=disc,inline=False)
                        embed.add_field(name='Structure(s) unique to the Goblin Holdout',value=disc1,inline=False)
                        embed.add_field(name='Obtaining the Amber Crystal',value=disc2,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'mithril deposits':
                        embed = discord.Embed(title='Mithril Deposits',description='The Mithril Deposits is home to the Jade Gemstone and Jade Crystal, as well as alot of Mithril',colour=discord.Color.blue())
                        disc = """
                        __Team Treasurite Members__ - Mobs with player like appearances that throw balls that spawn small mobs such as wolves and endermites, similar to Team Rocket from the famous Game and Anime series, Pokèmon.
                        """
                        disc1 = """
                        __Mines of Divan__ - Home to the Jade Crystal. It is also a popular spot used to mine Jade Gemstones due to its large veins.
                        __Corleone's Hideout__ (Unofficial Name) - Where Boss Corleone is located.
                        """
                        disc2 = """
                        To obtain the Jade Crystal, talk to one of the 4 Keepers. They will provide you with a metal detector whcih you can use on the gold floor of the Mines of Divan. You will need to find 4 weapons using the Metal Detector. Once you find all 4 weapons return them to each of the Keepers. Doing so will spawn the Jade Crystal in the middle of the Mines of Divan.
                        """
                        embed.add_field(name='Mob(s) unique to the Mithril Deposits',value=disc,inline=False)
                        embed.add_field(name='Structure(s) unique to the Mithril Deposits',value=disc1,inline=False)
                        embed.add_field(name='Obtaining the Jade Crystal',value=disc2,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'magma fields':
                        embed = discord.Embed(title='Magma Fields',description='The Magma Fields are home to the Topaz Gemstone and Topaz Crystal. The Magma Fields generate below Y=64 throughout the Crystal Hollows. In this area players can expect to generate Heat. At 100 Heat the player will start burning exponential damage until they cool down or die',colour=discord.Color.blue())
                        disc = """
                        __Yog__ - Magma Cubes that explode after being killed
                        """
                        disc1 = """
                        __Khazad-dûm__ - Home of the Topaz Crystal and Bal. It is also a popular spot used to mine Topaz Gemstones due to its large veins.
                        """
                        disc2 = """
                        To obtain the Topaz Crystal, you have to kill Bal. Bal has 100 hitpoints and takes damage in increments of 1. Using a Hurricane Bow or Juju are recomended. Killing Bal spawns the Topaz Crystal behind him.
                        """
                        embed.add_field(name='Mob(s) unique to the Magma Fields',value=disc,inline=False)
                        embed.add_field(name='Structure(s) unique to the Magma Fields',value=disc1,inline=False)
                        embed.add_field(name='Obtaining the Topaz Crystal',value=disc2,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'other':
                        embed = discord.Embed(title='Other locations in the Crystal Hollows',description='There are many randomly spawning structures in the Crystal Hollows. Most include one or two Treasure Chests and unique veins of Gemstones. The 2 below are the most prominent of these other locations',colour=discord.Color.blue())
                        disc = """
                        The Fairy Grotto spawns randomly anywhere in the Crystal Hollows. It is the only place where Jasper Gemstones spawn. The Fairy Grotto is also home to mobs called Butterflies.
                        """
                        disc1 = """
                        The Dragon's Lair is home to a Giant Dragon. It sells 3 Golden Dragon Eggs per lobby it is in. It can spawn anywhere in the Crystal Hollows, but unlike the Fairy Grotto, it does not have a guaranteed chance to spawn
                        """
                        embed.add_field(name='Fairy Grotto',value=disc,inline=False)
                        embed.add_field(name="Dragon's Lair",value=disc1,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                elif msg.content.lower() == 'events':
                    embed = discord.Embed(title='Mining Events',description='Mining Events are events that occur every Skyblock Day in the Dwarven Mines and Crystal Hollows',colour=discord.Color.blue())
                    disc = """
                    This event provides doubled powder rates in the Dwarven Mines and Crystal Hollows.
                    """
                    disc1 = """
                    This event provides +600 Mining Speed if your look the right direction in the Dwarven Mines and Crystal Hollows.
                    """
                    disc2 = """
                    This event provides +500 Mining Speed and +50 Mining Fortune if you are close to at least 1 player in the Dwarven Mines and Crystal Hollows.
                    """
                    disc3 = """
                    The raffle is an event that occurs in the Dwarven Mines. Participating in the event grants Mining XP, Mithril Powder, HOTM Xp, and bits (If you have a booster cookie). Collecting tickets on the ground and returning them to the raffle box grants a chance to get triple drops.
                    """
                    disc4 = """
                    The Mithril Gourmand event is an event that occurs in the Dwarven Mines. Mining mithril in the deignated area gives the player Tasty Mithril. Giving multiple of this item to an NPC called Don Esspresso gives 20,000 Mining XP, 100 HOTM XP, and 1000 Mithril Powder.
                    """
                    disc5 = """
                    The Goblin Raid is an event in the Dwarven Mines. Killing all 1000 Goblins in the designated area gives 20,000 Mining XP, 100 HOTM XP, and 1000 Mithril Powder.
                    """
                    embed.add_field(name='2x Powder',value=disc,inline=False)
                    embed.add_field(name='Gone with the wind',value=disc1,inline=False)
                    embed.add_field(name='Better Together',value=disc2,inline=False)
                    embed.add_field(name='Raffle',value=disc3,inline=False)
                    embed.add_field(name='Mithril Gourmand',value=disc4,inline=False)
                    embed.add_field(name='Goblin Raid',value=disc5,inline=False)
                    embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 'hotm':
                    embed = discord.Embed(title='Heart of the Mountain',description='The Heart of the Mountain (aka HOTM) is a upgradeable stats tree the player can use to buff their own Mining Stats. HOTM provides a massive benefit to the player when Mining for XP, Powder, or money. HOTM currently has 7 levels',colour=discord.Color.blue())
                    hotm1 = bazaardata['ENCHANTED_COAL']['buyPrice']*10 + bazaardata['ENCHANTED_REDSTONE']['buyPrice']*10 + bazaardata['ENCHANTED_LAPIS_LAZULI']['buyPrice']*10
                    hotm1 = round(hotm1,2)
                    disc = f"""
                    To obtain the first HOTM level you have to talk to an NPC by the name of Rhys. Rhys will ask you to gather 3 different enchanted ores, 10 each. The cheapest ores to do this with would be coal, redstone and lapis lazuli. Currently this would cost a total of `{hotm1}`. Once you give all the items to Rhys, you will unlock HOTM 1
                    """
                    disc1 = """
                    Leveling HOTM takes a very long time. To first start out you want to talk to the King of the Dwarven Mines (There are actually 7 different kings but they switch once every minecraft day). After a bit of dialogue you will get access to the Commisions. Commisions are essentially quests that give Mining XP, HOTM XP, and Powder upon completion. The first 4 Commisions of the day grant 1000 more HOTM XP so it is recomended to do at least 4 Commisions a day for a casual playthrough.\n\nCommisions themselves come in one of few types. In the Dwarven Mines, these consist of Mining Mithril in a certain zone of the Dwarven Mines, killing Goblins or Ice Walkers, or praticipating in events. In the Crystal Hollows, these consist of Mining a certain Gemstone, defeating certain enemies, Mining Hardstone, or finding Crystals. Dwarven Commisions give a base HOTM XP of 100 while Crystal Hollows Commisions give 400 bas HOTM XP. While Crystal Hollows Commisions give more XP they are much harder to do.
                    """
                    disc2 = """
                    HOTM 1 - Obtain a set of Glacite Armor from the Auction House, this is a set you likely have already gotten or will get as this is a great early game Combat set and Mining set. If you are on Ironman or wish to grind out the set yourself then use a Pickaxe of any kind to attack the icewalkers as a pickaxe does more damage to them. For a Pickaxe to use at HOTM one talk to an NPC named Bubu in the Dwarven Mines and buy a Fractured Mithril Pickaxe.\n\nHOTM 2 - Once you reach HOTM 2 go back to Bubu and buy a Bandaged Mithril Pickaxe. If you haven't already done so reforge your Pickaxe to Fortunate or Excellent, or use a Lapis Crystal for extra Mining XP\n\nHOTM 3 - You could probably continue using the gear from HOTM 3, but for an upgrade we recomend buying a Titanium Pickaxe at Bubu. If you play Ironman we recomend you start gathering the materials nescessary to forge a Titanium Drill DR-X355 as this and it's upgraded forms will help in the gathering of Gemstones to craft things like Divan Armor.
                    """
                    disc3 = """
                    HOTM 4 - At HOTM 3 you unlocked access to the Crystal Hollows, and while that's a great thing, we don't recomend doing the rest of your commissions there. As for gear we recomend upgrading your Titanium Pickaxe to a Refined Titanium Pickaxe at Bubu.\n\nHOTM 5 - At HOTM 5 you unlock Sorrow Armor, which is a big upgrade from the Glacite you were using. We recomend buying Sorrow Pieces that are either already reforged or have the Gemstone Slots unlocked on them, as they are similarlly priced to ones without.\n\nHOTM 6 - At level 6 we recomend buying a Gemstone Gauntlet. At this level the Armor of Divan is also unlocked but it is very pricey so we recomend only buying it if you to plan to mine Gemstones for money. Ironman players are recomended to have aquired a Titanium Drill DR-X455 or DR-X555 at this point with decent attachments. Since these items are a bit pricey it is now worth it to use a good reforge stone on them such as Hot Stuff or Rock Gemstone\n\nHOTM 7 - Your done leveling HOTM.
                    """
                    disc4 = """
                    Peak of the Mountain is a permenently upgradeable Perk in HOTM. It has 5 levels and each level requires an increasing amount of Mithril Powder. Upgrading it completely yeilds massive benifits such as 2 Tokens of the Mountain as well as an extra Forge and Commission slot.
                    """
                    disc5 = """
                    HOTM is a customizable skill tree that you can upgrade to best suit your needs. Below are some skill trees that are used commonly for certain applications. The ones highlighted in blue are perks of special importance and should be focused on.\n\nMithril/Titanium Mining - https://imgur.com/r669szn\n\nPowder Mining - https://imgur.com/Oev6Trm\n\nGemstone Mining - https://imgur.com/3F41zjR
                    """
                    disc6 = """
                    There are 2 types of Powder when it comes to Mining, Mithril Powder and Gemstone Powder, being earned from their respective ores. Powder is not a physical item but rather a stat added to your profile. Powder can be used to upgrade perks in the HOTM Skill Tree. For applications such as Gemstone Mining it is recomended to have a large amount of Powder.
                    """
                    embed.add_field(name='Unlocking HOTM',value=disc,inline=False)
                    embed.add_field(name='Commissions',value=disc1,inline=False)
                    embed.add_field(name='HOTM Gear Progression: 1-3',value=disc2,inline=False)
                    embed.add_field(name='HOTM Gear Progression: 4-7',value=disc3,inline=False)
                    embed.add_field(name='Peak of the Mountain',value=disc4,inline=False)
                    embed.add_field(name='HOTM Tree',value=disc5,inline=False)
                    embed.add_field(name='Powder',value=disc6,inline=False)
                    embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 'gemstones':
                    disc = f"""
                    Gemstones can be found mainly in the Crystal Hollows and in the Crimson Isles. Each gemstone gives various buffs depending on the type and tier. Each gemstone has 5 tiers, rough, flawed, fine, flawless, and perfect. There are 8 gemstones, being amber, jade, topaz, sapphire, ruby, amethyst, jasper, and opal.
                    Jade is found in the crystal hollows and gives mining fortune.
                    Amber is found in the crystal hollows and gives mining speed
                    Topaz is found in the crystal hollows and gives pristine
                    Sapphire is found in the crystal hollows and gives intelligence
                    Ruby is found in the crystal hollows and gives health
                    Amethyst is found in the crystal hollows and gives defense
                    Jasper is found in the crystal hollows, more specifically, fairy grotto, and gives strength
                    Opal is found in the Smoldering Tomb and gives true defense
                    Gemstones can be applied to armor, talismans, and weapon to grant the item extra stats
                    """
                    disc1 = f"""
                    Many armor pieces and weapon have gemstone slots. This means gemstones can be added to grant a small stat boost. Some have to be unlocked by the player, while some are automatically unlocked. The cost of the slot vary depending on the armor/weapon. An item can have 1-5 gemstone slots. There are specific types of gemstone slots, named below
                    Universal Slot-Any gemstone can be inserted
                    Combat-Jasper, sapphire, ruby, amethyst
                    Offensive-Jasper and sapphire
                    Defensive-Ruby and amethyst
                    Mining-Amber, jade, topaz
                    This link shows all items that have gemstone slots and what it costs to unlock
                    https://hypixel-skyblock.fandom.com/wiki/Gemstone_Slot?adlt=strict&toWww=1&redig=7418E8D3289C4B9F939067E65D1EEDC6
                    """
                    embed.add_field(name='Gemstones',value=disc,inline=False)
                    embed.add_field(name='Gemstone Slots',value=disc1,inline=False)
                    embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                    await ctx.send(embed=embed)
            elif msg.content.lower() == 'combat':
                embed = discord.Embed(title='Combat Catagories',description='',colour=discord.Color.blue())
                disc = """
                __Select a Combat Catagory to view information__

                Experience
                Locations
                Gear Progression
                Crimson Isle
                """
                embed.add_field(name='Options',value=disc,inline=False)
                embed.set_footer(text='Type in the name of the section you would like to explore')
                await ctx.send(embed=embed)
                def check(m):
                    return m.content.lower() in ['experience','locations','gear progression','crimson isle'] and m.channel == channel
                msg = await bot.wait_for('message',check=check)
                if msg.content.lower() == 'experience':
                    embed = discord.Embed(title='Combat Experience',description='This is a guide on the most common and efficient ways to gain combat experience',colour=discord.Color.blue())
                    disc = """
                    1) Booster Cookie - Provides a +25 Combat Wisdom bonus
                    2) Combat XP Boost III Potion - Provides a +20 Combat Experience bonus
                    3) Legendary Wolf Pet - Provides a +30 Combat Wisdom bonus
                    """
                    disc1 = """
                    The Bestiary is a system that tracks Individual Mob Kills in game. Similar to collections, killing a certain number of a mob will cause will cause the player to unlock Bestiary Milestones. 10 Individual Milestones will lead to an increase in the overall milestone. Every even Bestiary Milestone will result with the player being awarded 1 million Combat Experience, making it a very viable method to level Combat.
                    """
                    disc2 = """
                    The first place to grind Combat XP is the Deep Caverns, as the player can find lapis zombies, and miner skeletons/zombies. The next step are the crypts, located in a cave at the edge of the graveyard and are home to crypt ghouls. These give a good amount of combat xp and are often used to spwan the Revenent Horror boss. The next step a player could take are the enderman located in the End. These can be grinded for both Combat XP and Ender Armor pieces. Although it may be more expensive, the Tier 5 Revenant Horror is a good way to grind Combat XP. Once the player starts to play dungeons, Combat XP will be gained passively as every mob gives a decent amount of Combat XP, and will eventually add up over time. If the player is able to efficiently clear the Floor 6 Dungeon, a good way to gain a lot of Combat XP are the Golems in the F6 boss room. Another way to gain Combat XP is through Ghosts. Ghosts are found in "The Mist" in the Dwarven Mines. They have 1 million hp and only take melee damage.
                    """
                    embed.add_field(name='XP Boosts',value=disc,inline=False)
                    embed.add_field(name='Bestiary',value=disc1,inline=False)
                    embed.add_field(name='XP Gain Progression',value=disc2,inline=False)
                    embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 'locations':
                    embed = discord.Embed(title='Combat Locations',description='Islands and Areas in the Skyblock Game centered around Combat',color=discord.Color.blue())
                    disc = 'Home to Zombies, Zombie Villagers(Only at night), and Crypts'
                    disc1 = 'Requires combat level 1 to enter. You can find variants of different spiders, relics, arachne, and the broodmother.'
                    disc2 = 'Not a Combat Island since it has a Foraging 1 requirement but has the Howling Cave located in the waterfall, which is home to 3 different types of wolves.'
                    disc3 = 'Requires combat level 12. Home to all versions of enderman, including enderman, zealots, voidling fanatics, voidling extremists, watchers, obsidian defenders, and the ender dragon. Also contains the end race.'
                    disc4 = 'Requires combat level 24 to enter. Home to the kuudra boss, all nether mobs, and introduces new blocks like opal, sulphur, mycelium, and red sand.'
                    embed.add_field(name='Graveyard',value=disc,inline=False)
                    embed.add_field(name="Spider's Den",value=disc1,inline=False)
                    embed.add_field(name='The Park',value=disc2,inline=False)
                    embed.add_field(name='The End',value=disc3,inline=False)
                    embed.add_field(name='Crimson Isle',value=disc4,inline=False)
                    embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 'gear progression':
                    embed = discord.Embed(title='Combat Gear Progression',description='A walkthrough of what gear to use at which stages of the game. Please note these are general recomendations and that specific recomendations are highlighted in their specific sections.',color=discord.Color.blue())
                    disc = """
                    The first armor set you will want to aim for is a set of lapis and/or miner armor. This will be good towards getting stronger armor sets and exploring around the skyblock islands. Lapis and miner armor can be dropped from Lapis zombies and miner zombies/skeleton respectively. The next armor set you should aim for is ender armor. This set can be dropped from all enderman(excluding zealots and the ones found in the void sepulture) and is a great starting set. An alternative to ender armor is Glacite Armor which is obtained by killing Ice walkers. Glactite has similar stats to Ender Armor and helps with mining. The next big set is Dragon Armor. Start out on young or unstable dragon armor, as they are relatively cheap and very useful. Young dragon will provide speed and damage, while unstable will do slightly more damage but without speed buffs. The player can then upgrade to strong or wise dragon if they choose to.
                    """
                    disc1 = """
                    The first sword used by most players should be the undead sword. It is very cheap and can get you through a lot of the early game. An alternative could also be the silver fang. The next major weapon you should aim for is the aspect of the end(also called aote for short) and/or the raiders axe. Both are very good until you can make the next upgrade and are about the same price. An important thing to note is that the aspect of the end can be kept due to its high usefulness in its teleport ability. The next weapon to carry you into mid game is the aspect of the dragons(also called aotd for short). This weapon is quite strong and can be used as a weapon for dungeons as well.
                    """
                    disc2 = """
                    Shadow assassin will be the next major armor set. It is purely a damage set, and is obtained from floor 5 of the catacombs. This armor can be “fragged,” meaning when surrounded by 8 livid frags in a crafting table, the rarity increases and also gets higher stats. This set is great both inside and outside of dungeons, and will be used until the next armor set(s) can be obtained. The tarantula helmet, reaper mask, and golden heads are also great options to use. They provide a good amount of damage and can be better than a shadow assassin helmet in some cases. The Tarantula Helmet is especially good outside of dungeons, reaper mask can provide extra healing, and golden heads give double the stats(only of the helmet) inside its given dungeon floor. Necromancer lord armor is also a viable option. It is a tanky armor set without damage, and is obtained from floor 6. It can be used both as a tank and mage set, but does not perform well outside of dungeons.
                    """
                    disc3 = """
                    The next upgrade from the aspect of the dragons is the flower of truth(fot) and/or livid dagger. The flower of truth has a very useful ability that makes killing a large amount of mobs quite easy. The livid dagger on the other hand is very useful for dealing high amounts of damage to a single target per second. Another possible(but not needed) upgrade is the shadow fury, which is similar to the livid dagger but with higher potential damage output. If the player is a mage class, the spirit sceptre is a great weapon. It has high damage output on its ability and can be spammed very fast. It will be the best mage weapon before the hyperion. For archers, the juju shortbow will be the best. It is a very strong bow capable of insta shooting and will be the best until the terminator.
                    """
                    disc4 = """
                    After the completion of floor 7, the 4 Wither Sets, Necron, Storm, Goldor, and Maxor, will be unlocked. Necron is purely a damage set, and is used for berserkers and archers both outside and inside of dungeons. Maxor is a set without much base stats, but is commonly used with Archer and Mage sets due to its high speed. Storm is an intelligence based set, meaning its useful for mages. Goldor is a tank set, giving lots of health and defense. At this point, other armor pieces will start to be considered. The Warden Helmet is a better version of the Tarantula Helmet unlocked at Revenant Horror level 8. It gives damage depending on the speed of the player, and is one of the best helmets outside of dungeons.  Diamond heads can also start being used inside of dungeons. They function the same way as golden heads, but have higher stats. The final sets to consider are the Aurora and Crimson armor. If time is taken to upgrade these sets , then these sets outperform Storm and Necron outside Dungeons.
                    """
                    disc5 = """
                    Once the player has progressed more, they can look into weapons that will carry them all around skyblock. A great melee choice is the giant sword(F6) or dark claymore(M7). Both have very high single hit damage and will be the best melee weapon. For archers, the best bow is the Terminator, as it shoots 3 arrows at once and also has a strong beam ability, and is the best weapon for high dungeon floors. The best mage weapon will be the hyperion/wither blade. It does high amounts of area damage while teleporting you forward. There are 4 variants, astraea, scylla, hyperion, and valkyrie. The astraea is a tank based wither blade, giving defense and true defense. The scylla can be used for mage or for general healing, as it has high critical damage stats. The hyperion is a plain mage weapon, giving just huge amounts of intelligence. The valkyrie has a melee capability, giving strength and damage.
                    """
                    embed.add_field(name='Early Game Armor',value=disc,inline=False)
                    embed.add_field(name='Early Game Weapons',value=disc1,inline=False)
                    embed.add_field(name='Mid Game Armor',value=disc2,inline=False)
                    embed.add_field(name='Mid Game Weapons',value=disc3,inline=False)
                    embed.add_field(name='Late Game Armor',value=disc4,inline=False)
                    embed.add_field(name='Late Game Weapons',value=disc5,inline=False)
                    embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 'crimson isle':
                    embed = discord.Embed(title='Crimson Isle',description='The Crimson Isle is the largest Island by both size and amount of features, making it very expansive and very confusing to players.',color=discord.Color.blue())
                    disc = """
                    __Select a Crimson Isle Catagory to view Information__

                    Locations
                    Bosses
                    Kuudra
                    Dojo
                    Factions
                    """
                    embed.add_field(name='Options',value=disc,inline=False)
                    embed.set_footer(text='Type in the name of the section you would like to explore')
                    await ctx.send(embed=embed)
                    def check(m):
                        return m.content.lower() in ['locations','bosses','dojo','factions','kuudra'] and m.channel == channel
                    msg = await bot.wait_for('message',check=check)
                    if msg.content.lower() == 'locations':
                        embed = discord.Embed(title='Crimson Isle Locations',description='Information on the Various Locations in the Crimson Isle',color=discord.Color.blue())
                        disc = """
                        The first location the Player explores when they spwan on the Crimson Isle. Mobs in this location Include the Boss Bladesoul, Bezals, Blazes, Wither Skeletons, and Wither Spectres. The NPC Elle will also be located in the Stronghold, who starts off the player with their main quest to carry throught their Journey in the Crimson Isle.
                        """
                        disc1 = """
                        Right outside the Stronghold, the Crimson Fields are where players can find Magma Cubes.
                        """
                        disc2 = """
                        The giant volcano in the middle of the Crimson Isle is a common spot for Lava Fishing and is the Home to Odgar. Inside the volcano lava will slowly rise and when it erupts, it unleashes mobs called Matchos and Mineable Sulfur
                        """
                        disc3 = """
                        Located Inside the Volcano, Odgars Hut is the home of Odgar, an NPC that tracks the players Trophy Fish.
                        """
                        disc4 = """
                        A pool of lava that has an extremly rare chance to spawn the Pihlegblast Sea Creature. Also home to the Kuudra Beliver NPC.
                        """
                        disc5 = """
                        A large underground area that spawns Flares and the Magma Boss.
                        """
                        disc6 = """
                        Found through on of the many tunnels leading off the Magma Chamber, this location is home to the Aura NPC, who currently serves no known purpose.
                        """
                        disc7 = """
                        Found through on of the many tunnels leading off the Magma Chamber, this location is home to the Matriarch. Inside the Matriarch is the Belly of the Beast, where the player can obtain Heavy Pearls. These can be used to upgrade the Kuudra Sets.
                        """
                        disc8 = """
                        The Dojo is a location where the player can earn and upgrade an exclusive Belt accessory. Speaking to Master Tao will earn you the White Belt, and completing the Dojo Challenges will upgrade the Belt, up to the Black Belt.
                        """
                        disc9 = """
                        Past the Crimson Fields is the home to mobs such as the Magma Cube Riders and the Flaming Spiders, as well as Red Sand.
                        """
                        disc10 = """
                        Located between the Crimson Fields and Scarlaton, this location houses mobs such as Mushroom Bulls, Exes, Wais, and Zees. Mooshroom can also be mined here.
                        """
                        disc11 = """
                        Home of the Barbarians.
                        """
                        disc12 = """
                        Home of the Mages.
                        """
                        disc13 = """
                        An addititon of the Barbarian Outpost, this is where the player goes to join the Barbarian Faction. Here the player can also find a Blacksmith, Townsquare, Auction House, Bazaar, and a Minion Shop selling t12 minions
                        """
                        disc14 = """
                        Located within Dragontail, Cheif Scorn and his Barbarian Guards reside here.
                        """
                        disc15 = """
                        The spawnpoint of the Barbarian Duke X Boss.
                        """
                        disc16 = """
                        An addititon of the Mage Outpost, this is where the player goes to join the Mage Faction. This location also includes the Scarleton Community center, where players go to complete quests, the Throne Room located above the community center, the Mage Council located below the community center, the Scarleton Plaza, where players can access the Auction House, Bazaar, buy t12 minions, access the Bank and Blacksmith.
                        """
                        disc17 = """
                        Located in Scarleton, Igrupan's house is where his chicken coop is. The player will have to complete 2 quests if they choose the Mage Faction here.
                        """
                        disc18 = """
                        Home of the Dean, who plays a big role in the questline if the player chooses the Mage Faction.
                        """
                        disc19 = """
                        The spawnpoint of the Mage Outlaw Boss.
                        """
                        disc20 = """
                        A barren land filled only with netherrack.
                        """
                        disc21 = """
                        The spawnpoint of the Ashfang Boss.
                        """
                        disc22 = """
                        Located next to The Wasteland, this large skull is the home to the Kuudra Gatekeeper, who can be used to access the Kuudra bossfight
                        """
                        disc23 = """
                        Located next to The Wasteland, this set of caves is home to the Opal Gemstones and Blazes, which are meant to be used for Blaze Slayer.
                        """
                        embed.add_field(name='Stronghold',value=disc,inline=False)
                        embed.add_field(name='Crimson Fields',value=disc1,inline=False)
                        embed.add_field(name='Blazing Volcano',value=disc2,inline=False)
                        embed.add_field(name="Odger's Hut",value=disc3,inline=False)
                        embed.add_field(name='Plhlegblast Pool',value=disc4,inline=False)
                        embed.add_field(name='Magma Chamber',value=disc5,inline=False)
                        embed.add_field(name="Aura's Lab",value=disc6,inline=False)
                        embed.add_field(name="Matriarch's Lair",value=disc7,inline=False)
                        embed.add_field(name='Dojo',value=disc8,inline=False)
                        embed.add_field(name='Burning Desert',value=disc9,inline=False)
                        embed.add_field(name='Mystic Marsh',value=disc10,inline=False)
                        embed.add_field(name='Barbarian Outpost',value=disc11,inline=False)
                        embed.add_field(name='Mage Outpost',value=disc12,inline=False)
                        embed.add_field(name="Dragontail",value=disc13,inline=False)
                        embed.add_field(name="Cheif's Hut",value=disc14,inline=False)
                        embed.add_field(name='The Dukedom',value=disc15,inline=False)
                        embed.add_field(name="Scarleton",value=disc16,inline=False)
                        embed.add_field(name="Igrupan's House",value=disc17,inline=False)
                        embed.add_field(name='Cathedral',value=disc18,inline=False)
                        embed.add_field(name='Courtyard',value=disc19,inline=False)
                        embed.add_field(name='The Wasteland',value=disc20,inline=False)
                        embed.add_field(name='Ruins of Ashfang',value=disc21,inline=False)
                        embed.add_field(name='Forgotten Skull',value=disc22,inline=False)
                        embed.add_field(name='Smoldering Tomb',value=disc23,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'bosses':
                        embed = discord.Embed(title='Crimson Isle Bosses',description='Information on the various bosses on the Crimson Isle',color=discord.Color.blue())
                        embed1 = discord.Embed(title='Crimson Isle Bosses Cont.',description='Continutation from the previous Embed',color=discord.Color.blue())
                        disc = """
                        **About:** Spawns in “Ruins of Ashfang” at -484, 135, -1010. Looks like 2 blazes stacked on top of each other, and has 50m hp. Ashfang can only be damaged in margins of 2m, by blaze souls. Blaze souls are spawned when one of his minions are killed, right where the blaze was before it died. Players must aim carefully(because easy to miss), and left click to shoot it at ashfang. Ashfang will heal 2m hp for each type of blaze not killed when he calls them back.
                        **How to fight:** Ashfang will throw out a ring of blazes, with there being 3 different types, all of which have 10m HP
                        **Ashfang Underling:** Labeled with a red name. Takes all forms of damage and is the easiest to kill
                        **Ashfang Acolyte:** Labeled with a blue name. Does not take magic damage.
                        **Ashfang Follower:** Labeled with a gray name. Only can be damaged by “gravity.” player must lure them into gravity areas.
                        """
                        disc1 = """
                        **Abilities:** Player can be “frozen” by ashfang follower, preventing them from using abilities, a message saying “you are too cold to use abilities!” will pop up if you try. Ashfang also cannot be damaged by normal attacks due to his “scorched barrier” and can also damage you with it.
                        **Drops:** Drops the “Lumino Fiber,” which is needed for questline as well as crafting fire veil wand. Also drops variants of blaze rods(normal and enchanted) alongside a possible kuudra key and magma urchin
                        """
                        disc2 = """
                        **About:** Has 70m hp, and spawn in the “The Dukedom” at -535, 117, -900. Melee boss that takes all forms of damage. Has high damaging attacks.
                        **How to fight:** Players can take different methods depending on gear.
                        **Archer:** Voodoo doll for slow+bow spam while dodging jump attack will eventually kill him, might take a couple lives as he can usually just jump behind you and deal high amounts of damage.
                        **Phantom rod cheese:** Basically what it sounds, phantom rod then spam left click, takes a long time but it works, must still dodge jump attacks
                        **Mage:** Voodoo doll is nice for slow down+high DoT damage. Power orb and Mana Steal are good for mana regen. Try to stay out of its melee while spamming ability
                        **Melee/Bers:** Necron/crimson+Warden is ideal for this, with a t6 enchanted giants sword or claymore. Voodoo doll and power orbs are nice but not needed. Dodge the Barb Duke and attack constantly.
                        """
                        disc3 = """
                        **Cheese strat for hype users(thank you to h8re’s guildmate for telling him so he can tell me):** if no one is on top of the arena, player can go under the area to spam wither impact into the ceiling, this will damage the barbarian through the ground while he cannot damage you.
                        **Abilities:** Melee attack, and a jump attack. The area of landing for the jump attack is marked by a ring of purple particles on the ground. Stay out of this or you will get stunned and be unable to move, then you might die.
                        **Drops:** Drops “leather cloth” which is needed for mage quest line and to craft the gauntlet of contagion. Also drops variants of porkchop(raw and enchanted) alongside possible kuudra key and magma urchin.
                        """
                        disc4 = """
                        **About:** Wither Skeleton with a mini blaze on his head, has 50m base hp, spawns in the stronghold at -295, 82, -520. Has mediocre damage but high damaging abilities. Bladesoul takes all forms of damage.
                        **How to fight:** Player can usually out-heal his dps with wither shied/syphon/florid/wand, is relatively slow so you can just run away if needed. There are some cheeses with bladesoul
                        **Staircase cheese:** Bladesoul can’t go past the staircase leading out from his room, so players can camp around the corner of the wall to damage him while not getting hit by his melee.
                        **Ledge camp:** Bladesoul has short melee reach, so players can stand on the ledges to avoid his melee attack.
                        THIS DOES NOT PREVENT YOU FROM GETTING HIT BY HIS WITHER SKULL ATTACK
                        """
                        disc5 = """
                        **Abilities:** Summons and shoots a ring of wither skulls around him, does heavy damage and a good chance to 1 hit you. It can be avoided as the skulls are relatively slow and he spawns a lot of black particles around him before he does, giving players a chance to back off and get ready. Bladesoul can also spawn in a wither guard, wither guards have 5m hp and increase bladesoul’s hp by 12.5m for each guard alive, when killed his hp will drop back down. Bladesouls is also THE ONLY boss who heals from player deaths.
                        **Drops:** Drops “Hallowed skull” which is needed for quest line and to craft ragnarock axe and wand of strength. Drops variants of coal(normal and enchanted) alongside possible kuudra key and magma urchin.
                        """
                        disc6 = """
                        **About:** Spawns in the Courtyard at -180, 105, -860. Has 70m hp and various attacks. Mage outlaw also does not move other than floating up and down a few blocks.
                        **How to fight:** Player should try and damage it all times unless it has shield up or must dodge an attack.
                        **Melee/Bers:** Warden+necron/crimson with a t6 enchanted giant sword/claymore is a great choice, will allow player to get lot of damage in without dying.
                        **Archer:** Similar idea to bers, orb might be nice due to less healing
                        **Mage:** Ability spam will get the job done relatively fast, though DO NOT use ability against mage shield as it will most likely 1 tap you.
                        **Abilities:**  Mage outlaw will usually start by spawning an end crystal above him, which shoots a laser at you. You can’t really dodge it but can out-heal it fairly easily with wither shield/syphon. After this, he will randomly cycle through 3 other abilities.
                        """
                        disc7 = """
                        **Abilities Cont.:** Mage shield(this isnt an ability but more of a passive), usually when he performing one of the other abilities named below, reflects 10% of damage back to you.
                        **Lightning strikes:** Spawns checker board patterns on the ground that lightning hits, just avoid them.
                        **Red dome:** Creates a dome outlined by redstone blocks and red particles, stay outside of it.
                        **Wither summons:** Spawns 2 flying wither skulls with 200k hp, mage outlaw cannot be damage until they die.
                        **Drops:** Drops “spell powder” which is used for barbarian questline(i assume) and used to craft both the fire freeze staff and fire veil staff(yes the ashfang staff) as well as the wand of strength. Drops variants of glowstone(normal and enchanted) as well as potential kuudra key and magma urchin.
                        """
                        disc8 = """
                        **About:** Huge magma cube, spawns in the magma chamber underneath the blazing volcano. There is like 15 entrances but one of them is at -338, 87, -686 then at -373, 80, -720.
                        **How to fight:** Magma boss has 5(?) phases where he must “absorb damage” everytime a phase ends he splits into a bunch of smaller cubes, then reforms into the main one. Not necessarily hard, just very long and needs a lot of people
                        **Abilities:** Lights the floors on fire(not like vanilla fire but fire particles), avoid them to not take damage.
                        """
                        disc9 = """
                        Vanquishers are a miniboss, similar to special zealots, they can spawn when any crimson isles mob is killed. They are withers with 10m hp and drop 3 nether stars(or 1-2 if ur loot sharing). Nether stars can be crafted into vanquished equipment, more specifically: Vanquished Ghast Cloak, Vanquished Glowstone Gauntlet, Vanquished Blaze Belt, Vanquished Magma Necklace (feel free to right click the nether star to view recipes), these all require the highest/second highest collection for that item.
                        """
                        disc10 = """
                        Each boss can only be beat 4 times if you want the drops, beat another boss to reset this.
                        You must actually pick up the drops, it does not instantly go into your inventory
                        They give a lot of runecrafting xp if you want to level that for some reason
                        Kuudra is in its own seperate section because of its expansiveness
                        """
                        embed.add_field(name='Ashfang',value=disc,inline=False)
                        embed.add_field(name='Ashfang Cont.',value=disc1,inline=False)
                        embed.add_field(name='Barbarian Duke X',value=disc2,inline=False)
                        embed.add_field(name='Barbarian Duke X Cont.',value=disc3,inline=False)
                        embed.add_field(name='Bladesoul',value=disc4,inline=False)
                        embed.add_field(name='Bladesoul Cont.',value=disc5,inline=False)
                        embed1.add_field(name='Mage Outlaw',value=disc6,inline=False)
                        embed1.add_field(name='Mage Outlaw Cont.',value=disc7,inline=False)
                        embed1.add_field(name='Magma Boss',value=disc8,inline=False)
                        embed1.add_field(name='Vanquishers',value=disc9,inline=False)
                        embed1.add_field(name='General Notes',value=disc10,inline=False)
                        embed.set_footer(text='Continue to the next Embed')
                        embed1.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                        await ctx.send(embed=embed)
                        await ctx.send(embed=embed1)
                    elif msg.content.lower() == 'dojo':
                        embed = discord.Embed(title='The Dojo',description='Information regarding the Dojo and its Challenges',color=discord.Color.blue())
                        disc = """
                        Master Tao stands outside the Dojo at -234 108 -632 and has 7 Challenges for the player to complete. The player gets score based on how they perform in each challenge. This score then contributes to the level of your Dojo Belt, white being the lowest and black being the highest, similar to Karate and Taekwando. Each Challenge lasts 2 minutes.
                        """
                        disc1 = """
                        The player spawns into the Dojo and zombies start to spawn around them. Hitting these zombies into the lava earns the player a certain amount of points. The amount of points is based on the Helmet the Zombie is waering:
                        Leather Helmet - Punching this Zombie just once causes a subtration of 30 points from the players total score. This Zombie should be avoided
                        Iron Helmet - This Zombie awards 10 points upon falling into lava.
                        Gold Helmet - This Zombie awards 20 points upon falling into lava.
                        Diamond Helmet - The only zombies that spwan with this helmet are Baby Zombies. They are harder to hit in due to having a smaller hitbox and being faster but they award 30 points.
                        """
                        disc2 = """
                        The player spawns in and is given Jump Boost(The level of Jump Boost is based on the difficulty level reached). The player has to avoid the walls by going through the holes in them. This game is based on hole in the wall but unlike hole in the wall just touching the wall is immediate failiure, unlike where as in traditional hole in a wall the player has to be knocked off to fail. The player gains 9 points for every 2 seconds they are alive.
                        """
                        disc3 = """
                        The player is given a bow and is required to shoot down targets as they spawn. Based on the color of the target the player gets a certain amount of points. All targets start out at green but as time passes they go too yellow then to red:
                        Green - Lasts 3 Seconds - Gives 8 Points
                        Yellow - Lasts 3 Seconds - Gives 16 Points
                        Red - Lasts 1 Second - Gives 32 Points
                        """
                        disc4 = """
                        The player is slowly given 4 swords, wood, iron, gold, and diamond, and is required to hit zombies with their respective helmets. The player is then required to hit a zombie with a sword corresponding to its helmet. If the player suceeded in doing this they get 8 points, however if they hit a zombie with the wrong sword then they lose 16 points.
                        """
                        disc5 = """
                        The player starts on 1 block and is required to follow a path that appears in front of them as the path behind them disappears. The color of the path will change from green to orange to red indicating that it is disappearing.
                        """
                        disc6 = """
                        This challenge is currently disabled and the guide for this challenge will be written when the challenge is renabled.
                        """
                        disc7 = """
                        The player spawns in and is required to avoid the ghasts fireballs. As time goes on more Ghasts spawn in. As the fireballs make contact with the platform the blocks it made contact with disappear, making the platform an obsticle course.
                        """
                        embed.add_field(name='General Information',value=disc,inline=False)
                        embed.add_field(name='Test of Force',value=disc1,inline=False)
                        embed.add_field(name='Test of Stamina',value=disc2,inline=False)
                        embed.add_field(name='Test of Mastery',value=disc3,inline=False)
                        embed.add_field(name='Test of Discipline',value=disc4,inline=False)
                        embed.add_field(name='Test of Swiftness',value=disc5,inline=False)
                        embed.add_field(name='Test of Control',value=disc6,inline=False)
                        embed.add_field(name='Test of Tenacity',value=disc7,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'factions':
                        embed = discord.Embed(title='Crimson Isle Factions',description='The 2 Crimson Isle Factions are integrel parts of the Crimson Isle Questline. This guide will provide a basic explanation of the 2.',color=discord.Color.blue())
                        disc = """
                        The 2 Factions, the Mage Faction and the Barbarian Faction, represent the 2 main races on the Crimson Isle. Through the Crimson Isle Questline, the player can choose which faction they would like to join. Although the name may suggest this, the player is not required to be a Mage/Berserker to join the Mage or Barbarian Factions respectively. Each Faction has it's own headquarters in its respective locations, where the player can complete quests for Reputation and Combat Experience. If you have already joined a faction, you can always switch, although you would have to jump through some hoops.
                        """
                        disc1 = """
                        Reputation is needed in the crimson isles for certain attributes and kuudra. Rep can be gained by doing the daily quests from the quest board, killing certain minibosses, and defeating kuudra, as well as side quests such as the fighting practice guy, painting guy, and chicken guy.
                        """
                        disc2 = """
                        Every day, their respective headquarters, there will be 5 daily quests for the player to complete. Each quests grants various rewards based on the grade of the quest, ranging from D to S:
                        D - 2000 Combat XP, 30 Reputation.
                        C - 5000 Combat XP, 50 Reputation.
                        B - 10000 Combat XP, 75 Reputation.
                        A - 15000 Combat XP, 100 Reputation.
                        S - 20000 Combat XP, 125 Reputation.
                        Quests can also randomly award various types of loot based on the teir - https://wiki.hypixel.net/Barbarian_Faction / https://wiki.hypixel.net/Mage_Faction
                        """
                        embed.add_field(name='Basic Info',value=disc,inline=False)
                        embed.add_field(name='Reputation',value=disc1,inline=False)
                        embed.add_field(name='Daily Quests',value=disc2,inline=False)
                        embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                        await ctx.send(embed=embed)
                    elif msg.content.lower() == 'kuudra':
                        embed = discord.Embed(title='Kuudra',description='Kuudra is the main boss in the Crimson Isle. There are currently 2 tiers out.',color=discord.Color.blue())
                        disc = """
                        Requires completion of either barbarian or mage questline(you will know if you have the "Fight the monster" quest. There is a 100k entry fee into the bossfight whether the player wins or loses. A "Kuudra key" is required to open the higher tier chest. The bossfight is to shoot tentacles in the lava with cannons. There are 4 tentacles that the players must defeat to win the fight. The kuudra will spawn mobs occasionally, which give tokens when killed. Tokens can also be obtained by shooting power ups and shooting tentacles. Tokens are used for cannon upgrades, as well as revives if a player dies. The best cannon upgrades are multishot, bonus damage, accelerate, rapid fire, and sweet spot.
                        """
                        disc1 = """
                        The tier 2 is unlocked by 1k reputation in either faction(barb or mage) and completion of the tier 1. This requires 200k to enter and a "hot kuudra key" to unlock the higher tier chest. The same principle follows as the tier 1, except the tentacles and mobs gain more hp, and an extra phase at the end. After the 4 tentacles are defeated, Kuudra will spawn alongside the 4 tentacles. The tentacles must be defeated for kuudra to take much damage.
                        """
                        disc2 = f"""
                        {placeholder}
                        """
                        disc3 = f"""
                        {placeholder}
                        """
                        disc4 = f"""
                        {placeholder}
                        """
                        disc5 = """
                        Notable drops are full sets of aurora, crimson, fervor, terror, mana book variants, fatal tempo, kuudra pet, inferno, aurora staff, kuudra teeth, and crimson essence.
                        """
                        disc6 = """
                        Kuudra can also cause events to happen, that can kill you if you do not complete them in time.
                        Mana bomb: 8 prismarine blocks will spawn on the map, players must use mana next to them to disarm, and all players will die if not completed in time.
                        Dropship(s): A ghast(two if its the kuudra boss phase) will spawn, which takes 1 damage no matter what it is hit with, can be damaged by both bows and cannons.
                        Wandering blazes: Blazes will spawn around the map, although there is no time limit, they do increased damage and can only be killed with cannons.
                        """
                        embed.add_field(name='Kuudra T1(Base)',value=disc,inline=False)
                        embed.add_field(name='Kuudra T2(Hot)',value=disc1,inline=False)
                        embed.add_field(name='Kuudra T3(Burning)',value=disc2,inline=False)
                        embed.add_field(name='Kuudra T4(Fiery)',value=disc3,inline=False)
                        embed.add_field(name='Kuudra T5(Infernal)',value=disc4,inline=False)
                        embed.add_field(name='Drops',value=disc5,inline=False)
                        embed.add_field(name='Side Notes',value=disc6,inline=False)
                        embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                        await ctx.send(embed=embed)
            elif msg.content.lower() == 'foraging':
                embed = discord.Embed(title='Foraging Catagories',description='',color=discord.Color.blue())
                disc = """
                __Select a Foraging Catagory to view Information__

                Experience
                Locations
                """
                embed.add_field(name='Options',value=disc,inline=False)
                embed.set_footer(text='Type in the name of the section you would like to explore')
                await ctx.send(embed=embed)
                def check(m):
                    return m.content.lower() in ['experience','locations'] and m.channel == channel
                msg = await bot.wait_for('message',check=check)
                if msg.content.lower() == 'experience':
                    embed = discord.Embed(title='Foraging Experience',description='This is a guide on the most common and efficient ways to gain foraging experience',color=discord.Color.blue())
                    disc = """
                    1) Epic/Legendary Ocelot Pet - Provides a +30 Foraging Wisdom bonus
                    2) Toil Reforge - Provides a +1/2/3/4/5/6 Foraging Wisdom bonus based on the rarity of the axe used
                    3) Foraging XP Boost III Potion - Provides a +20 Foraging Wisdom bonus
                    4) Booster Cookie - Provides a +25 Foraging Wisdom bonus
                    """
                    disc1 = "For all of the methods listed below, you will want to equip yourself with a Treecapitator with the Toil reforge and Efficancy 5 for the method to work effectively"
                    disc2 = "Equip yourself with your Treecapitator, Young Dragon Armor, and an AOTE/AOTV and head to the Dark Thicket, where you can mine down the Dark Oak Trees. You will want to teleport around or run around to each tree as this method has lots of competition."
                    disc3 = "Equip yourself with your Treecapitator, Young Dragon Armor, and an AOTE/AOTV and head over to the Jungle Island, where you can mine down the Jungle Trees. While there isn't as much competition as the Dark Thicket, the trees in the Jungle Island has less connected logs than the trees in the Dark Thicket."
                    disc4 = "For this method you will need a Treecapitator, Jungle Spalings, and Enchanted Bone Meal. Put the Saplings in your first hotbar slot, the bone meal in your second hotbar slot, and your Treecapitator in your third hotbar slot, and proceed to cycle through them. On your Island, place the Saplings in a 2x2 grid, use the bone meal, and mine it with a Treecapitator. This is by far one of, if not the most effcient method to gain Foraging XP. Credit for Method C goes to `Something like that` - https://youtu.be/Asgr8XtrU00"
                    embed.add_field(name='XP Boosts',value=disc,inline=False)
                    embed.add_field(name='Foraging Methods',value=disc1,inline=False)
                    embed.add_field(name='Method A',value=disc2,inline=False)
                    embed.add_field(name='Method B',value=disc3,inline=False)
                    embed.add_field(name='Method C',value=disc4,inline=False)
                    embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 'locations':
                    embed = discord.Embed(title='Foraging Locations',description='All the Foraging locations are located on The Park, and are Seperated by type of Log',color=discord.Color.blue())
                    disc = "The Spawnpoint of the Park. In this section, you will find Birch Trees and the Rainmaker."
                    disc1 = "A cave holding 3 different types of wolves. The enterence to this cave is located behind a wall located inside the Waterfall in the Birch Park. The wall will require a Superboom TNT to break."
                    disc2 = "This location has Spruce Trees. It also holds the Melancholic Viking NPC and Gustave's Wood Race."
                    disc3 = "This location has the Dark Oak Trees. The Trials of Fire can also be found here."
                    disc4 = "This location is home to Acacia Trees. You will also find the Melody NPC along with her harp and Master Tactician Funk Merchant NPC."
                    disc5 = "The highest location in the Park. Home to Jungle Trees and the Romero and Juliet quest."
                    embed.add_field(name='Birch Park',value=disc,inline=False)
                    embed.add_field(name='Howling Cave',value=disc1,inline=False)
                    embed.add_field(name='Spruce Woods',value=disc2,inline=False)
                    embed.add_field(name='Dark Thicket',value=disc3,inline=False)
                    embed.add_field(name='Savanna Woodland',value=disc4,inline=False)
                    embed.add_field(name='Jungle Island',value=disc5,inline=False)
                    embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                    await ctx.send(embed=embed)
            elif msg.content.lower() == 'fishing':
                embed = discord.Embed(title='Fishing Catagories',description='',color=discord.Color.blue())
                disc = """
                __Select a Fishing Catagory to view information__

                Experience
                Gear Progression
                Locations
                Trophy Fishing
                """
                embed.add_field(name='Options',value=disc,inline=False)
                embed.set_footer(text='Type in the name of the section you would like to explore')
                await ctx.send(embed=embed)
                def check(m):
                    return m.content.lower() in ['experience','gear progression','locations','trophy fishing'] and m.channel == channel
                msg = await bot.wait_for('message',check=check)
                if msg.content.lower() == 'experience':
                    embed = discord.Embed(title='Fishing Experience',description='This is a guide on the most common and efficient ways to gain fishing experience',color=discord.Color.blue())
                    disc = """
                    1) Legendary Squid Pet - Provides a +30 Fishing Wisdom bonus.
                    2) Booster Cookie - Provides a +25 Fishing Wisdom bonus.
                    3) Fishing XP Boost III Potion - Provides a +20 Fishing Wisdom bonus.
                    4) Mayor Marina - Provides a +50 Fishing Wisdom bonus when elected with the Fishing XP Buff perk.

                    Side Note - It is useful to also get ones Sea Creature Chance up as killing Sea Creatures gains more xp than other types of fish.
                    """
                    disc1 = """
                    A commonly used method to level fishing is too gain XP by using Fishing Minions. It can cost somewhere in the likes of 30-50m coins for 25-30 t11 Fishing Minions but is useful as they gain XP passively. Other ways to boost XP production is through Minion Fuel, Super Compactors, Larger Chests, and a Beacon. Please note that Diamond Spreading is not recomeneded as diamonds take up space in the minion, reducing efficancy.
                    """
                    disc2 = """
                    __Level 0-20__: Fish in the hub, Spiders Den, or Park.

                    __Level 20-30__: Lava Fish in the Crystal Hollows.

                    __Level 30-50__ Lava Fish in the Crimson Isle.
                    """
                    embed.add_field(name='XP Boosts',value=disc,inline=False)
                    embed.add_field(name='Fishing Minions',value=disc1,inline=False)
                    embed.add_field(name='XP Gain Progression',value=disc2,inline=False)
                    embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 'gear progression':
                    embed = discord.Embed(title='Fishing Gear Progression',description='This guide includes information on how to progress as a fisherman',color=discord.Color.blue())
                elif msg.content.lower() == 'Locations':
                    embed = discord.Embed(title='Fishing Locations',description='Information on the various places you can fish',color=discord.Color.blue())
                    embed.add_field(name='Wilderness',value='Located in the Hub southeast of spawn, this is one of the first places new players should fish.',inline=False)
                    embed.add_field(name='The Park',value='In the Birch Park, a river flows through there where players often fish along with a rainmaker to spawn squids',inline=False)
                    embed.add_field(name="Spider's Den",value='Another common place to fish due to the naturally spawning rain',inline=False)
                    embed.add_field(name='Crystal Hollows',value='Players often fish here because of the higher XP rates from Sea Creatures as well as Worm Fishing in the Precursor Ruins.',inline=False)
                    embed.add_field(name='Crimson Isle',value='An expansive area where you can lava fish at basically any lava pool unless special mobs are desired such as the Plhlegblast Pool',inline=False)
                    embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 'trophy fishing':
                    embed = discord.Embed(title='Trophy Fishing',description='Trophy Fishing is a form of Lava Fishing where the player attempts to collect all the trophy fish. Each type of Trophy Fish has 4 rarities, Bronze, Silver, Gold, and Diamond.',color=discord.Color.blue())
                    disc = """
                    **Novice**
                    For novice, you need to catch 15 Bronze tier fish.
                    I found, the easiest route for this was to catch every fish other than Obfuscated 3 and 2 Location fish (skeleton, moldfin, soul and Karate fish)
                    You unlock the Bronze Hunter Armor by doing this, which makes getting trophy fish much easier!

                    **Adept**
                    For Adept, you need to catch ALL 18 SILVER tier fish!
                    This shouldn't be too difficult, if you're lucky. Although the hardest ones to get are the Location fish
                    (skeleton, moldfin, soul and Karate fish) and the Obfuscated 2 and 3 Fish, so try get those out the way first!
                    You get the Silver Hunter armor, which prevents you from getting sea creatures, and gives you a 5% trophy fish chance!
                    """
                    disc1 = """
                    **Expert**
                    For Expert, You need 18 gold tiered fish.
                    You get the Golden Hunter armor, which prevents you from getting sea creatures, and gives you a 10% trophy fish chance!

                    **Master**
                    For Master, You need 18 Diamond tiered fish... (good luck.)
                    You get the Diamond Hunter armor, which prevents you from getting sea creatures, and gives you a 15% trophy fish chance!
                    """
                    disc2 = """
                    **Below are all the trophy fish along with locations to catch them**
                    Sulphur Skitter: Caught near Sulphur Blocks
                    Obfuscated 1 (weird character name): Caught with Corrupted Bait
                    Obfuscated 2 (weird character name): Caught with Obfuscated 1 as bait
                    Obfuscated 3 (weird character name): Caught with Obfuscated 2 as bait (what a pain)
                    Gusher: Caught after a volcano eruption
                    Blobfish: caught everywhere
                    Steaming-Hot Flounder: Caught near the geysers in the volcano (steam coming from lava)
                    Slugfish: Bobber must be active for 30 seconds
                    Golden Fish: Golden head swimming in the lava
                    """
                    disc3 = """
                    Lavahorse: Caught everywhere
                    Mana ray: Lured by having at least 1200 mana
                    Volcanic Stonefish: found in blazing volcano
                    Vanille: Only caught with Starter Lava rod with no enchantments
                    Skeleton Fish: found in burning desert
                    Moldfin: Found in mystic Marsh
                    Soul Fish: Found in the stronghold
                    KarateFish: found in the dojo
                    Flying fish: Caught when 8 blocks above lava
                    """
                    disc4 = """
                    There are 4 Fish Rarities, Bronze, Silver, Gold and Diamond, each one being rarer than the last. You don't need to do anything differently to get the rarities, its just rng.
                    Bronze - 72.8%
                    Silver - 25%
                    Gold - 2%
                    Diamond - 0.2%
                    """
                    disc5 = """
                    Make sure to use Hot bait while fishing, its cheap to make and helps you get more, rarer trophy fish

                    Since Sulphur turns ALL mobs into corrupted mobs 100% of the time, you have a chance to get Obfuscated 1 fish (and corrupted fragments) from every Sea creature you fish up, (they are much more powerful though) meaning you dont need to use Corrupted bait!

                    For slug-fish, reel out your rod and wait 30 seconds, ignore when any fish bites and wait until after 30 seconds, then reel in the next fish you see (you can change your SBE fishing timer if you have that), very easy way to get it this way!

                    For the flying-fish, I found it easier to fish up while the lava is at the top of the volcano, as you stand at the top and fish into the lava. If you want to grind it while the volcano isnt erupting, I found a good spot to do so. Go to -384 199 -761 and stand on the ledge, if you're at the right spot you can look down and fish into the small pond below.
                    """
                    disc6 = """
                    For the SoulFish, any of the lava pools infront of spawn work fine (as its an epic fish, it does take a while to catch, took me around 20-30 mins)

                    For the Karate Fish, I found more success around the side of the Dojo, (as its an epic fish, it does take a while to catch, took me around 20-30 mins) Cords: -220 108 -565

                    For slug-fish, reel out, ignore when the fish bites and wait, they will bite again after a while, very easy way to get it!
                    """
                    embed.add_field(name='Trophy Fish Rarities',value=disc4,inline=False)
                    embed.add_field(name='Trophy Fish Ranks',value=disc,inline=False)
                    embed.add_field(name='Trophy Fish Ranks Cont.',value=disc1,inline=False)
                    embed.add_field(name='Trophy Fish Types',value=disc2,inline=False)
                    embed.add_field(name='Trophy Fish Types Cont.',value=disc3,inline=False)
                    embed.add_field(name='Fishing Tips',value=disc5,inline=False)
                    embed.add_field(name='Fishing Tips Cont.',value=disc6,inline=False)
                    embed.set_footer(text='Written by ItsHypers#3032 with help from Dradonhunter11 and Dr_DW',icon_url='https://images-ext-1.discordapp.net/external/SmYrqmCKJli_LNjpbui4aTMtkTZeoS6p5Cw1bLExgNs/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/561054408348270593/a_23d2a2f189e3110eb988d0d0b2d9280a.gif')
                    await ctx.send(embed=embed)
            elif msg.content.lower() == 'enchanting':
                embed = discord.Embed(title='Enchanting Guide',description='This is a guide on how to quickly and efficiantly gain enchanting experience.',color=discord.Color.blue())
                disc = """
                1) Epic/Legendary Gaurdian Pet - Provides a +30 Enchanting Wisdom bonus.
                2) Booster Cookie - Provides a +25 Enchanting Wisdom bonus.
                3) Enchanting XP Boost III Potion - Provides a +20 Enchanting Wisdom bonus.
                """
                disc1 = """
                The most common and recomended method to gain enchanting xp in the Experimentation Table unlocked at Enchanting Level 10. There are 3 different Experiments in the Experimentation Table:
                **Superpairs:** This is the main experiment. It is a memory matching game where you can match pairs together for experience and special rewards, the higher the tier, the greater the awards.
                **Chronomatron:** As an addon, it grants experience and extra clicks for the main experiment. This is a memory based color sequence game. Players have to remember and repeat the sequence. The more sequences remembered the more clicks rewarded.
                **Ultrasequencer:** As an addon, it grants experience and extra clicks for the main experiment.This is a memory based number sequence game. Players have to remember and repeat the sequence. The more sequences remembered the more clicks rewarded.

                It is recomeneded to have a mod such as SBA, Skytils, NEU, or SBE for experiments.
                """
                embed.add_field(name='XP Boosts',value=disc,inline=False)
                embed.add_field(name='Experimentation Table',value=disc1,inline=False)
                embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                await ctx.send(embed=embed)
            elif msg.content.lower() == 'alchemy':
                embed = discord.Embed(title='Alchemy Guide',description='This is a guide on how to quickly and efficiantly gain alchemy experience.',color=discord.Color.blue())
                disc = """
                1) Booster Cookie - Provides a +25 Alchemy Wisdom bonus.
                2) Alchmey XP Boost III Potion - Provides a +20 Alchemy Wisdom bonus.
                3) Spider SLayer Level 8 - Provides a +10 Alchemy Wisdom bonus.

                While doing alchemy, it is recomeneded to use a level 1 Legendary Sheep Pet so that it levels up along side you, making back some of the money spent on reasorces for alchemy.
                """
                disc1 = f"""
                Alchemy XP is mainly gained by brewing potions, brewing ALOT of potions. So the most common, cost effective, and mental capacity effective method is too place down several Brewing Stands next to water. The most commonly used ingredient used for alchemy xp in enchanted sugarcane, currently priced at `{round(bazaardata['ENCHANTED_SUGAR_CANE']['buyPrice'],2)}` a piece. It takes several hundred of these too max the skill. First place in your netherwart, then the enchanted sugarcane, and finally enchanted glowstone. Enchanted glowstone is very cheap and it increases the NPC sell price of the potions you make. Selling the potions can help recouperate some of the cost that was spent on the enchanted sugarcane.
                """
                embed.add_field(name='XP Boosts',value=disc,inline=False)
                embed.add_field(name='Brewing',value=disc1,inline=False)
                embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                await ctx.send(embed=embed)
            elif msg.content.lower() == 'taming':
                embed = discord.Embed(title='Taming Guide',description='This is a guide on how to gain taming experience.',color=discord.Color.blue())
                disc = """
                Taming XP is gained by gaining experience in other skills while the player has a pet active. While it is not fully passive, it is considered to be a passive skill. You cannot directly boost the XP gain of this skill (Except a Booster Cookie) but you can boost taming xp gain by boosting XP gain in other skills
                1) Booster Cookie - Provides a +25 Skill Wisdom bonus.
                2) Skill XP Boost III Potion - Provides a +20 Skill Wisdom bonus.
                3) Skill XP Boost Pets such as the Rabbit Pet, Ocelot Pet, Guardian Pet, Silverfish Pet, and Wolf Pet - Provides a +30 Skill Wisdom bonus.

                No matter what you do, just remember too have a pet equiped at all times.
                """
                embed.add_field(name='XP Bonus',value=disc,inline=False)
                embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                await ctx.send(embed=embed)
        elif msg.content.lower() == 'dungeons':
            embed = discord.Embed(title='Dungeon Catagories',description='',color=discord.Color.blue())
            disc = """
            __Select a catagory to view information__

            Information
            Entrance
            F1 / M1 (Either one works)
            F2 / M2
            F3 / M3
            F4 / M4
            F5 / M5
            F6 / M6
            F7 / M7
            """
            embed.add_field(name='Options',value=disc,inline=False)
            embed.set_footer(text='Type in the name of the section you would like to view information for')
            await ctx.send(embed=embed)
            def check(m):
                return m.content.lower() in ['information','entrance','f1','m1','f2','m2','f3','m3','f4','m4','f5','m5','f6','m6','f7','m7'] and m.channel == channel
            msg = await bot.wait_for('message',check=check)
            if msg.content.lower() == 'information':
                embed = discord.Embed(title='Dungeons Introduction',description='A basic guide on the inner workings of dungeons',color=discord.Color.blue())
                disc = """
                Dungeons are PvE raid activities in which a team of 2 to 5 players work together to defeat mobs within a procedurally generated series of rooms, ending in a boss fight. Players are rewarded based on their performance within the dungeon with Dungeoneering/Catacombs XP and items within chests. The rewards scale up with the difficulty of the dungeon; the more difficult missions can drop some of the strongest items in the game. There are 5 classes; Tank, Berserk, Archer, Mage, Healer
                There are the Catacombs and its Master Mode.
                Only Entrance has a non catacomb level requirement at Combat XV(15), the rest require certain catacomb levels
                By doing dungeons you gain Catacombs and Class experience both buff your stats and classes also give special abilities depending on the class.
                """
                disc1 = """
                Within each Dungeon, the following special rooms will always generate:

                1 starting room - Green Room 🟢
                At least 2 puzzle rooms - Purple Room 🟣
                1 mini-boss room - Yellow Room 🟡
                1 Fairy room - Pink Room 🔻
                1 Blood room - Red Room 🔴
                1 Trap room (Floor 3+ only) - Orange Room 🟠
                The rest of the space is filled in with normal rooms - Brown Rooms 🟤
                """
                disc2 = """
                Dungeons are completed in grades, the higher the grade you complete a dungeon in, the more experience you get(catacombs and class) and the more higher tier chests you can open. From F5-M7 S+ will allow you to have a bedrock chest and the bedrock chest has the most powerful and profitable items in the entire game as well as higher essence which can be used to dungeonise and star items which will give those items a powerful stat in dungeons, essence can also be used in the essence shop at Malik
                The grades are as follows:
                **S+, S, A, B, C, D, F**
                The normal (🟤) rooms and the puzzle room (🟣) will have secrets, collecting secrets will increase your grade in dungeons. These secrets are in fixed positions in rooms and you can use mods to find them in dungeons(my personal recommendation is DungeonRooms).
                Finding secrets can give you items or blessings, blessings give you buffs.
                """
                disc3 = """
                Each star gives 10% stat boost; The following stats are boosted by both Dungeon levels and stars:

                ❤ Health
                ❈ Defense
                ❁ Strength
                ❁ Damage
                ✦ Speed
                ☠ Crit Damage
                ✎ Intelligence
                α Sea Creature Chance
                ✧ Pristine
                ⸕ Mining Speed
                ☘ Mining Fortune
                The following stats are only boosted by stars:

                ✯ Magic Find
                ❂ True Defense
                ☣ Crit Chance
                ⚔ Bonus Attack Speed
                ⫽ Ferocity
                ๑ Ability Damage
                For the following stats, it is unknown how they are boosted:

                ♣ Pet Luck
                ☘ Farming Fortune
                ☘ Foraging Fortune
                """
                disc4 = """
                Entrance: Combat 15
                Floor 1: Catacombs 1
                Floor 2: Catacombs 3
                Floor 3: Catacombs 5
                Floor 4: Catacombs 9
                Floor 5: Catacombs 14
                Floor 6: Catacombs 19 (recommended 22+)
                Floor 7: Catacombs 24 (recommended 28+)

                Master Mode Floor 1: Catacombs 24 (recommended 30+)
                Master Mode Floor 2: Catacombs 26 (recommended 33+)
                Master Mode Floor 3: Catacombs 28 (recommended 35+)
                Master Mode Floor 4: Catacombs 30 (recommended  not doing lmao)
                Master Mode Floor 5: Catacombs 32 (recommended 40+)
                Master Mode Floor 6: Catacombs 34 (recommended 44+)
                Master Mode Floor 7: Catacombs 36 (recommended 45+)
                """
                disc5 = """
                Currently, there are 5 playable classes within Dungeons:

                >The Healer uses their healing abilities to keep the team alive and dealing damage.
                >The Berserk specialises in close-quarter combat, relying on life-steal and high melee damage to defeat enemies.
                >The Mage relies on high Intelligence levels and magic damage to shut enemies down with magic weapons.
                >The Archer's ranged weapons allow it to take down high-health enemies from a safe distance.
                >The Tank keeps the team safe by drawing enemy attention away from and taking damage on behalf of more vulnerable members of the team.

                Each class gains class-specific buffs and abilities within Dungeons. The power of those buffs and abilities are increased by leveling up those classes. Class abilities can be used with the Dungeon Orb, or by pressing the drop (ultimate) or drop stack (regular) key with an Orb in inventory.
                """
                disc6 = """
                The Undead Mobs in the Blood Rooms of F5, F6, and F7 have special attributes.
                -Boomers: Have TNT for heads. Explode on kill. Drop Superboom TNT.
                -Stormy: Have lighting attacks. Occasionally drop Thunderlord 6 enchantment books.
                -Healthy: Have extra HP. Occasionally drop Healng Tissue.
                -Golden: Wear golden armor. Drop golden essence
                -Stealthy: Invisible. 
                -Speedy: Very fast. Drop Dungeon Potions based on the dungeon floor(eg. Floor 6 Speedy Mobs can drop Dungeon 6 Potions)
                """
                disc7 = """
                -Creeper Beams: Shooting 2 sea lanterns in a row with a bow causes them to be connected with a guardian beam, so you want 4 beams to pass through the creeper in the middle of the room
                -Teleport Maze: There are multiple teleport paths that take the player throughout the room. Doing this for long enough will eventually take the player to the chest in the middle.
                -Three Weirdos: This is a riddle puzzle as you have to read the text and solve the riddle. Mods often help simplify this process.
                -Water board: Using a set of 7 levers, the player has to open all the gates but getting water to flow to them
                -Tic Tac Toe: The player has to tie a game of Tic Tac Toe. There is also a secret in this room.
                """
                disc8 = """
                -Higher or Lower: If the entrance to this room is at the top, the player has kill the Blazes from highest HP to lowest HP, and vice versa for when the entrance is at the bottom. There is also a secret in this room.
                -Boulder: Pushing buttons clears the way too the chest. It is possible to make the path to the chest immpossible to pass however.
                -Ice Fill: Walking over ice turns it into packed ice, and completley filling in all 3 stages opens up the chest.
                -Ice Path. Push the Silverfish to the ice wall blocking the chest. The Silverfish only goes in pne direction at a time
                -Quiz: Answer the 3 questions. These questions are always about skyblock.
                -Bomb Defuse: 2 people are required for this puzzle. After stepping on the pressure plates, players have to communicate too solve the puzzles, as the solution is on the right. This puzzle has a 2 minute time limit.
                """
                embed.add_field(name='Introduction',value=disc,inline=False)
                embed.add_field(name='Dungeon Rooms',value=disc1,inline=False)
                embed.add_field(name='Dungeon Score',value=disc2,inline=False)
                embed.add_field(name='Dungeon Stars',value=disc3,inline=False)
                embed.add_field(name='Dungeon Level Requirements',value=disc4,inline=False)
                embed.add_field(name='Classes',value=disc5,inline=False)
                embed.add_field(name='Blood Room Modifiers',value=disc6,inline=False)
                embed1 = discord.Embed(title='Dungeon Puzzles',description='Puzzles contribute a lot too the score in dungeons, as a failed puzzle means the loss of 14 points. Below is a short guide on each puzzle:',color=discord.Color.blue())
                embed1.add_field(name='Puzzles Pt. 1',value=disc7,inline=False)
                embed1.add_field(name='Puzzles Pt. 2',value=disc8,inline=False)
                embed.set_footer(text='Written by Pucapi#1168',icon_url='https://images-ext-2.discordapp.net/external/qigAY3wUsa8L-2CMGxA4kk-4rrG1Q0qD8EaaeyGGxHY/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/675106662302089247/44dd09251ad48c2b14c185e3ca598b21.png?width=676&height=676')
                embed1.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                await ctx.send(embed=embed)
                await ctx.send(embed=embed1)
            elif msg.content.lower() == 'entrance':
                embed = discord.Embed(title='Dungeon Floor Entrance | The Watcher',description='The Entrance is the first dungeon floor the player has access too. The boss of this floor is The Watcher(He is present in the other floors as well) and the player is required too have at least Combat Level 15 too enter',color=discord.Color.blue())
                disc = """
                The entrance is the smallest Dungeon Floor, standing at a room size classified as "Tiny."
                Players automatically respawn after 50 seconds of death.
                This floor does NOT have a trap room.
                The Blood Room on this floor is the boss room.
                This Floor does NOT have a Master Mode variant
                This floor can spawn with a few of 5 puzzles(See Dungeons>Information for a guide on each puzzle):
                -Creeper Beams
                -Teleport Maze
                -Three Weirdos
                -Water board
                -Tic Tac Toe
                """
                disc1 = """
                The Watcher is pretty straightforward. Once your party unlocks the Blood Room the Watcher will begin to spawn Undead which are Low HP high defense mobs, meaning they have less HP but they take less damage. If your party kills all the mobs the Watcher will let you "pass." For this floor that means you beat it but for the rest of the floors the Watcher will ignite a portal to the Boss Room. If you are having trouble clearing the Blood Room, use an AOTE/AOTV or any other type of teleport ability and teleport on top of the opposing blood door. From there, use a bow to kill off the Undead.
                """
                disc2 = """
                Berserker: Strong Dragon Armor/Aspect of the Dragons/Rare Enderman/Uncommon Griffin
                Mage: Mage isn't really recomended since good Mage Weapons arent really available at this level
                Archer: Strong Dragon Armor/Runaans/Hurricane/Venoms Touch(Preferably upgraded)/Rare Tiger/Uncommon Griffin
                Tank: Old Dragon/Holy Dragon Armor/Aspect of the Dragons/Rare Blue Whale
                Healer: Strong Dragon Armor/Aspect of the Dragons/Rare Blue Whale
                """
                embed.add_field(name='General Info',value=disc,inline=False)
                embed.add_field(name='The Watcher',value=disc1,inline=False)
                embed.add_field(name='Gear Guide',value=disc2,inline=False)
                embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                await ctx.send(embed=embed)
            elif msg.content.lower() in ['f1','m1']:
                embed = discord.Embed(title='Dungeons Floor 1 | Bonzo',description='Floor 1 is the second Dungeons floor and the first Master Mode floor the player has access to. The Boss of this floor is Bonzo and this floor has a requirement of Catacombs Level 1 and Catacombs Level 24 for Normal Mode and Master Mode respectively',color=discord.Color.blue())
                disc = """
                Depending on the score earned, up to 5 chests will be available to unlock at the end of the Dungeon
                The player will respawn after 50 seconds of dying
                This floor can spawn with a few of 5 puzzles(See Dungeons>Information for a guide on each puzzle):
                -Creeper Beams
                -Teleport Maze
                -Three Weirdos
                -Water board
                -Tic Tac Toe
                """
                disc1 = """
                Bonzo has 2 phases:
                **Phase 1:** Bonzo does not attack the player, but rather runs around at the speed of sound while spawning undead mobs to kill your party.
                **Phase 2:** After depleting Bonzo's first healthbar, Bonzo stops summoning Undead, equips a weapon similar or exactly the same to the Bonzo Staff and begins attacking the party. When Bonzo is shooting a bunch of Balloons while in the middle or Wither Skulls while on top of a pillar, standing behind an opposing pillar until Bonzo stops is a vaible method of survival. Bonzo has the same amount of HP as the first phase.
                """
                disc2 = """
                In Master Mode, Bonzo has more HP and deals more damage. His Undead also have more HP. In the first phase, the Tank should attract the Undead and should lifesteal off them(Using the Syphon enchantment). Meanwhile the DPS classes shouls be damaging Bonzo to destory his first Healthbar. During the Second phase, a DPS class such as the Archer should kill all the Undead so that they aren't an issue anymore, and the Tank should prepare too take alot of damage as they support the other party members.
                """
                disc3 = """
                Archer: Strong/unstable/young with a bow such as runaans, hurricane, or venoms touch, enderman/tiger/griffin/skeleton/wither skeleton pet
                Berserker: Strong/unstable/young dragon with an aspect of the dragons, enderman/tiger/lion/griffin/wither skeleton pet
                Mage: Wise dragon+dark goggles with a bonzo staff and/or frozen scythe, sheep pet
                Tank: Heavy armor or old dragon armor, any weapons, tanky pet such as whale or turtle
                Healer: Strong/unstable/young+mender helmet, aspect of the dragons, can use either damage pet or tanky pet
                """
                disc4 = """
                Archer: Necron+golden bonzo head or tarantula helm/reaper mask, juju or terminator, baby yeti/ender dragon/golden dragon pet
                Berserker: Necron+golden bonzo head or tarantula/reaper mask, juju/terminator or axe of the shredded+giant sword/valkyrie/claymore, baby yeti/ender dragon/golden dragon pet
                Mage: Storm+wither goggles, wither blade/giant sword/claymore, sheep/ender dragon/golden 
                Tank: Goldor+reaper mask, livid dagger(possibly astraea), whale pet
                Healer: Necron+mender crown, juju or term, baby yeti/whale/ender dragon/golden dragon pet
                """
                embed.add_field(name='General Info',value=disc,inline=False)
                embed.add_field(name='Bonzo',value=disc1,inline=False)
                embed.add_field(name='Normal Mode Gear Guide',value=disc3,inline=False)
                embed.add_field(name='Master Mode',value=disc2,inline=False)
                embed.add_field(name='Master Mode Gear Guide',value=disc4,inline=False)
                embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki • Gear Guide written by AlienTheHoward#2188',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                await ctx.send(embed=embed)
            elif msg.content.lower() in ['f2','m2']:
                embed = discord.Embed(title='Dungeons Floor 2 | Scarf',description='Floor 2 is the third Normal Mode floor and the second Master Mode floor. The Boss on this floor is Scarf and this floor has a Catacombs Level Requirement of 3 and 26 for Normal Mode and Master Mode respectively',color=discord.Color.blue())
                disc = """
                Depending on the score earned, up to 5 chests will be available to unlock at the end of the Dungeon
                The player will respawn after 95 seconds of dying
                This floor can spawn with a few of 6 puzzles(See Dungeons>Information for a guide on each puzzle):
                -Creeper Beams
                -Teleport Maze
                -Three Weirdos
                -Water board
                -Tic Tac Toe
                -Higher or Lower
                """
                disc1 = """
                Scarf has 2 phases:
                **Phase 1:** The four Tombstones on the sides of the Boss room will break open and spawn four different mobs. The Undead Warrior is supposed to resemble a berserker in that it weilds a sword and has an ability that allows it too teleport toward its enemies. The Undead Mage is a Mage and will attack you with ranged magic attacks. The Undead Archer is an Archer and will shoot you with a bow. Finally the Undead Priest is a Healer class mob that constantly heals Scarf.
                **Phase 2:** After you defeat the 4 Undeads, Scarf will begin attacking the player and all 4 Undeads will respawn. For players starting out killing all 4 then targeting Scarf will probably be the best way to defeat the boss, but if possible, targeting the Undead Priest and then Scarf without caring about the other Undeads is also a viable method.
                """
                disc2 = """
                In Master Mode, Scarf and his Undeads have more HP and deal way more damage. 2 of each Undead will spawn, meaning you have 2 Undead Warrior's too deal with instead of one. The Undead Warriors teleport ability is especially brutal as it will kill any mid-game player who isn't a tank. Unless your party can survive the barage of the 8 Undeads, it would be better to kill the Undeads rather than ignoring them.
                """
                disc3 = """
                Archer: Strong/unstable/young with a bow such as runaans, hurricane, or venoms touch, enderman/tiger/griffin/skeleton/wither skeleton pet
                Berserker: Strong/unstable/young dragon with an aspect of the dragons, enderman/tiger/lion/griffin/wither skeleton pet
                Mage: Wise dragon+dark goggles with a bonzo staff and/or frozen scythe, sheep pet
                Tank: Heavy armor or old dragon armor, any weapons, tanky pet such as whale or turtle
                Healer: Strong/unstable/young+mender helmet, aspect of the dragons, can use either damage pet or tanky pet
                """
                disc4 = """
                Archer: Necron+golden scarf head, juju or terminator, baby yeti/ender dragon/golden dragon pet
                Berserker: Necron+golden scarf head or tarantula/reaper mask, juju/terminator or axe of the shredded+giant sword/valkyrie/claymore, baby yeti/ender dragon/golden dragon pet
                Mage: Storm+wither goggles, wither blade/giant sword/claymore, sheep/ender dragon/golden dragon
                Tank: Goldor+reaper mask, livid dagger(possibly astraea), whale pet
                Healer: Necron+mender crown, juju or term,baby yeti/ender dragon/golden dragon/whale
                """
                embed.add_field(name='General Info',value=disc,inline=False)
                embed.add_field(name='Scarf',value=disc1,inline=False)
                embed.add_field(name='Normal Mode Gear Guide',value=disc3)
                embed.add_field(name='Master Mode',value=disc2,inline=False)
                embed.add_field(name='Master Mode Gear Guide',value=disc4,inline=False)
                embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki • Gear Guide written by AlienTheHoward#2188',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                await ctx.send(embed=embed)
            elif msg.content.lower() in ['f3','m3']:
                embed = discord.Embed(title='Dungeons Floor 3 | The Professor',description='Floor 3 is the fourth Normal Mode floor and the third Master Mode floor. The Boss on this floor is The Professor and this floor has a Catacombs Level Requirement of 5 and 28 for Normal Mode and Master Mode respectively',color=discord.Color.blue())
                disc = """
                Depending on the score earned, up to 5 chests will be available to unlock at the end of the Dungeon
                The player will not automatically respawn
                The Trap Room will spawn on this Floor
                This floor can spawn with a few of 9 puzzles(See Dungeons>Information for a guide on each puzzle):
                -Creeper Beams
                -Teleport Maze
                -Three Weirdos
                -Water board
                -Tic Tac Toe
                -Higher or Lower
                -Boulder
                -Ice Fill
                -Ice Path
                """
                disc1 = """
                The Professor has 2 phases:
                **Phase 1:** The Professor does not attack the party, rather he has 4 Guardians, the Chaos Guardian, Healthy Guardian, Reinforced Guardian, and Laser Guardian. Each have unique abilities (All the information here - https://wiki.hypixel.net/The_Professor#Fight_Mechanics) but the main point are that if the party takes too long to kill the Guardians any dead Guardians will respawn with 80% HP.
                **Phase 2:** If all the Guardians are at 0 HP The Professor fuses with the Guardians and proceeds to attack the player as a flying Guardian. Water will also begin to fill the Boss Room slowly turning it into a fish tank. Once the boss reaches 1 HP, Necron kills The Professor, ending the boss fight and clearing the floor.
                """
                disc2 = """
                The Professor and his Guardians have more HP.
                Respawned Guardians gain 90% HP, and are respawned in 7 seconds.
                Just like with F2, a lot of the pressure falls on the Tank for keeping the team alive, as the Guardian Abilities are now something to worry about. Stay away from the Reinforced Guardian during it's TNT Rain ability and the Tank should wear a Spirit Mask when the Chaos Guardian is about to unleash it's Body Slam ability(And Discharge maybe).
                """
                disc3 = """
                Archer: Strong dragon with venoms touch or possibly a juju if the player can afford one and has unlocked one, enderman/tiger/griffin/skeleton pet
                Berserker: strong dragon with flower of truth, tiger/wither skeleton/griffin pet
                Mage: Wise dragon or zombie soldier with dark goggles, frozen scythe or bonzo staff
                Tank: Heavy armor or old dragon armor, any weapon, tanky pet like whale or turtle 
                Healer: Strong+mender helmet, aspect of the dragons, can use either damage pet or tanky pet
                """
                disc4 = """
                Archer: Necron+golden/diamond professor head, terminator, baby yeti/ender dragon/golden dragon pet
                Berserker:  Necron+golden/diamond professor head, juju/terminator or axe of the shredded+giant sword/valkyrie/claymore, baby yeti/ender dragon/golden dragon pet
                Mage: Storm+wither goggles, wither blade/giant sword/claymore, sheep/ender dragon/golden dragon pet
                Tank: Goldor+reaper mask, astraea, whale pet
                Healer:  Necron+mender crown, juju or term,baby yeti/ender dragon/golden dragon/whale
                """
                embed.add_field(name='General Info',value=disc,inline=False)
                embed.add_field(name='The Professor',value=disc1,inline=False)
                embed.add_field(name='Normal Mode Gear Guide',value=disc3,inline=False)
                embed.add_field(name='Master Mode',value=disc2,inline=False)
                embed.add_field(name='Master Mode Gear Guide',value=disc4,inline=False)
                embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki • Gear Guide written by AlienTheHoward#2188',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                await ctx.send(embed=embed)
            elif msg.content.lower() in ['f4','m4']:
                embed = discord.Embed(title='Dungeons Floor 4 | Thorn',description='Floor 4 is the fifth Normal Mode floor and the fourth Master Mode floor. The Boss on this floor is Thorn and this floor has a Catacombs Level Requirement of 9 and 30 for Normal Mode and Master Mode respectively',color=discord.Color.blue())
                disc = """
                Floor 4 is by far the mosted hated of the Catacombs floors due to the Thorn Bossfight being the most annoying videogame bossfight ever programmed.
                Depending on the score earned, up to 5 chests will be available to unlock at the end of the Dungeon
                The player will not automatically respawn
                The Trap Room will spawn on this Floor
                This floor can spawn with a few of 9 puzzles(See Dungeons>Information for a guide on each puzzle):
                -Creeper Beams
                -Teleport Maze
                -Three Weirdos
                -Water board
                -Tic Tac Toe
                -Higher or Lower
                -Boulder
                -Ice Fill
                -Ice Path
                """
                disc1 = """
                Thorn never actually attacks the player, instead tens, if not, hundreds of Animal Spirits attack the player. Alone these guys do little damage but keep in mine, there are alot of them. The best plan of action is either a) Run around with an AOTE/AOTV and a healing item or b) Teleport into the stands. The issue with standing in the stands however, is that Spirit Bats like to come attack you, so either run like a goose or use the Decoy Item(Which can be dropped when clearing Dungeon Floors). Either way avoid dying until the Spirit Bear spawns. You see, Thorn only has 4 hitpoints, but can only be damaged by the Spirit Bow dropped from the Spirit Bears. So you and your party will have to kill the Spirit Bear 4 times and shoot Thorn 4 times. Do note that as Thorn approaches the players position, he does have a tendency to turn around, causing most bow shots too miss(Also having high ping can cause the arrows too not connect at all).
                """
                disc2 = """
                In Master Mode, Thorn has 6 hitpoints, instead of 4. All the Spirit Animals have more HP and deal more damage, and 3 Spirit Bears spawn each time. However only after killing the last Spirit Bear will the party be awarded with the Spirit Bow. Since none of the mobs on this floor have ranged attacks as long as everyone has the skill of running away and can deal enough damage to kill 3 Spirit Bears in a timely fashion then much precedent doesnt have to be put on the Tank.
                """
                disc3 = """
                Archer: Strong dragon(or shadow assassin if unlocked through floor 5 carry), venoms touch or preferably a juju shortbow, wither skeleton/skeleton/griffin pet
                Berserker: Strong dragon(or shadow assassin if unlocked through floor 5 carry), flower of truth, wither skeleton/griffin pet
                Mage: Wise dragon or zombie soldier with dark goggles, spirit sceptre, sheep pet
                Tank: Heavy or old dragon armor, any weapon, whale or turtle pet
                Healer: Strong+mender helmet, any weapon, any pet
                """
                disc4 = """
                Archer:  Necron+golden/diamond thorn head, terminator, baby yeti/ender dragon/golden dragon pet
                Berserker: Necron+golden/diamond thorn head, terminator or axe of the shredded+giant sword/valkyrie/claymore, baby yeti/ender dragon/golden dragon pet
                Mage:  Storm+wither goggles, wither blade/giant sword/claymore, sheep/ender dragon/golden dragon
                Tank:  Goldor+reaper mask, astraea, whale pet
                Healer: Necron+mender crown, juju or term,baby yeti/ender dragon/golden dragon/whale
                """
                embed.add_field(name='General Info',value=disc,inline=False)
                embed.add_field(name='Thorn',value=disc1,inline=False)
                embed.add_field(name='Normal Mode Gear Guide',value=disc4,inline=False)
                embed.add_field(name='Master Mode',value=disc2,inline=False)
                embed.add_field(name='Master Mode Gear Guide',value=disc4,inline=False)
                embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki • Gear Guide written by AlienTheHoward#2188',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                await ctx.send(embed=embed)
            elif msg.content.lower() in ['f5','m5']:
                embed = discord.Embed(title='Dungeons Floor 5 | Livid',description='Floor 5 is the sixth Normal Mode floor and the fifth Master Mode floor. The Boss on this floor is Livid and this floor has a Catacombs Level Requirement of 14 and 32 for Normal Mode and Master Mode respectively',color=discord.Color.blue())
                disc = """
                Depending on the score earned, up to 6 chests will be available to unlock at the end of the Dungeon
                The player will not automatically respawn
                The Trap Room will spawn on this Floor
                This floor can spawn with a few of 9 puzzles(See Dungeons>Information for a guide on each puzzle):
                -Creeper Beams
                -Teleport Maze
                -Three Weirdos
                -Water board
                -Tic Tac Toe
                -Higher or Lower
                -Boulder
                -Ice Fill
                -Ice Path
                """
                disc1 = """
                When the player enters the Boss room, Livid greets the player and proceededs to turn into 8 versions of himself(Well he actually splits his soul up and possess 8 enderman using Thorn's Spirit). Althought there are 8 Livids, you only need to kill 1. Each Livid has a different color nametag, and the color of the nametag of the correct Livid corresponds with the color of the pattern on the celing in the middle of the room(You can also use mods such as DungeonsGuide to mark the correct Livid automatically). Killing the wrong Livid will cause that Livid to die but all the other Livids will geat a health boost. A common method used to fight Livid is teleporting up to a corner directly the left of where the player spawns in. From there the Tank attracs the Livids attention using the Jingle Bells item or the Castle of Stone ability. Meanwhile the party kills all the Livids.
                """
                disc2 = """
                Archer: Shadow assassin+golden livid head, juju shortbow, wither skeleton/skeleton/baby yeti pet
                Berserker: Shadow assassin+golden livid head, flower of truth and/or livid dagger, griffin/wither skeleton/baby yeti
                Mage: Wise dragon or zombie soldier+shadow goggles, spirit sceptre, sheep pet
                Tank: Old dragon(or necromancer lord if floor 6 completion through carry)+reaper mask, livid dagger with syphon or life steal, epic+ whale pet
                Healer: Shadow assassin+mender fedora, livid dagger and/or flower of truth, griffin/wither skeleton/whale pet
                """
                disc3 = """
                Pretty much the same as normal mode but Livid has more HP, deals more damage, and the party standson a different ledge. Livid also may change skin and colors of the clones, and killing the wrong clone now boosts the damage of the other clones.
                """
                disc4 = """
                Archer: Necron+golden/diamond livid head, terminator, baby yeti/ender dragon/golden dragon pet
                Berserker: Necron+golden/diamond livid head, terminator or axe of the shredded+giant sword/valkyrie/claymore, baby yeti/ender dragon/golden dragon pet
                Mage: Storm+wither goggles, wither blade/giant sword/claymore, sheep/ender dragon/golden dragon
                Tank: Goldor+reaper mask, astraea, whale pet
                Healer:  Necron+mender crown, term,baby yeti/ender dragon/golden dragon/whale
                """
                embed.add_field(name='General Info',value=disc,inline=False)
                embed.add_field(name='Livid',value=disc1,inline=False)
                embed.add_field(name='Normal Mode Gear Guide',value=disc2,inline=False)
                embed.add_field(name='Master Mode',value=disc3,inline=False)
                embed.add_field(name='Master Mode Gear Guide',value=disc4,inline=False)
                embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki • Gear Guide written by AlienTheHoward#2188',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                await ctx.send(embed=embed)
            elif msg.content.lower() in ['f6','m6']:
                embed= discord.Embed(title='Dungeon Floor 6 | Sadan',description='Floor 6 is the seventh Normal Mode floor and the sixth Master Mode floor. The Boss on this floor is Sadan and this floor has a Catacombs Level Requirement of 19 and 34 for Normal Mode and Master Mode respectively',color=discord.Color.blue())
                disc = """
                Depending on the score earned, up to 6 chests will be available to unlock at the end of the Dungeon
                The player will not automatically respawn
                The Trap Room will spawn on this Floor
                This floor can spawn with a few of 10 puzzles(See Dungeons>Information for a guide on each puzzle):
                -Creeper Beams
                -Teleport Maze
                -Three Weirdos
                -Water board
                -Tic Tac Toe
                -Higher or Lower
                -Boulder
                -Ice Fill
                -Ice Path
                -Quiz
                """
                disc1 = """
                The Sadan bossfight has 3 phases:
                **Phase 1:** Sadan  has a few dozen Terracotta Warriors that have 12 million HP and take reducded damage, as well as dealing a lot of damage with Flower of Truth style weapons. The strategy for this bossfight is for the Tank to stand in the middle of the room and lifsteal off the Terras while DPS classes damage the Terras and hopefully take them out. You either need to kill allof the Terras(They may respawn) or survive for about 2 minutes.
                **Phase 2:** 4 Giant Zombies, each with different abilities, fall into the bossroom. They are very easy to kill if 2-3 DPS classes are present.
                **Phase 3:** Sadan himself possesses a hybrid of the 4 Giants with all of the abilities. This is also very easy to kill.
                **Side Note:** There are 6 Golems sleeping in the boss room.  Killing them before the first phase will cause a 30 second delay, so people often kill them between the second and third phases to save time.
                """
                disc2 = """
                Archer: Shadow assassin+golden sadan head, juju shortbow, wither skeleton/skeleton/baby yeti pet
                Berserker: Shadow assassin+golden sadan head, juju or flower of truth+livid dagger, wither skeleton/baby yeti pet
                Mage: Necromancer lord+shadow goggles(or storm if unlocked), spirit sceptre or midas staff(not recommended), sheep pet
                Tank: Necromancer lord/perfect t12 armor+reaper mask, livid dagger, epic/leg blue whale
                Healer: Shadow assassin+mender fedora, livid dagger/juju, wither skeleton/griffin/baby yeti/whale
                """
                disc3 = """
                All mobs have increased health and damage.
                Giants can have multiple abilities(For example any Giant wearing boots canunleash a stomp attack).
                Giants can be revived in the third phase.
                """
                disc4 = """
                Archer: Necron+golden/diamond sadan head, terminator and scylla, ender dragon/golden dragon pet
                Berserker: Necron+golden/diamond sadan head, terminator and scylla or axe of the shredded+giant sword/valkyrie/claymore, baby yeti/ender dragon/golden dragon pet
                Mage: Storm+wither goggles, wither blade/giant sword/claymore, sheep/ender dragon/golden dragon
                Tank: Goldor+reaper mask, astraea, whale pet
                Healer: Necron+mender crown, term,baby yeti/ender dragon/golden dragon/whale
                """
                embed.add_field(name='General Info',value=disc,inline=False)
                embed.add_field(name='Sadan',value=disc1,inline=False)
                embed.add_field(name='Normal Mode Gear Guide',value=disc2,inline=False)
                embed.add_field(name='Master Mode',value=disc3,inline=False)
                embed.add_field(name='Master Mode Gear Guide',value=disc4,inline=False)
                embed.set_footer(text='Written by plebmaster21#0101 • Information obtained from the Official Hypixel Skyblock Wiki • Gear Guide written by AlienTheHoward#2188',icon_url='https://images-ext-1.discordapp.net/external/hQkKAlV9HWhepmwsFsbCrAKms5AMwUtfyIJ2qoALYOo/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/519985798393626634/db59ff8c287f8f706f6ed13ab49cd9df.png')
                await ctx.send(embed=embed)
            elif msg.content.lower() in ['f7','m7']:
                embed = discord.Embed(title='Dungeon Floor 7 | Necron, Storm, Goldor, and Maxor',description='Floor 7 is the final Normal and Master Mode Floor. This Floor has 4 bosses in Normal Mode and the secret 5th boss in Master Mode. The Catacombes level requirements are 24 for Normal Mode and 36 for Master Mode.',color=discord.Color.blue())
                embed1 = discord.Embed(title='Dungeon Floor 7 Cont.',description='Continutation from the previous Embed',color=discord.Color.blue())
                disc = """
                Depending on the score earned, up to 6 chests will be available to unlock at the end of the Dungeon
                The player will not automatically respawn
                The Trap Room will spawn on this Floor
                This floor can spawn with a few of 11 puzzles(See Dungeons>Information for a guide on each puzzle):
                -Creeper Beams
                -Teleport Maze
                -Three Weirdos
                -Water board
                -Tic Tac Toe
                -Higher or Lower
                -Boulder
                -Ice Fill
                -Ice Path
                -Quiz
                -Bomb Defuse
                """
                disc1 = """
                In this phase, there are two crystals on top of platforms, two players must grab those crystals and bring them to the pressure plates on the sides of the room. 

                If you are a mage, you can use a Jerry-Chine gun to boost yourself up to the crystal. (This is not recommended for other classes due to the massive mana cost of Jerry-Chine). Other classes can use the lava against the wall, and use a bonzo staff to launch themselves to the platform. Additionally, if you own spring boots, you can use those.

                After both crystals have been placed, one player (if there is a tank in the party, this is their job) must lure Maxor into the laser. A slime hat is very useful for this part, as Maxor deals true knockback, meaning shelmet will not work. After Maxor is in the laser, damage him until he becomes immune again. Then repeat the whole process again. If your party does very low damage, you may need to get the crystals a third time, but the process remains the same. This will complete phase 1.
                """
                disc2 = """
                When dropping down into phase 2, DPS classes should prioritize clearing out Wither Skeletons at of near the Green and Yellow Pillars.

                When you see the red countdown on your screen, all party members need to stand underneath one of the pillars or else Storm will one tap you(You can also use bonzo mask or wither cloak to block this). After Storm attacks, 2 players should go stand next to the green and yellow pads. The tank will then attract Storm and lure him underneath the green pillar(Slime hat is again useful here to make it easier to avoid the knockback). The player next to the green pad will then stand on the pad to crush Storm. You can then attack Storm for a short period, before he becomes invincible. Repeat the process once more to kill Storm. If Storm doesn't die in 2 pillars, there is the third blue pillar on the other side which is garunteed to kill him.

                After Storm is killed, go stand underneath the red pillar where the floor will break and you will drop down into phase 3. 
                """
                disc3 = """
                This phase is the one that a lot of new players find the most stressful. There are four separate sections of Terminals, or mini puzzles. Each section contains 4-5 Terminals, 1 Device, and 2 levers. While most players have mods with solvers, the puzzles are simple enough to do without them. Simply read the instructions at the top of the GUI, and complete what it tells you to do. 

                For the devices, each section has a different puzzle.
                Section 1 - Simon Says (Simple enough, I don't think I need to explain this one). 
                One person should type in chat that they'll do the Simon says device, and they should ignore all other terminals and go straight to the Simon says device, as it takes a long time to complete.
                Section 2 - Lights
                A large square of glowstone lamps with levers on them is located very high up in section 2, where you have to turn all the lamps on. The fastest way to do this is hit the 4 levers in the corners, and then the 2 in the middle.
                """
                disc4 = """
                Section 3 - Arrow Maze
                A bunch of arrows are in item frames on a wall. Rotate them until the block behind the item frame changes into a sea lantern. Repeat for all arrows.
                Section 4 - Targets
                A player must stand on the pressure plate somewhat up high, and shoot all of the green targets. Note, multiple players can shoot at the targets at the same time.

                After all four sections of terminals are complete, a gold door will drop down, where everyone must run inside. Goldor will then slowly approach, and if you get too close to him, you'll die. This section is all about DPS, however, note that Wither Impact does not damage Goldor. This phase relies heavily on the archer, as they will be dealing the most ranged damage. It is also helpful to have someone (usually the tank) hit Goldor with a last breath to lower his defence. After Goldor dies, phase 3 is complete. 
                """
                disc5 = """
                When you drop down into phase 4, all players will be suspended in the air while Necron breaks the floor underneath you. All party members will then be dropped into the lava. It is recommended that all party members jump over to the same side so that everyone can damage Necron. If there is a tank in the party, they should take Necron's aggro and then go into one of the corners in the iron pillars, so that the other party members can hit Necron without him moving too much.

                After enough damage is done to Necron, you will be blinded, and he will move to the centre platform. Here, you just damage him. After a certain amount of time, he will fly back towards the party, where you can just repeat the same thing described before. Necron can usually be killed in 2 phases, however, weaker parties may take longer.

                When Necron moves to the middle, players might follow in pursuit by jumping in the Lava. This is not reccomended for unexperience players.
                """
                disc6 = """
                Archer: Necron+golden/diamond necron head, juju or terminator, baby yeti/ender dragon/golden dragon/wither skeleton pet
                Berserker: Necron+golden/diamond necron head, juju/terminator or axe of the shredded+giant sword/valkyrie/dark claymore, wither skeleton/ender dragon/golden dragon/baby yeti pet
                Mage: Storm+wither goggles, hyperion(spirit sceptre if very low budget), sheep or whale pet
                Tank: Goldor+reaper mask, livid dagger(astraea if high budget), legendary whale pet
                Healer: Necron+mender crown, livid dagger/shadow fury+flower of truth/juju, wither skeleton/griffin/baby yeti/whale pet
                """
                disc7 = """
                The only real change is that Mobs have more HP and deal more damage. That and there is another phase, the Wither King.

                After defeating Necron, the middle of the bossroom opens up and players can hope into the Wither King bossroom. To start the bossfight, each player has to pick up a Relic from the mouth of the 5 Dragon Alters and place them at the feet of the castle looking structure. This will summon the Wither King and 5 Withered Dragons. This bossfight is a bit confusing, but all the party needs too do is kill the 5 dragons while they are close too their respective alters(The closeness is indicated by particles). Killing a dragon in the wrong place will cause it to respawn. The Wither King also likes to attack the party with AoE attacks so look out for those. Defeating the 5 Dragons in a timely manner will end the fight. Failing to kill all 5 dragons in a certain amount of time will cause your party too be crushed by a giant hand.
                """
                disc8 = """
                Archer: Necron+golden/diamond necron head, terminator and scylla, ender dragon/golden dragon pet
                Berserker: Necron+golden/diamond necron head, terminator and scylla or axe of the shredded+giant sword/valkyrie/claymore, ender dragon/golden dragon pet
                Mage: Storm+wither goggles, wither blade/giant sword/claymore, sheep/ender dragon/golden dragon
                Tank: Goldor+reaper mask, astraea, whale pet
                Healer: Necron+mender crown, term,baby yeti/ender dragon/golden dragon/whale
                """
                embed.add_field(name='General Info',value=disc,inline=False)
                embed.add_field(name='Phase 1 - Maxor',value=disc1,inline=False)
                embed.add_field(name='Phase 2 - Storm',value=disc2,inline=False)
                embed.add_field(name='Phase 3 Pt. 1 - Goldor',value=disc3,inline=False)
                embed.add_field(name='Phase 3 Pt. 2 - Goldor',value=disc4,inline=False)
                embed.add_field(name='Phase 4 - Necron',value=disc5,inline=False)
                embed1.add_field(name='Normal Mode Gear Guide',value=disc6,inline=False)
                embed1.add_field(name='Master Mode Phase 5 - The Wither King',value=disc7,inline=False)
                embed1.add_field(name='Master Mode Gear Guide',value=disc8,inline=False)
                embed.set_footer(text='Continue to the next Embed')
                embed1.set_footer(text='Written by KnockoffCanadian#1632 • Gear Guide written by AlienTheHoward#2188',icon_url='https://images-ext-1.discordapp.net/external/feyg3pLOSP2wE8Q7-EubCtckfOYHNW7a42GGnHPthd0/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/370024340730675202/bc16510b0ee41ccb312cd5d33066617b.png')
                await ctx.send(embed=embed)
                await ctx.send(embed=embed1)
        elif msg.content.lower() == 'slayers':
            embed = discord.Embed(title='Slayer Catagories',description='',color=discord.Color.blue())
            disc = """
            __Select a catagory to view information__

            Revenant Horror
            Tarantula Broodfather
            Sven Packmaster
            Voidgloom Seraph
            Inferno Demonlord
            """
            embed.add_field(name='Options',value=disc,inline=False)
            embed.set_footer(text='Type in the name of the section you would like to view information for')
            await ctx.send(embed=embed)
            def check(m):
                return m.content.lower() in ['revenant horror','tarantula broodfather','sven packmaster','voidgloom seraph','inferno demonlord'] and m.channel == channel
            msg = await bot.wait_for('message',check=check)
            if msg.content.lower() == 'revenant horror':
                embed = discord.Embed(title='Revenant Horror',description='The Zombie Slayer, Revenant Horror, currently has 5 tiers. We currently have guides for 2 tiers',color=discord.Color.blue())
                disc = """
                __Select a catagory to view information__

                T4
                T5
                """
                embed.add_field(name='Options',value=disc,inline=False)
                embed.set_footer(text='Type in the name of the section you would like to view information for')
                await ctx.send(embed=embed)
                def check(m):
                    return m.content.lower() in ['t4','t5'] and m.channel == channel
                msg = await bot.wait_for('message',check=check)
                if msg.content.lower() == 't4':
                    embed = discord.Embed(title='Revenant Horror Tier 4',description='',color=discord.Color.blue())
                    disc = """
                    Armor-3/4 Shadow assassin+zombie knight chestplate, 3/4 crimson+tarantula helm
                    Weapon-Flower of truth, livid dagger, aspect of the dragons, reaper falchion
                    Pet-Tiger, griffin, wither skeleton, blue whale, baby yeti
                    """
                    disc1 = "Costs 50k to spawn, grants 500 rev xp"
                    embed.add_field(name='Gear Guide',value=disc,inline=False)
                    embed.add_field(name='Other Notes',value=disc1,inline=False)
                    embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 't5':
                    embed = discord.Embed(title='Revenant Horror Tier 5',description='',color=discord.Color.blue())
                    disc = """
                    Armor-3/4 Necron+tarantula helm, 3/4 crimson+tarantula helm, 3/4 reaper+tarantula helm, can be substituted with warden helm/reaper mask
                    Weapon-Reaper falchion, shadow fury, giants sword, axe of the shredded
                    Pet-Griffin, blue whale, tiger, wither skeleton, baby yeti
                    """
                    disc1 = """
                    Costs 100k to spawn, 1500 rev xp, unlocks most of the rng drops like scythe blade, warden heart, shard of the shredded, etc. Spawns tnt which needs to be dodged, when/if it spawn bedrock, run away, it will explode killing anyone inside it. Can be cheesed with iron bars by preventing tnt from hitting you at -126, 41, -148 
                    """
                    embed.add_field(name='Gear Guide',value=disc,inline=False)
                    embed.add_field(name='Other Notes',value=disc1,inline=False)
                    embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                    await ctx.send(embed=embed)
            elif msg.content.lower() == 'tarantula broodfather':
                embed = discord.Embed(title='Tarantula Broodfather',description='The Spider Slayer, Tarantula Broodfather, currently has 4 tiers. We currently have guides for 1 tier',color=discord.Color.blue())
                disc = """
                Armor-2/4 shadow assassin+zombie knight chestplate, 3/4 crimson, 3/4 strong dragon + tarantula helm
                Weapon-Flower of truth, livid dagger, aspect of the dragon
                Pet-Griffin, wither skeleton, tiger
                """
                disc1 = """
                Costs 50k to spawn, grants 500 tara xp. Good idea to stand with back against a wall to prevent it from jumping behind, bring life steal/syphon weapons, tier 3 unlocks tarantula talis and fly swatter while tier 4 unlocks digested mosquito 
                Right click mage also is viable(aurora/storm/maxor with any high magic damage item can work for very fast bosses but is more expensive) 
                """
                embed.add_field(name='Gear Guide',value=disc,inline=False)
                embed.add_field(name='Other Notes',value=disc1,inline=False)
                embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                await ctx.send(embed=embed)
            elif msg.content.lower() == 'sven packmaster':
                embed = discord.Embed(title='Sven Packmaster',description='The Wolf Slayer, Sven Packmaster, currently has 4 tiers. We currently have guides for 1 tier',color=discord.Color.blue())
                disc = """
                Armor-3/4 shadow assassin+zombie knight chestplate, full mastiff, 3/4 crimson+tarantula helm, sorrow+crimson
                Weapon-Flower of truth, livid dagger, aspect of the dragons, shadow fury
                Pet-Wither skeleton, griffin, blue whale
                """
                disc1 = """
                Costs 50k to start and grants 500 xp, does true damage meaning your defense does not matter. It is recommended to use sorrow for true or water to prevent it from hitting you. Mastiff can also be used to gain a lot of hp
                """
                embed.add_field(name='Gear Guide',value=disc,inline=False)
                embed.add_field(name='Other Notes',value=disc1,inline=False)
                embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                await ctx.send(embed=embed)
            elif msg.content.lower() == 'voidgloom seraph':
                embed = discord.Embed(title='Voidgloom Seraph',description='The Enderman Slayer, Voidgloom Seraph, currently has 4 tiers. We currently have guides for 4 tiers',color=discord.Color.blue())
                disc = """
                __Select a catagory to view information__

                T1
                T2
                T3
                T4
                """
                embed.add_field(title='Options',value=disc,inline=False)
                embed.set_footer(text='Type in the name of the section you would like to view information for')
                await ctx.send(embed=embed)
                def check(m):
                    return m.content.lower() in ['t1','t2','t3','t4'] and m.channel == channel
                msg = bot.wait_for('message',check=check)
                if msg.content.lower() == 't1':
                    embed = discord.Embed(title='Voidgloom Seraph Tier 1',description='',color=discord.Color.blue())
                    disc = """
                    Armor-3/4 strong dragon+tarantula helm, 3/4 crimson+tarantula helm, 3/4 sa+zombie knight chestplate, 3/4 necron+tarantula helm or reaper mask
                    Weapon-Flower of truth, livid dagger, aspect of the dragons, shadow fury
                    Pet-Baby yeti, blue whale, griffin, tiger, wither skeleton, turtle
                    """
                    disc1 = """
                    Voidglooms have a "hits phase" where all hits count as 1 hit no matter how much damage you do, after this shield is broken, players can deal normal damage again
                    """
                    embed.add_field(name='Gear Guide',value=disc,inline=False)
                    embed.add_field(name='Other Notes',value=disc1,inline=False)
                    embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 't2':
                    embed = discord.Embed(title='Voidgloom Seraph Tier 2',description='',color=discord.Color.blue())
                    disc = """
                    Armor-3/4 Necron+reaper mask, final destination
                    Weapon-Voidedge katana, livid dagger, shadow fury, giant sword
                    Pet-Baby yeti, blue whale, turtle, leg/mythic eman
                    Useful items: florid zombie sword, summoning ring/necromancer sword/reaper scythe with m3 tank zombie souls, preferably 2-3, wand of atonement
                    """
                    disc1 = """
                    The tier 2 gains much more damage and strength, making it very challenging compared to the tier 1. It is highly recommended to bring necromancy items to both tank the boss and deal with its hits phase. Healing is also highly recommended as this boss will still do high amounts of damage. Starting from the tier 2, the boss will throw out beacons randomly called "Yang Glyphs." Players must go over and stand next to/on top of these to disarm them, otherwise they will be insta killed. This can be blocked with wither cloak. 
                    """
                    embed.add_field(name='Gear Guide',value=disc,inline=False)
                    embed.add_field(name='Other Notes',value=disc1,inline=False)
                    embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 't3':
                    embed = discord.Embed(title='Voidgloom Seraph Tier 3',description='',color=discord.Color.blue())
                    disc = """
                    Armor-Full final destination with a decent amount of kills(5-10k is recommended atleast)
                    Weapon-Voidedge/vorpal katana with tier 6 enchants
                    Pet-Blue whale, baby yeti, turtle, leg/mythic eman. Pet items such as the crochet tiger plushie or dwarf turtle shelmet are very useful
                    Useful items-Wand of atonement, florid zombie sword, summoning ring/necromancer sword/reaper scythe with m3 tank zombie souls, preferably 2-3
                    """
                    disc1 = """
                    Same as the tier 2, with higher stats. Also gains a new ability of throwing out floating heads. These heads will shoot at you and deal damage, and can be disarmed by looking right at them. This boss can also be cheesed until tier 3 with admin souls(m1 lvl 25), goblin armor, and a wither cloak. By standing on a ledge where the boss cannot reach the player, the 2 admin souls can completely solo the boss up to tier 3. The easiest way to spawn 2 admins is with full necrotic(even the cp) wise dragon armor, a lvl 100 sheep for mana reduction, and ult wise 5. If the mana cannot be reached, recombobulating and adding wisdom on the armor may help. 
                    """
                    embed.add_field(name='Gear Guide',value=disc,inline=False)
                    embed.add_field(name='Other Notes',value=disc1,inline=False)
                    embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                    await ctx.send(embed=embed)
                elif msg.content.lower() == 't4':
                    embed = discord.Embed(title='Voidgloom Seraph Tier 4',description='',color=discord.Color.blue())
                    disc = """
                    Armor-Full final destination(10k kills is recommended atleast). Can be either ancient or necrotic+loving
                    Weapon-Atomsplit, hyperion+fire veil wamd(if right click mage instead of melee)
                    Pet-Baby yeti, blue whale, ender dragon, golden dragon, sheep. Pet items can include dwarf turtle shelmet, crochet tigher plushie, antique remedies
                    Useful Items-Wand of atonement, florid zombie sword, scylla, necromancy items(2-5 souls), soul whip with mana steal and sapphire power scroll, weird tuba, pigman sword, end stone sword.
                    """
                    disc1 = """
                    Same as the tier 3 with even higher stats. Boss also gains a new ability of a laser phase, where it will become immune to damage but also not do damage. It will spawn 4 laser walls around it that spin in a circle. Players can either walk inside the walls or jump over to avoid them. It is recommended to use your soul whip on it during this phase to regen mana.
                    """
                    embed.add_field(name='Gear Guide',value=disc,inline=False)
                    embed.add_field(name='Other Notes',value=disc1,inline=False)
                    embed.set_footer(text='Written by AlienTheHoward#2188',icon_url='https://cdn.discordapp.com/avatars/803323100582248468/cb10f272fb4554080a201b9d37920a78.png?size=4096')
                    await ctx.send(embed=embed)
            elif msg.content.lower() == 'inferno demonlord':
                embed = discord.Embed(title='Inferno Demonlord',description='The Blaze Slayer, Inferno Demonlord, currently has 4 tiers. We currently have guides for 4 tiers',color=discord.Color.blue())
                disc = """
                __Select a catagory to view information__

                T1
                T2
                T3
                T4
                """
                embed.add_field(title='Options',value=disc,inline=False)
                embed.set_footer(text='Type in the name of the section you would like to view information for')
                await ctx.send(embed=embed)
                def check(m):
                    return m.content.lower() in ['t1','t2','t3','t4'] and m.channel == channel
                msg = await bot.wait_for('message',check=check)
                if msg.content.lower() == 't1':
                    embed = discord.Embed(title='Inferno Demonlord Tier 4',description='',color=discord.Color.blue())
                    disc = """

                    """

def setup(bot):
  bot.add_cog(AutomaticTutoringSystem(bot))
