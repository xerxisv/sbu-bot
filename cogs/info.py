import discord
from discord.ext import commands
from discord.ui import View

from utils.config.config import ConfigHandler
from utils.components import info_button

config = ConfigHandler().get_config()


INFO_EMBED_DESCRIPTION = "Skyblock University is a Skyblock Community focused on helping new players.\n\
We offer many services including **Tutoring, Bingo Guides and much more!**\n\
We host tons of giveaways and events!"


RULES_STRING = ":arrow_right: These rules are a general guideline; if something is not disallowed by the rules, that doesn't mean it's allowed.\n\
If you ever have questions about what's allowed, feel free to ask! Our Moderation team has the final say and can take any actions they need to end a situation up to and including bans.\n\
\n\
Everyone must also follow these rules:\n\
Hypixel server rules: https://hypixel.net/hypixel-rules\n\
Hypixel skyblock rules: https://hypixel.net/skyblock-rules\n\
Discord Terms of Service: https://discord.com/terms\n\
Discord commiunity guildelines: https://discord.com/guidelines\n\
\n\
:one: Respect others.\n\
Toxicity, bigotry, racist, sexist, homophobic, religiophobic, intolerant, or otherwise derogatory content of any sort is not tolerated in our server or in our guilds.\n\
\n\
:two: No NSFW content.\n\
No age-restricted or obscene content. This includes text, images, or [link]s featuring nudity, sex, hard violence, or other graphically disturbing content.\n\
\n\
:three: No Advertising.This includes sending invite [link]s to other servers in people's direct messages on Discord. You are allowed to advertise in our in-game guilds so long as it's not obnoxious or in a way that's begging. If you're found advertising sketchy [link]s or discord servers you will be punished. These mainly include irl trading server invites, ip grabber [link]s, fake verification [link]s etc.\n\
\n\
:four: No begging.\n\
No one likes a beggar. Those sending messages in guild chat/discord containing only buy my ah, asking for free things continuously, or things of that nature. things will be punished. If you'd like to advertise your Auction House, do so eloquently and in the proper channels.\n\
\n\
:five: Don't spam or excessively ping others.\n\
Don't spam our server or bots. Don't ping others who ask not to be pinged, and don't excessively ping moderation roles. If you need help, you can ping moderation roles ONCE for issues. Those found spam pinging or trying to raid the server will be removed promptly.\n\
\n\
:six: Don't scam, macro, or IRL trade, etc.\n\
Any actions that could lead to an in game punishment for yourself or others, examples - IRL trading, Scamming and Ratting. These will lead to a ban with no appeal option.\n\
\n\
:seven: Use common sense.\n\
If you are ever unsure about a rule, use your common sense! If you aren't sure whether something is allowed, chances are it's probably not. We'll let you know if you post something that should be removed or you can open a question ticket to ask as well in support-tickets\n\
\n\
If you run into anyone causing issues let a staff member know by opening a ticket in support-tickets. Do not mini-mod."



HOW_TO_DONATE_STRING = "Skyblock University was created out of a passion and desire to do something great for the part of the Hypixel Skyblock community that is often overlooked - the new, early, and mid-game players. It was founded at the beginning of February 2021 and has since grown at a rapid pace, and unfortunately, we do have the overhead costs. We have a grand vision for Skyblock University and would love to keep building the community, growing our Discord Server, create new guilds as they are required, and develop new and exciting features, perks, and benefits for Skyblock University members.\n\
\n\
Up to this point we have spent countless hours creating the environment we have here at Skyblock University, hosted numerous fun and successful events and tirelessly created materials and guides to help our community. Our VPS service to host our discord bots is also $10 a month, which I pay out of our own pocket. If you would like to donate to Skyblock University to enable us to continue to do the work that we've been doing and empower us to deliver new and exciting features and benefits to our members please consider donating today using either of the following [link]:\n\
Patreon: https://www.patreon.com/skyblockuniversity\n\
\n\
We so appreciate your generosity and consideration, have a fantastic day!\n\
Server Donators\n\
<@823204617201909811> - $80\n\
<@171702273913782273> - $22\n\
<@593083280845307923> - $22\n\
<@348876600273666050> - $1.69\n\
<@566329261535920175> - $26\n\
Notes\n\
People who donate $10 or more will be allowed to add a message to their shout out. This can contain another server's [link] or a short message of your choosing so long as it follows our server's rules\n\
If you choose to advertise in this space it will be up only for a month, but your name will forever be on our list.\n\
You will only be added to this list if you request to be put on it, To request, please Dm an <@766041783137468506>\n\
(This is to help those who would like to be anonymous with their donations)"

HOW_TO_HELP_STRING = "Here's a list of things you can do to help us in other ways!\n\
**Bump our forum posts.**\n\
You can find the [link]s to our forum posts in this channel: our-guilds\n\
**Answering questions is always needed and appreciated!**\n\
We have help channels, along with a tutoring system that only people of Instructor rank or higher have access to seeing and answering specific questions. We always need more people to make themselves available to answering and providing knowledgeable information to the next wave of new Hypixel Skyblock players!\n\
**Consider hosting various parties or events.**\n\
If you're going to spend time mining or fishing or some other activity for a few hours, consider using our pings in party-finder, accessible through party-finder-access, to invite others to hang out with you while you skill. Events can be fairly small but still fun and low maintenance. <@837466543847768084> are able to host any event. You also don't need to pay any money to host events, they can be for fun and completely free.\n\
**Simply being active is also incredibly helpful!**\n\
This server wouldn't be where it is currently without it's active and helpful community! For that we would really like to thank each and every person here today!\n\
**Donate to the prize pool or to a giveaway!**\n\
The money for events is coming from commiunity donations, we wouldn't be able to make events without them."

ABOUT_US_STRING = "Skyblock University was founded with one goal in mind: to help brand new, early, and mid-game Hypixel Skyblock players by empowering them and equipping them with the tools, resources, and mentors they need to continually grow, learn, and progress.\n\
\n\
Hypixel Skyblock is a game where it's easy to begin but difficult to master, full of complexities and nuances, and it only gets more and more complex as Hypixel releases new updates. The learning curve can be steep, how to use your time and money efficiently can be unclear, understanding how to progress can be difficult, and for new players, it can feel overwhelming.\n\
\n\
Skyblock University aims to create a friendly and welcoming atmosphere where new players can receive coaching, feedback, and mentorship from late-game and end-game players on whatever they are currently struggling with, access a wealth of knowledge regarding mods, tools, and resources, as well as an active community to run dungeons with, skill grind with, and just hang out and chat and have fun with.\n\
\n\
We're accomplishing this goal through a two tiered approach:\n\
\n\
- The creation and maintenance of a Community Discord Server which provides a place for Skyblock University members to interact with their peers from all stages of the game, from all different guilds, to quickly and easily access the mentors, tools, and resources they need to excel\n\
- The creation of a Skyblock University Guild in game with no requirements, allowing new, early, and mid-game players a chance to get to understand how guilds work while providing them access to mentors in game who can answer their questions, run dungeons with them, and experience a relaxed guild environment where they can get to know their peers.\n\
\n\
A passion for helping new players is what brought our staff team together to help make this vision a reality and if you're reading this, we're so glad you're here. We're excited with how far we've come and we're even more excited for what the future has in store!"

GUILD_INFORMATION_STRING = "We currently have four in-game guilds, they are all the same but have different people.\n\
3 out of our 4 guilds have no requirements at all.\n\
\n\
Our rules:\n\
\n\
1️⃣ Follow Hypixel rules and our server's <#766033393807786005>\n\
\n\
2️⃣ Be nice to one another, toxicity is not tolerated as it makes people feel unwelcome and does not add to our teaching environment\n\
\n\
3️⃣ No begging. Repeat offenders of begging will be removed. We love to help people but we expect everyone to gain what they have through working for it.\n\
\n\
4️⃣ Stay active. If you do not log in to Hypixel for 7 or more days you most likely will be kicked from the guild.\n\
\n\
➡️ *If you have a planned leave from the game use `+inactive add time` and we will not kick you for the time you list.\n\
➡️ People who are kicked for inactivity are welcome to join back at any time!*\n\
\n\
**If you're interested in joining the Skyblock University Guild, you can do so by:\n\
\n\
- typing `/g join SB (Guild Name)` in-game\n\
- asking for a guild invite in <#1044525895597166592>\n\
- open a join request ticket in <#1044525895597166592>\n\
\n\
After you join you can assign your corresponding guild's roles to yourself by using the `+verify [IGN]`  command in <#1044525895597166592> or <#1044525895597166592>\n\
\n\
We hope to see you in-game!**\n\
\n\
**Please note:**\n\
*The current number of Guild members is listed at the top of our channel list. In the event that the Skyblock University guild is full, Skyblock University has various clubs that function as sister guilds under the umbrella of Skyblock University. Look below to see all join commands and guild information for each of our five guilds.*"

SB_UNI_STRING = "SB University\n\
Guild Leader: <@606917358438580224>\n\
No Requirement Hypixel Skyblock Guild\n\
Moderators: <@141629127110295552> and <@714139701879111721>\n\
Forum Post: [Link](https://hypixel.net/threads/skyblock-university-helping-new-and-midgame-players-large-community-8-guilds.5098895/#post-36636361)\n\
[Plancke.io](https://plancke.io/hypixel/guild/name/Skyblock%20Uni)\n\
**How To Join:** `/g join SB University`"
SB_ALPHA_STRING = "Guild Leader: <@351827324758523905>\n\
No Requirement Hypixel Skyblock Guild\n\
Moderators: <@895488539775598603> and <@491654047741509633>\n\
Forum Post: [Link](https://hypixel.net/threads/skyblock-university-helping-new-and-midgame-players-large-community-8-guilds.5098895/#post-36636361)\n\
[Logo](https://i.imgur.com/7g2rBEI.png) | [Logo Light](https://i.imgur.com/JHrR3kL.png)\n\
[Plancke.io](https://plancke.io/hypixel/guild/name/SB%20Alpha%20Psi)\n\
**How To Join:** `/g join SB Alpha Psi`"
SB_LAMBDA_STRING = "Guild Leader: <@606917358438580224>\n\
No Requirement Hypixel Skyblock Guild\n\
Moderators: <@165242007793434624>\n\
Forum Post: [Link](https://hypixel.net/threads/skyblock-university-helping-new-and-midgame-players-large-community-8-guilds.5098895/#post-36636361)\n\
[Plancke.io](https://plancke.io/hypixel/guild/name/SB%20Lambda%20Pi)\n\
**How To Join:** /g join SB Lambda Pi"
SB_MASTERS_STRING = "Guild Leader: <@86636550045065216>\n\
**REQS: 3500 Senither Weight\n\
500k Slayer Experience\n\
Catacombs Level 28**\n\
Moderators: <@220578609335631872>, <@610365291469471755>, and <@665885831856128001>\n\
Forum Post: [Link](https://hypixel.net/threads/skyblock-university-helping-new-and-midgame-players-large-community-8-guilds.5098895/#post-36636361)\n\
[Logo](https://imgur.com/loRE5fq)\n\
[Plancke.io](https://plancke.io/hypixel/guild/name/SB%20Masters)\n\
**How To Join:** Open a ticket in <#1044527146422501386>"


INACTIVE_LIST_STRING = "**How to add yourself to our inactive list?\n\
> `+inactive add Time`\n\
\n\
Here is an example\n\
\n\
> +inactive add 7d**"

BUTTON_STRINGS = {
    "Rules": {
        "description": RULES_STRING,
        "view": None,
        "image": "https://imgur.com/H6DndPs.jpg"
    },
    "How To Donate Money": {
        "description": HOW_TO_DONATE_STRING,
        "view": None,
        "image": "https://imgur.com/9IYU4TI.jpg"
    },
    "How To Help": {
        "description": HOW_TO_HELP_STRING,
        "view": None,
        "image": "https://imgur.com/XVW7QNH.jpg"
    },
    "About Us": {
        "description": ABOUT_US_STRING,
        "view": None,
        "image": "https://imgur.com/KGQcTMv.jpg"
    },
    "Guild Information": {
        "description": GUILD_INFORMATION_STRING,
        "view": {
            "dropdown": {
                "Guild Information": {
                    "description": GUILD_INFORMATION_STRING,
                    "image": "https://imgur.com/SIjgNrX.jpg"
                },
                "SB University": {
                    "description": SB_UNI_STRING,
                    "image": "https://imgur.com/pEqyyOW.jpg"
                },
                "SB Alpha Psi": {
                    "description": SB_ALPHA_STRING,
                    "image": "https://imgur.com/hJyH9I1.jpg"
                },
                "SB Lambda Pi": {
                    "description": SB_LAMBDA_STRING,
                    "image": "https://imgur.com/pEqyyOW.jpg"
                },
                "SB Masters": {
                    "description": SB_MASTERS_STRING,
                    "image": "https://imgur.com/qlrwfpQ.jpg"
                }
            },
            "button": None
        },
        "image": "https://imgur.com/SIjgNrX.jpg"
    },
    "Inactive List": {
        "description": INACTIVE_LIST_STRING,
        "view": None,
        "image": None
    }
}




class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        view = View(timeout=None)
        i = 0
        j = 0
        for button in BUTTON_STRINGS:
            i += 1
            label = button
            description = BUTTON_STRINGS[button]["description"]
            button_view = BUTTON_STRINGS[button]["view"]
            image = BUTTON_STRINGS[button]["image"]


            button = info_button(self.bot, label, description, button_view, image, row=j)
            view.add_item(button)
            
            if i == 5:
                i = 0
                j += 1
        bot.add_view(view)
        

    @commands.group(name='info', aliases=[], case_insensitive=True)
    @commands.has_role(config["admin_role_id"])
    async def info(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.bot.get_command('info help').invoke(ctx)
            return
        await ctx.trigger_typing()
    
    @info.command(name='reload', aliases=['load'])
    async def reload(self, ctx: commands.Context):
        await info_reload(self.bot, config)
        
        await ctx.send("Successfuly loaded info buttons")

    @info.command(name="unload", aliases=["ul"])
    async def unload(self, ctx: commands.Context):
        channel = await self.bot.fetch_channel(config["info"]["info_channel_id"])
        if channel.last_message_id is not None:
            message = await channel.fetch_message(channel.last_message_id)
        else:
            message = None

        try:
            await message.edit(view=None)
            await ctx.send("Successfuly unloaded info buttons")
        except discord.Forbidden:
            await ctx.send("Failed to unload info buttons")
        

async def info_reload(bot, config):
    channel = await bot.fetch_channel(config["info"]["info_channel_id"])
    try:
        message = await channel.fetch_message(channel.last_message_id)
    except discord.NotFound:
        message = None
    

    embed = discord.Embed(title="Info", description=INFO_EMBED_DESCRIPTION, color=config["colors"]["primary"])
    
    view = View(timeout=None)
    i = 0
    j = 0
    for button in BUTTON_STRINGS:
        i += 1
        label = button
        description = BUTTON_STRINGS[button]["description"]
        button_view = BUTTON_STRINGS[button]["view"]
        image = BUTTON_STRINGS[button]["image"]

        view.add_item(info_button(bot, label, description, button_view, image, row=j))
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

        
    

def setup(bot):
    bot.add_cog(Info(bot))