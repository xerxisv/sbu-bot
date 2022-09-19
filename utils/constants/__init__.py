# CHAOS
import os
import dotenv

dotenv.load_dotenv()

SBU_LOGO_URL = 'https://cdn.discordapp.com/avatars/937099605265485936/8a5d786e369fdda9f355f12eaf0487fb.png?size=4096'

# Pseudo constants
GUILD_ID = 0

BOT_OWNER_ROLE_ID = 0  # the bot administrator role, has access to load, unload commands
JR_MOD_ROLE_ID = 0
MODERATOR_ROLE_ID = 0
JR_ADMIN_ROLE_ID = 0
ADMIN_ROLE_ID = 0
QOTD_ROLE_ID = 0
GUILD_MEMBER_ROLE_ID = 0
VERIFIED_ROLE_ID = 0
SB_UNI_MEMBER_ROLE_ID = 0
SB_KAPPA_MEMBER_ROLE_ID = 0
SB_ALPHA_MEMBER_ROLE_ID = 0
SB_RHO_MEMBER_ROLE_ID = 0
SB_MASTERS_MEMBER_ROLE_ID = 0
SB_DELTA_MEMBER_ROLE_ID = 0
SB_LAMBDA_MEMBER_ROLE_ID = 0

QOTD_CHANNEL_ID = 0
MOD_CHAT_CHANNEL_ID = 0
BANNED_LIST_CHANNEL_ID = 0
SUGGESTIONS_CHANNEL_ID = 0
SBU_BOT_LOGS_CHANNEL_ID = 0
CARRY_SERVICE_REPS_CHANNEL_ID = 0
MOD_ACTION_LOG_CHANNEL_ID = 0

TOTAL_MEMBER_COUNT_VC_ID = 0
MEMBER_COUNT_VC_IDS = []

# User constants for chat triggers
ADU_ID = 397389995113185293
FLOP_ID = 615987518890049555
PINGU_ID = 381494697073573899
NOOMI_ID = 566329261535920175
WINCHAE_ID = 797274543042986024
PLEB_ID = 519985798393626634
SKYE_ID = 681475158975971329
MEGA_ID = 675106662302089247
COCOMONKEY_ID = 283326249735028736
RAIZEL_ID = 241589674131456000


if os.getenv('MODE') == 'PRODUCTION':
    GUILD_ID = 764326796736856066

    # Roles
    BOT_OWNER_ROLE_ID = 1015989853202169877
    JR_MOD_ROLE_ID = 924332988743966751
    MODERATOR_ROLE_ID = 801634222577156097
    JR_ADMIN_ROLE_ID = 808070562046935060
    ADMIN_ROLE_ID = 766041783137468506
    GUILD_MEMBER_ROLE_ID = 0
    VERIFIED_ROLE_ID = 0
    SB_UNI_MEMBER_ROLE_ID = 803695821094125585
    SB_ALPHA_MEMBER_ROLE_ID = 821080619332796437
    SB_KAPPA_MEMBER_ROLE_ID = 832803831166926859
    SB_DELTA_MEMBER_ROLE_ID = 838121681931075594
    SB_LAMBDA_MEMBER_ROLE_ID = 843871813481267270
    SB_RHO_MEMBER_ROLE_ID = 879979053396942848
    SB_MASTERS_MEMBER_ROLE_ID = 944524838553399326

    # Channels
    QOTD_CHANNEL_ID = 868630191080083476
    TOTAL_MEMBER_COUNT_VC_ID = 890288776302190602
    SBU_BOT_LOGS_CHANNEL_ID = 946591422616838264
    MOD_CHAT_CHANNEL_ID = 802982854291488808
    QOTD_ROLE_ID = 868630686712614922
    BANNED_LIST_CHANNEL_ID = 830188559964307526
    SUGGESTIONS_CHANNEL_ID = 803320921393856602
    CARRY_SERVICE_REPS_CHANNEL_ID = 957773469431525396
    MOD_ACTION_LOG_CHANNEL_ID = 823938991345893417
    MEMBER_COUNT_VC_IDS = [945493379599446056, 945493468539654205, 945493492434604072, 945493508398153808,
                           945493526047776889, 945493540748791899, 945493556909473812, 945493573263040522]

else:
    GUILD_ID = 1017925960177303612

    # Roles
    BOT_OWNER_ROLE_ID = 1017925960592531587
    JR_MOD_ROLE_ID = 1017925960571568344
    MODERATOR_ROLE_ID = 1017925960571568345
    ADMIN_ROLE_ID = 1017925960592531591
    JR_ADMIN_ROLE_ID = 1017925960571568346
    GUILD_MEMBER_ROLE_ID = 1017925960458313783
    VERIFIED_ROLE_ID = 1017925960374435895
    SB_UNI_MEMBER_ROLE_ID = 1017925960571568339
    SB_ALPHA_MEMBER_ROLE_ID = 1017925960571568338
    SB_KAPPA_MEMBER_ROLE_ID = 1017925960554786835
    SB_DELTA_MEMBER_ROLE_ID = 1017925960554786834
    SB_LAMBDA_MEMBER_ROLE_ID = 1017925960554786833
    SB_RHO_MEMBER_ROLE_ID = 1017925960554786831
    SB_MASTERS_MEMBER_ROLE_ID = 1017925960554786829

    # Channels
    QOTD_CHANNEL_ID = 1017925962194747402
    TOTAL_MEMBER_COUNT_VC_ID = 1017925961406238727
    SBU_BOT_LOGS_CHANNEL_ID = 1017925964690358399
    MOD_CHAT_CHANNEL_ID = 1017925964270932022
    QOTD_ROLE_ID = 1017925960223436836
    BANNED_LIST_CHANNEL_ID = 1017925964065415294
    SUGGESTIONS_CHANNEL_ID = 1017925961779515488
    CARRY_SERVICE_REPS_CHANNEL_ID = 1017925963474010117
    MOD_ACTION_LOG_CHANNEL_ID = 1017925964270932020
    MEMBER_COUNT_VC_IDS = [1017925961406238728, 1017925961406238729, 1017925961603358890, 1017925961603358891,
                           1017925961603358892, 1017925961603358893, 1017925961603358894, 1017925961603358895]


GUILD_MEMBER_ROLES_IDS = [SB_UNI_MEMBER_ROLE_ID, SB_ALPHA_MEMBER_ROLE_ID, SB_DELTA_MEMBER_ROLE_ID,
                          SB_KAPPA_MEMBER_ROLE_ID, SB_LAMBDA_MEMBER_ROLE_ID,
                          SB_RHO_MEMBER_ROLE_ID, SB_MASTERS_MEMBER_ROLE_ID]

GUILDS_INFO = {
    "SB UNIVERSITY": {
        "role_id": SB_UNI_MEMBER_ROLE_ID,
        "guild_uuid": '6111fcb48ea8c95240436c57',
        "bridge_uuid": 'e3020a41a5c24597ad11a2348c46f815'
    },
    "SB ALPHA PSI": {
        "role_id": SB_ALPHA_MEMBER_ROLE_ID,
        "guild_uuid": '604a765e8ea8c962f2bb3b7a',
        "bridge_uuid": 'a42c79f6f60841c38ae6ee1bf2eb7d35'
    },
    "SB KAPPA ETA": {
        "role_id": SB_KAPPA_MEMBER_ROLE_ID,
        "guild_uuid": '607a0d7c8ea8c9c0ff983976',
        "bridge_uuid": '384248632f3942069a80327a94150f6d'
    },
    "SB DELTA OMEGA": {
        "role_id": SB_DELTA_MEMBER_ROLE_ID,
        "guild_uuid": '608d91e98ea8c9925cdb91b7',
        "bridge_uuid": 'd35172fc9191404c9671532569b62585'
    },
    "SB LAMBDA PI": {
        "role_id": SB_LAMBDA_MEMBER_ROLE_ID,
        "guild_uuid": '60a16b088ea8c9bb7f6d9052',
        "bridge_uuid": 'c767caebf1da4039ad47be2f9b8a61c6'
    },
    "SB RHO XI": {
        "role_id": SB_RHO_MEMBER_ROLE_ID,
        "guild_uuid": '6125800e8ea8c92e1833e851',
        "bridge_uuid": '4e65ce7ae36e4c64907bc525b4aab845'
    },
    "SB MASTERS": {
        "role_id": SB_MASTERS_MEMBER_ROLE_ID,
        "guild_uuid": '570940fb0cf2d37483e106b3',
        "bridge_uuid": 'de5e3ff48a9e42d18b4fa1dc62b779cf'
    }
}
