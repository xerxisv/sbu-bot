# CHAOS
import os

import dotenv

dotenv.load_dotenv()

SBU_LOGO_URL = 'https://cdn.discordapp.com/avatars/937099605265485936/8a5d786e369fdda9f355f12eaf0487fb.png?size=4096'
QOTD_PATH = './data/qotd.json'
SBU_GOLD = 0xc0c09e
SBU_PURPLE = 0x8F49EA
SBU_ERROR = 0xFF0000
SBU_SUCCESS = 0x00FF00

# Pseudo constants
GUILD_ID = 0

JR_MOD_ROLE_ID = 0
MODERATOR_ROLE_ID = 0
JR_ADMIN_ROLE_ID = 0
ADMIN_ROLE_ID = 0
QOTD_ROLE_ID = 0
GUILD_MEMBER_ROLE_ID = 0
VERIFIED_ROLE_ID = 0
ACTIVE_ROLE_ID = 0
SB_UNI_MEMBER_ROLE_ID = 0
SB_KAPPA_MEMBER_ROLE_ID = 0
SB_ALPHA_MEMBER_ROLE_ID = 0
SB_MASTERS_MEMBER_ROLE_ID = 0
SB_DELTA_MEMBER_ROLE_ID = 0
SB_LAMBDA_MEMBER_ROLE_ID = 0
TOP_GUILD_ACTIVE_ROLE_ID = 0
WEIGHT_BANNED_ROLE_ID = 0
FRESHMAN_ROLE_ID = 0
INSTRUCTOR_ROLE_ID = 0
PROFESSOR_ROLE_ID = 0
DEAN_ROLE_ID = 0
PROVOST_ROLE_ID = 0
PRIMUS_ROLE_ID = 0
LEGATUS_ROLE_ID = 0
BOOSTER_ROLE_ID = 0
QUARANTINED_ROLE_ID = 0
BOT_ROLE_ID = 0
MUTED_ROLE_ID = 0
SERVER_BOT_ROLE_ID = 0
UNI_BRIDGE_ROLE_ID = 0
ALPHA_BRIDGE_ROLE_ID = 0
KAPPA_BRIDGE_ROLE_ID = 0
DELTA_BRIDGE_ROLE_ID = 0
LAMBDA_BRIDGE_ROLE_ID = 0
MASTERS_BRIDGE_ROLE_ID = 0
EVERYONE_ROLE_ID = 0

QOTD_CHANNEL_ID = 0
MOD_CHAT_CHANNEL_ID = 0
ADMIN_CHAT_CHANNEL_ID = 0
BANNED_LIST_CHANNEL_ID = 0
SUGGESTIONS_CHANNEL_ID = 0
SBU_BOT_LOGS_CHANNEL_ID = 0
CARRY_SERVICE_REPS_CHANNEL_ID = 0
CRAFT_REPS_CHANNEL_ID = 0
MOD_ACTION_LOG_CHANNEL_ID = 0
BOOSTER_LOG_ID = 0
EARNABLE_ROLES_CHANNEL_ID = 0
OUR_GUILDS_CHANNEL_ID = 0
SUPPORT_TICKETS_CHANNEL_ID = 0
HOW_TO_HELP_CHANNEL_ID = 0
INFO_CHANNEL_ID = 0
BOOK_A_TUTOR = 0

# Categories
MODERATOR_CHANNELS_CATEGORY_ID = 0
MODERATION_GUIDES_CATEGORY_ID = 0
ADMIN_CHANNELS_CATEGORY_ID = 0
LOGGING_CHANNELS_CATEGORY_ID = 0
ARCHIVE_CATEGORY_ID = 0
CHANCELLOR_CHANNELS_CATEGORY_ID = 0

# VC IDs
UNI_VC_ID = 0
ALPHA_VC_ID = 0
KAPPA_VC_ID = 0
DELTA_VC_ID = 0
LAMBDA_VC_ID = 0
RHO_VC_ID = 0
MASTERS_VC_ID = 0

TOTAL_MEMBER_COUNT_VC_ID = 0

BRIDGE_CHANNEL_IDS = []
BRIDGE_BOT_IDS = []

if os.getenv('MODE') == 'PRODUCTION':
    GUILD_ID = 764326796736856066

    # Roles
    JR_MOD_ROLE_ID = 924332988743966751
    MODERATOR_ROLE_ID = 801634222577156097
    JR_ADMIN_ROLE_ID = 808070562046935060
    ADMIN_ROLE_ID = 766041783137468506
    GUILD_MEMBER_ROLE_ID = 824993223436533810
    VERIFIED_ROLE_ID = 812725363686899743
    ACTIVE_ROLE_ID = 809902629760139314
    SB_UNI_MEMBER_ROLE_ID = 803695821094125585
    SB_ALPHA_MEMBER_ROLE_ID = 821080619332796437
    SB_KAPPA_MEMBER_ROLE_ID = 832803831166926859
    SB_DELTA_MEMBER_ROLE_ID = 838121681931075594
    SB_LAMBDA_MEMBER_ROLE_ID = 843871813481267270
    SB_MASTERS_MEMBER_ROLE_ID = 944524838553399326
    TOP_GUILD_ACTIVE_ROLE_ID = 1031644373823262801
    WEIGHT_BANNED_ROLE_ID = 1041544214061776977
    FRESHMAN_ROLE_ID = 765539703016521729
    INSTRUCTOR_ROLE_ID = 801505303854055497
    PROFESSOR_ROLE_ID = 801541534247944253
    DEAN_ROLE_ID = 803273909951922227
    PROVOST_ROLE_ID = 818478619646623797
    PRIMUS_ROLE_ID = 946963518350045224
    LEGATUS_ROLE_ID = 947841300240138290
    BOOSTER_ROLE_ID = 803053116076589068
    QUARANTINED_ROLE_ID = 901668197906915359
    BOT_ROLE_ID = 765637218018394172
    MUTED_ROLE_ID = 804064527439626290
    SERVER_BOT_ROLE_ID = 813185990112837703
    UNI_BRIDGE_ROLE_ID = 1028810266445627394
    ALPHA_BRIDGE_ROLE_ID = 1023302352591126600
    KAPPA_BRIDGE_ROLE_ID = 1025482652570103849
    DELTA_BRIDGE_ROLE_ID = 1025477430078603316
    LAMBDA_BRIDGE_ROLE_ID = 1023329530334687254
    MASTERS_BRIDGE_ROLE_ID = 1027671227357204532
    EVERYONE_ROLE_ID = 764326796736856066

    # Channels
    QOTD_CHANNEL_ID = 868630191080083476
    TOTAL_MEMBER_COUNT_VC_ID = 890288776302190602
    SBU_BOT_LOGS_CHANNEL_ID = 946591422616838264
    MOD_CHAT_CHANNEL_ID = 802982854291488808
    ADMIN_CHAT_CHANNEL_ID = 911601330219532328
    QOTD_ROLE_ID = 868630686712614922
    BANNED_LIST_CHANNEL_ID = 830188559964307526
    SUGGESTIONS_CHANNEL_ID = 803320921393856602
    CARRY_SERVICE_REPS_CHANNEL_ID = 957773469431525396
    CRAFT_REPS_CHANNEL_ID = 860357041474371614
    MOD_ACTION_LOG_CHANNEL_ID = 823938991345893417
    BOOSTER_LOG_ID = 1033820228934709308
    EARNABLE_ROLES_CHANNEL_ID = 809891432050458655
    OUR_GUILDS_CHANNEL_ID = 803383229906157600
    SUPPORT_TICKETS_CHANNEL_ID = 765927458314387498
    HOW_TO_HELP_CHANNEL_ID = 876646094480736286
    INFO_CHANNEL_ID = 1050875691324952676
    BOOK_A_TUTOR = 805125682609782854

    # Categories
    MODERATOR_CHANNELS_CATEGORY_ID = 802982296617484378
    MODERATION_GUIDES_CATEGORY_ID = 905663798986301490
    ADMIN_CHANNELS_CATEGORY_ID = 801476879248261160
    LOGGING_CHANNELS_CATEGORY_ID = 989739103690051594
    CHANCELLOR_CHANNELS_CATEGORY_ID = 905664982656630805
    ARCHIVE_CATEGORY_ID = 859970790418153482

    # VCs
    UNI_VC_ID = 945493379599446056
    ALPHA_VC_ID = 945493468539654205
    KAPPA_VC_ID = 945493492434604072
    DELTA_VC_ID = 945493508398153808
    LAMBDA_VC_ID = 945493526047776889
    RHO_VC_ID = 945493556909473812
    MASTERS_VC_ID = 945493573263040522

    BRIDGE_CHANNEL_IDS = [812416103372292126, 819929855008178246, 843467314259296276,
                          944526812166361088]
    BRIDGE_BOT_IDS = [1021641891470651423, 1021641933866663986, 1021642115790413866,
                        1021642225223999508]

else:
    GUILD_ID = 1017925960177303612

    # Roles
    JR_MOD_ROLE_ID = 1017925960571568344
    MODERATOR_ROLE_ID = 1017925960571568345
    ADMIN_ROLE_ID = 1017925960592531591
    JR_ADMIN_ROLE_ID = 1017925960571568346
    GUILD_MEMBER_ROLE_ID = 1017925960458313783
    VERIFIED_ROLE_ID = 1017925960374435895
    ACTIVE_ROLE_ID = 1017925960416366669
    SB_UNI_MEMBER_ROLE_ID = 1017925960571568339
    SB_ALPHA_MEMBER_ROLE_ID = 1017925960571568338
    SB_KAPPA_MEMBER_ROLE_ID = 1017925960554786835
    SB_DELTA_MEMBER_ROLE_ID = 1017925960554786834
    SB_LAMBDA_MEMBER_ROLE_ID = 1017925960554786833
    SB_MASTERS_MEMBER_ROLE_ID = 1017925960554786829
    TOP_GUILD_ACTIVE_ROLE_ID = 1030894413016203365
    WEIGHT_BANNED_ROLE_ID = 1041542973055324200
    FRESHMAN_ROLE_ID = 1017925960500265079
    INSTRUCTOR_ROLE_ID = 1017925960525414561
    PROFESSOR_ROLE_ID = 1017925960525414562
    DEAN_ROLE_ID = 1017925960525414563
    PROVOST_ROLE_ID = 1017925960525414564
    PRIMUS_ROLE_ID = 1017925960525414565
    LEGATUS_ROLE_ID = 1017925960525414566
    BOOSTER_ROLE_ID = 1037515948283936900
    QUARANTINED_ROLE_ID = 1017925960592531592
    BOT_ROLE_ID = 1017925960592531590
    MUTED_ROLE_ID = 1017925960592531589
    SERVER_BOT_ROLE_ID = 1017925960500265080
    EVERYONE_ROLE_ID = 1017925960177303612

    # Channels
    QOTD_CHANNEL_ID = 1017925962194747402
    TOTAL_MEMBER_COUNT_VC_ID = 1017925961406238727
    SBU_BOT_LOGS_CHANNEL_ID = 1017925964690358399
    MOD_CHAT_CHANNEL_ID = 1017925964270932022
    ADMIN_CHAT_CHANNEL_ID = 1017925964690358392
    QOTD_ROLE_ID = 1017925960223436836
    BANNED_LIST_CHANNEL_ID = 1017925964065415294
    SUGGESTIONS_CHANNEL_ID = 1017925961779515488
    CARRY_SERVICE_REPS_CHANNEL_ID = 1022831138923884594
    CRAFT_REPS_CHANNEL_ID = 1017925963666960515
    MOD_ACTION_LOG_CHANNEL_ID = 1017925964270932020
    BOOSTER_LOG_ID = 1042923026213249084
    EARNABLE_ROLES_CHANNEL_ID = 0  # Channels used by crisis, can't be bothered
    OUR_GUILDS_CHANNEL_ID = 0
    SUPPORT_TICKETS_CHANNEL_ID = 0
    HOW_TO_HELP_CHANNEL_ID = 0
    INFO_CHANNEL_ID = 1062069251793485905
    BOOK_A_TUTOR = 0

    # Categories
    MODERATOR_CHANNELS_CATEGORY_ID = 0
    MODERATION_GUIDES_CATEGORY_ID = 0
    ADMIN_CHANNELS_CATEGORY_ID = 0
    LOGGING_CHANNELS_CATEGORY_ID = 0
    CHANCELLOR_CHANNELS_CATEGORY_ID = 0
    ARCHIVE_CATEGORY_ID = 0

    # VCs
    UNI_VC_ID = 1017925961406238728
    ALPHA_VC_ID = 1017925961406238729
    KAPPA_VC_ID = 1017925961603358890
    DELTA_VC_ID = 1017925961603358891
    LAMBDA_VC_ID = 1017925961603358892
    MASTERS_VC_ID = 1017925961603358895

    BRIDGE_CHANNEL_IDS = [1022179121457025196, 1017925963088146482, 1017925963088146483, 1023695383588782211]
    BRIDGE_BOT_IDS = [981945056267210842, 983145287264657508, 930410408932679720]

WEIGHT_ROLES_INFO = {
    "INSTRUCTOR": {
        "role_id": INSTRUCTOR_ROLE_ID,
        "weight_req": 700,
        "name": "Instructor",
        "previous": {}
    },
    "PROFESSOR": {
        "role_id": PROFESSOR_ROLE_ID,
        "weight_req": 2100,
        "name": "Professor",
        "previous": {INSTRUCTOR_ROLE_ID}
    },
    "DEAN": {
        "role_id": DEAN_ROLE_ID,
        "weight_req": 4200,
        "name": "Dean",
        "previous": {INSTRUCTOR_ROLE_ID, PROFESSOR_ROLE_ID}
    },
    "PROVOST": {
        "role_id": PROVOST_ROLE_ID,
        "weight_req": 8400,
        "name": "Provost",
        "previous": {INSTRUCTOR_ROLE_ID, PROFESSOR_ROLE_ID, DEAN_ROLE_ID}
    },
    "PRIMUS": {
        "role_id": PRIMUS_ROLE_ID,
        "weight_req": 12600,
        "name": "Primus",
        "previous": {INSTRUCTOR_ROLE_ID, PROFESSOR_ROLE_ID, DEAN_ROLE_ID, PROVOST_ROLE_ID}
    },
    "LEGATUS": {
        "role_id": PROVOST_ROLE_ID,
        "weight_req": 18800,
        "name": "Legatus",
        "previous": {INSTRUCTOR_ROLE_ID, PROFESSOR_ROLE_ID, DEAN_ROLE_ID, PROVOST_ROLE_ID, PRIMUS_ROLE_ID}
    }
}

GUILD_MEMBER_ROLES_IDS = [
    SB_UNI_MEMBER_ROLE_ID, SB_ALPHA_MEMBER_ROLE_ID, SB_DELTA_MEMBER_ROLE_ID,
    SB_KAPPA_MEMBER_ROLE_ID, SB_LAMBDA_MEMBER_ROLE_ID, SB_MASTERS_MEMBER_ROLE_ID
]
CRISIS_IGNORED_CATEGORIES = [
    MODERATOR_CHANNELS_CATEGORY_ID, MODERATION_GUIDES_CATEGORY_ID, ADMIN_CHANNELS_CATEGORY_ID,
    LOGGING_CHANNELS_CATEGORY_ID, CHANCELLOR_CHANNELS_CATEGORY_ID, ARCHIVE_CATEGORY_ID
]
CRISIS_IGNORED_ROLES = [
    JR_MOD_ROLE_ID, MODERATOR_ROLE_ID, JR_ADMIN_ROLE_ID, ADMIN_ROLE_ID, QUARANTINED_ROLE_ID, BOT_ROLE_ID,
    SERVER_BOT_ROLE_ID, MUTED_ROLE_ID, EVERYONE_ROLE_ID, UNI_BRIDGE_ROLE_ID, ALPHA_BRIDGE_ROLE_ID,
    KAPPA_BRIDGE_ROLE_ID, DELTA_BRIDGE_ROLE_ID, MASTERS_BRIDGE_ROLE_ID
]
CRISIS_REMOVE_VIEW_PERMS_CHANNELS = [
    EARNABLE_ROLES_CHANNEL_ID, OUR_GUILDS_CHANNEL_ID, SUPPORT_TICKETS_CHANNEL_ID, HOW_TO_HELP_CHANNEL_ID, BOOK_A_TUTOR
]

GUILDS_INFO = {
    "SB UNIVERSITY": {
        "role_id": SB_UNI_MEMBER_ROLE_ID,
        "guild_uuid": '6111fcb48ea8c95240436c57',
        "bridge_uuid": 'e3020a41a5c24597ad11a2348c46f815',
        "vc_id": UNI_VC_ID
    },
    "SB ALPHA PSI": {
        "role_id": SB_ALPHA_MEMBER_ROLE_ID,
        "guild_uuid": '604a765e8ea8c962f2bb3b7a',
        "bridge_uuid": 'a42c79f6f60841c38ae6ee1bf2eb7d35',
        "vc_id": ALPHA_VC_ID
    },
    # "SB KAPPA ETA": {
    #     "role_id": SB_KAPPA_MEMBER_ROLE_ID,
    #     "guild_uuid": '607a0d7c8ea8c9c0ff983976',
    #     "bridge_uuid": '384248632f3942069a80327a94150f6d',
    #     "vc_id": KAPPA_VC_ID
    # },
    # "SB DELTA OMEGA": {
    #     "role_id": SB_DELTA_MEMBER_ROLE_ID,
    #     "guild_uuid": '608d91e98ea8c9925cdb91b7',
    #     "bridge_uuid": 'd35172fc9191404c9671532569b62585',
    #     "vc_id": DELTA_VC_ID
    # },
    "SB LAMBDA PI": {
        "role_id": SB_LAMBDA_MEMBER_ROLE_ID,
        "guild_uuid": '60a16b088ea8c9bb7f6d9052',
        "bridge_uuid": '382b64daa73d46cb81759bcd4e13ce9f',
        "vc_id": LAMBDA_VC_ID
    },
    "SB MASTERS": {
        "role_id": SB_MASTERS_MEMBER_ROLE_ID,
        "guild_uuid": '570940fb0cf2d37483e106b3',
        "bridge_uuid": '87de0116d5834793a3f2ad0d99b4e8f2',
        "vc_id": MASTERS_VC_ID
    }
}





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
        "image": None
    },
    "How To Help": {
        "description": HOW_TO_HELP_STRING,
        "view": None,
        "image": None
    },
    "About Us": {
        "description": ABOUT_US_STRING,
        "view": None,
        "image": "https://imgur.com/SIjgNrX.jpg"
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
            }
        }
        ,
        "image": "https://imgur.com/SIjgNrX.jpg"
    },
    "Inactive List": {
        "description": INACTIVE_LIST_STRING,
        "view": None,
        "image": None
    }
}

