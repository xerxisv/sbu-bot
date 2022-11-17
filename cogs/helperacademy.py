import asyncio
import discord
import time
from discord.ext import commands
import random
from discord.utils import get
from utils.constants import MODERATOR_ROLE_ID

#######################
#                     #
#     STRINGS         #
#                     #
#######################

report = """
Here at Skyblock University, we believe each and every person deserves to feel comfortable in our guild. However, this does not mean that we allow individuals to bully or treat others poorly in our guilds and server. Unfortunately, our moderation team cannot be everywhere at once, so we need to rely on our Seniors and Instructors to tell us when someone has taken an action that has disturbed them or otherwise made them uncomfortable.
"""
body1 = """
Here’s a few examples of potential rule breaking that’s reportable:
```Begging
Talking about drugs
Talking about sexually related things
Spamming chat with caps, or fast messages with little in it
Promoting rule breaking or leading people to break rules
Hacking```
"""
end = """
This list is not exhaustive, but should give you an idea of some of the things that we don’t allow. You can find a full list of our rules in rules

If you find someone doing these actions in game you can report them to our moderation team by opening a “report a user” ticket in get-help. Please be sure to include screenshots of everything you are reporting.

Our lack of knowledge of these situations happening may turn into people thinking we tolerate bad behavior. This is not our intention or what we wish to show new members. The more people report, the more aware we are of people who make everyone else unhappy, the faster we can remove excessively disruptive people and make our guilds and server more comfortable for everyone. You will be our front line in making our server safe for both current and new members.
**Type the command -done when finished reading**"""

report1 = """
Bobby531 recently joined the guild and is asking for a Hyperion for free, then saying they’re just kidding right afterwards. They have repeated this behavior a few times in the past.

It’s never fun to be nagged by guild members for free things. We have “No Begging” in our rules and believe everyone should know that they can be in our guild without 10 people harassing them, asking for free things. Regardless if someone says “just kidding” right after, it’s still annoying to have to deal with on a regular basis, and we don’t want to have to force our members ignore these issues or /ignore add the beggar. Handling them right away by reporting them is the best and fastest way to get someone to stop doing an undesirable behavior.
**Type the command -done when finished reading**"""

report2 = """
Georgina32 and Bobby555 have been talking about drugs for a few minutes, both of them are just simply naming drugs one after another. This started because Bobby555 said he needed more drugs for his dungeon runs(referring to Potions).

Because Mojang’s ToS states the game is for ages 10 and above, we don’t allow talk of illicit substances or likewise, due to the player base being so young. These actions would warrant a report, even if Georgina32 and Bobby555 have already stopped talking about drugs. You will need to take and submit screenshots with your report.
**Type the command -done when finished reading**
"""

report3 = """
Sopheee, Randy67, and Bobby555 are all getting a bit rowdy. They start to turn to making “deez nuts” jokes to each other. Sopheee sets all the jokes up, and Bobby555 is saying the punchline to each joke.

While "deez nuts" jokes aren’t punishable, if the conversation turns into spamming you should report all 3 of them to our staff
**Type the command -done when finished reading**"""

report4 = """  
Sopheee is upset you “told on” her by reporting her to staff. She’s DMing you telling you how horrible you are for ruining their fun.

This is plain harassment and is not tolerated. Please let us know if you’re every harassed publicly or privately by another member in our server or guilds and we will be sure to handle them immediately. We want everyone to feel safe on our server. You will need to take and submit screenshots with your report.
**Type the command -done when finished reading**
"""

kindness = """
This academy is an incredibly important piece to how we survive as a guild and server. Our staff need to also be helpful and kind. People that are found being catty or otherwise rude will be stripped of their ranks and reduced to Freshmen moving forward.

We aren’t here to berate confused newcomers into submission by calling them worthless nons and promoting how big and strong we are. The sole purpose of our server and guilds are to help new and mid-game players learn how to play skyblock. Holding yourself above another player due to how much weight, networth, etc you have has absolutely no place here. The idea that you treat others this way needs to be smashed from here on if you wish to have a rank in this server.

"""
body2 = """If you would consider our guild like a college campus, our general chat being our open area where people can congregate, our help channels are like our classrooms, and our tutoring sessions are just that. We are a school here, and where we absolutely do like to have fun, there is still a bit of professionalism that we need to show to the new and confused members of our community. With new members we need to remember that we were new too at one point in time and didn’t have all the information or know where to go. We must put ourselves back in their shoes to treat them with kindness and respect all humans deserve.
"""
body3 = """If you feel yourself getting short with someone, irritated or angry - don’t fret! We have plenty of other people who would love to help and take your place. Just step back for a minute and let someone else take over.

"""
end1 = """If you are helping someone that is just asking for free things from you over and over again, please be sure to report beggars to our mod team, so we may handle these situations individually.
**
Type the command -done when finished reading
**
"""


body4 = """
> Report disruptive people
> Understand when to report 
> Check people as they request to join our guild
> Be available to answer questions in tutoring tickets
> Be generally helpful, kind, and welcoming to all.

**This Academy has four sections.**:
**Report Guide** - How and when to report someone to our staff that is breaking our rules
**Kindness Academy** - How to be generally helpful, kind, and welcoming to all
**Guild Checking Academy** - How to check if people are on our #banned-list or on a scammer list
**Tutoring Academy** - What tutoring tickets are and how to act in them

After you are done reading, you will be tested with several open answer questions to make sure you understand what was covered. You may ask questions before testing.

Once you finish reading all sections of this academy, please ping the Moderator role THEN clarify if you've pinged to ask questions OR if you're ready to be tested.
**Type the command -done when finished reading**"""

guildchecking1 = """Check if they are on <@797974550834053203> scammer/irl trader list by performing this command in <#801507439236874290>:

/lookup player [ign]

You can see and example below of someone who is not flagged and someone who is flagged.

Link to gif if you're having trouble loading: https://i.imgur.com/DzRRdk5.mp4"""
guildchecking2 = """Use:
`+banlist check [ign]`

This command searches our <#830188559964307526> channel to ensure this person was not previously banned from our guilds or a scammer.

Link to gif if you're having trouble loading: https://i.imgur.com/1G8oPwT.gif"""
guildchecking3 = """
You can use this command to bring up a cheat-sheet on how to look up people in our guilds at any time in the future:

`!bannedlist`

Note: If you are unable to look people up, you will not be able to hold a rank in our guilds.
Please continue below.
**Type -done after you finish reading this**"""

done1 = "You are done with the course. Ping <@&801634222577156097> to start the test or ask questions"


lookuplist = ["shachi", "Rvon", "Fijit", "someonestolemypc", "jpgaming55", "LordZarach",
                "Skeldow", "FDRR", "LavenderHeights", "MartinNemi03", "69mn", "zStrelizia",
                "Adviceful", "Zykm", "russiandeniss", "spedwick", "FantasmicGalaxy", "urra", 
                "Iwolf05", "noscope_", "luvanion", "KSavvv18", "43110s", "dukioooo",
                "CoruptKun", "Teunman", "302q", "Tera_Matt", "jexh", "Royalist",
                "McMuffinLover", "o600", "jjww2", "n0twanted", "LeaPhant", "Zanjoe",
                "Yarnzy_", "ih8grinding", "Verychillvibes", "LesbianCatgirl", "Legendofhub", "Spectrov",
                "_YungGravy", "wigner", "U4BJ"
                ]
lookuplistans = ["Scammer", "Scammer", "Not Scammer", "Scammer", "Scammer", "Not Scammer",
                "Scammer", "Scammer", "Scammer", "Not Scammer", "Scammer", "Scammer", 
                "Scammer", "Scammer", "Scammer", "Scammer", "Not Scammer", "Scammer",
                "Scammer", "Scammer", "Scammer", "Scammer", "Scammer", "Not Scammer",
                "Scammer", "Scammer", "Scammer", "Scammer", "Not Scammer", "Scammer",
                "Scammer", "Not Scammer", "Not Scammer", "Scammer", "Not Scammer", "Scammer", 
                "Scammer", "Scammer", "Scammer", "Not Scammer", "Scammer", "Scammer",
                "Not Scammer", "Scammer", "Scammer"
                ]

situations = ["""bith_creative: I can’t seem to be able to do F7, I keep dying, could anyone give me some tips? 
SoFestivePleasantt: sure
FartFace: How about you just get good at the game?
Seal2906: huh
bith_creative: that’s not nice…""",
              """Lemonbad: Carry me in f6
              Lemonbad: pls?
              Lemonbad: F6 please?
              Lemondbad: lol can’t do f6?
              YourCasualMelon: I can do it with a tank
              Lemonbad: lmao this guild is so trash""",
              """BonkofDuty: could someone give me a free armour set for f4?
              FastgoStabber: Adaptive armour is relatively great
              BonkofDuty: It looks cheap could you buy for me?
              BonkofDuty: pls :3
              FastgoStabber: No earn it yourself that way it’s more fun
              BonkofDuty: ok sir o7""",
              """
              TheHolyBonk: yo anyone want some enchanted quartz blocks for 1.2m?
              BlueCow03: sure visit me
              TheHolyBonk: cool

              TheHolyBonk has left the guild
              BlueCow03: NO
              StanTheStonk3069: F
              ElonMucus: what was it?
              BlueCow03: HE REPLACED THE QUARTZ BLOCKS WITH SNOW BLOCKS!
              Traingovroom53: kekw
              CatScreech82: f""",
              """Uda5092: I’m not going to sleep tonight
              ScaryDuck: You better sleep otherwise I’ll hack your account and take your stuff
              Uda5092: wtf
              PinguHuman420: chill
              ScaryDuck: Give me your stuff
              Uda5092: fine
              PinguHuman420: Don’t do it!
              Uda5092: I already did…""",
              """Goodbean123: whats ur favourite band?
              BigBrain96: One Direction
              AuntAsh: Imagine Dragons
              Goodbean123: oh no…
              BadBean987: Imagine dragon deez nuts on ur chin
              BigBrain96: Ayo?""",
              """DogeLover4: Hyperion on my ah!!!
              AmericanDove07: pog
              DogeLover4: ./ah DogeLover4

              DogeLover4: still got a hype on my ah! /ah DogeLover4
              AmericanDove07: I’m too poor
              DogeLover4: Imagine
              DogeLover4: peasant

              DogeLover4: ./ah DogeLover4 still got the Hyperion up""",
              """Flylit: how’s everyone’s day going?
              FootRaider27: stfu
              123456789Boom: Not that good
              FootRaider27: L bozo
              Flylit: I was just trying to be nice ;-;
              Flylit has left the guild!
              FootRaider27: L kekw""",
              """wyvwall: i have 900m what should i buy
              NoNoNo50: what pet?
              wyvwall: epic tiger
              NoNoNo50: get legendary e drag
              wyvwall: ok got tied boosted one
              NoNoNo50: Are you fucking stupid
              Flylit: oi back off
              NoNoNo50: you’re and idiot non LLLLL
              wyvwall: damn ok then ;-;""",
              """EvilChicken101: MVP+ for 25m!
              LightTheme2: sure
              AceOnAPlate: that’s not allowed is it?
              EvilChicken101: it’s just a trade…""",
              """KekMoment: A
              KekMoment: B
              KekMoment: C
              KekMoment: D
              KekMoment: E
              KekMoment: F
              KekMoment: G
              KekMoment: H
              StopItGetSomeHelp: Stop spamming
              KekMoment: I
              KekMoment: J
              StopItGetSomeHelp: I said stop spamming
              KekMoment: No u""",
              """Kazenamipat: Yo guys I just got farming 30
              Beepbeep: gg
              smhmyhead: Bro your soooo bad only farming 30?
              smhmyhead: I have farming 55 get on my level
              Kazenamipat: I haven’t played as long tho""",
              """
              9876543bombdiffused: Hey can someone help me with crafting a juju?
              bith_creative: Sure
              9876543bombdiffused: I’ll need collat
              bith_creative: Sure
              ——————-
              9876543bombdiffused has left the guild!
              ——————-
              bith_creative: Wait
              bith_creative: Noooo he scammed me
              Confuzalation: How?
              bith_creative: He gave me enchanted snow blocks not enchanted quartz blocks
              """]

situationsans = [
    """Open a ticket in <#765927458314387498> for report a user and report FartFace for toxicity""",
    """Report LemonBad for begging in <#765927458314387498> and direct them to <#887548399036022804> on dc""",
    """No necessary action is needed as they only ask once and stopped when told to""",
    """Create a report a scammer ticket in <#765927458314387498> and remember to ask for ss of the trade so that TheHolyBonk can be 
    reported to skykings """,
    """Report ScaryDuck_ for scamming in <#765927458314387498> with ss of the trade""",
    """Report BadBean987 in <#765927458314387498>  for nsfw jokes in guild chat""",
    """Report DogeLover4 in <#765927458314387498> for spam advertising""",
    """Report FootRaider27 for toxicity in <#765927458314387498>""",
    """Report NoNoNo50 for toxicity in <#765927458314387498>""",
    """Report EvilChicken101 for irl trading in <#765927458314387498> from there our moderators can further oversee 
    this """, """Report KekMoment in <#765927458314387498> for spam""",
    """Report smhmyhead in <#765927458314387498> for toxicity""",
    """Report 9876543bombdiffused in <#765927458314387498> for scamming"""]


#######################
#                     #
#       EMBEDS        #
#                     #
#######################

reporte1 = discord.Embed(
    title='Reporting people',
    description='',
    colour=discord.Colour.blue()
)
reporte1.set_footer(text='SBU Rank Academy')
reporte1.add_field(name="Belief", value=report, inline=False)
reporte1.add_field(name="Against Rules", value=body1, inline=False)
reporte1.add_field(name="Disclaimer", value=end, inline=False)



reporte2 = discord.Embed(
    title='Example 1',
    description='',
    colour=discord.Colour.blue()
)
reporte2.set_footer(text='SBU Rank Academy')
reporte2.add_field(name="1.", value=report1, inline=False)

reporte2a = discord.Embed(
    title='Example 2',
    description='',
    colour=discord.Colour.blue()
)
reporte2a.set_footer(text='SBU Rank Academy')
reporte2a.add_field(name="2.", value=report2, inline=False)



reporte3 = discord.Embed(
    title='Example 3',
    description='',
    colour=discord.Colour.blue()
)
reporte3.set_footer(text='SBU Rank Academy')
reporte3.add_field(name="3.", value=report3, inline=False)



reporte4 = discord.Embed(
    title='Example 4',
    description='',
    colour=discord.Colour.blue()
)
reporte4.set_footer(text='SBU Rank Academy')
reporte4.add_field(name="4.", value=report4, inline=False)



kindness1 = discord.Embed(
    title='Kindness Academy',
    description='',
    colour=discord.Colour.blue()
)
kindness1.set_footer(text='SBU Rank Academy')
kindness1.add_field(name="Why Kindness Academy?", value=kindness, inline=False)
kindness1.add_field(name="SBU Example", value=kindness, inline=False)
kindness1.add_field(name="What to do if you get annoyed.", value=body3, inline=False)
kindness1.add_field(name="The end for Seniors", value=end1, inline=False)



helper1 = discord.Embed(
    title='Helper Academy',
    description='',
    colour=discord.Colour.blue()
)
helper1.set_footer(text='SBU Rank Academy')
helper1.add_field(name="Rank Requirements", value=body4, inline=False)



guildc = discord.Embed(
    title='Guild Checking academy',
    description='',
    colour=discord.Colour.blue()
)
guildc.set_footer(text='SBU Rank Academy')
guildc.add_field(name="#1 Use bots to check scammer lists", value=guildchecking1, inline=False)
guildc.set_image(
    url="https://cdn-longterm.mee6.xyz/plugins/commands/images/764326796736856066/98245433fe5c01c4e8b26c4334319e6334b154542c09d943bad6c8f0e2e58b52.gif")

guildc1 = discord.Embed(
    title='Guild Checking academy',
    description='',
    colour=discord.Colour.blue()
)
guildc1.add_field(name="#2 Use discord's search bar to search and make sure they are not in our #banned-list",
                  value=guildchecking2, inline=False)
guildc1.set_image(
    url="https://cdn-longterm.mee6.xyz/plugins/commands/images/764326796736856066/2c1d1c042343c75852863d3018df07f9737a06b0b2b67d63a84477d35d4ce6ee.gif")

guildc2 = discord.Embed(
    title='Guild Checking academy',
    description='',
    colour=discord.Colour.blue()
)
guildc2.add_field(name="Notes", value=guildchecking3, inline=False)

end = discord.Embed(
    title="The end",
    description=done1,
    colour=discord.Colour.blue()
)


#######################
#                     #
#      COMMANDS       #
#                     #
#######################

class HA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helperacademy(self, ctx):
        member = ctx.message.author
        role = get(member.guild.roles, name="HA Applicant")
        await member.add_roles(role)
        message = await ctx.send(embed=helper1)
        channel = message.channel

        def check(m):
            return m.content.lower() == '-done' and m.channel == channel

        msg = await self.bot.wait_for('message', check=check)
        message = await ctx.send(embed=reporte1)
        msg = await self.bot.wait_for('message', check=check)
        message = await ctx.send(embed=reporte2)
        msg = await self.bot.wait_for('message', check=check)
        message = await ctx.send(embed=reporte2a)
        msg = await self.bot.wait_for('message', check=check)
        message = await ctx.send(embed=reporte3)
        msg = await self.bot.wait_for('message', check=check)
        message = await ctx.send(embed=reporte4)
        msg = await self.bot.wait_for('message', check=check)
        message = await ctx.send(embed=kindness1)
        msg = await self.bot.wait_for('message', check=check)
        message = await ctx.send(embed=guildc)
        message = await ctx.send(embed=guildc1)
        message = await ctx.send(embed=guildc2)
        msg = await self.bot.wait_for('message', check=check)
        message = await ctx.send(embed=end)

    @commands.command()
    @commands.has_role(MODERATOR_ROLE_ID)
    async def lookupsection(self, ctx):
        length = len(lookuplist)
        randomlist = random.sample(range(0, length), 9)
        channel = self.bot.get_channel(883539648754892910)
        channelid = ctx.channel.id
        questions = discord.Embed(
            title='Lookup Section',
            description='',
            colour=discord.Colour.blue()
        )
        answers = discord.Embed(
            title=f'Lookup Section Answers',
            description='',
            colour=discord.Colour.red()
        )
        questions.set_footer(text='SBU Rank Academy Questions')
        questions.add_field(name="What to do.",
                            value="Look up this list of people and mention if they are cleared to enter our guild or not:",
                            inline=False)
        answers.set_footer(text='SBU Rank Academy Answers')
        templist = ""
        for banned in randomlist:
            answers.add_field(name=lookuplist[banned], value=lookuplistans[banned], inline=False)
            templist = templist + "\n" + lookuplist[banned]
        questions.add_field(name="Lookup: ", value=templist, inline=False)
        await channel.send(f"Lookup Section Answers for <#{channelid}>")
        await ctx.send(embed=questions)
        await channel.send(embed=answers)

    @lookupsection.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Insufficient Permissions")


def setup(bot):
    bot.add_cog(HA(bot))