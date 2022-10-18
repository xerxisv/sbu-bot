import discord
from random import choice

triggers = {
    "MEOW": {
        "owner": [397389995113185293],
        "reply": 'Meow'
    },
    "MEOWO": {
        "owner": [397389995113185293],
        "reply": 'UwU meow'
    },
    "FLOP": {
        "owner": [615987518890049555],
        "reply": ["<:turtleonfire:1021834121347084309>", "Fleee", "All hail King Flop",
                  "https://i.imgur.com/pnruanZ.png"]
    },
    "PINGU": {
        "owner": [381494697073573899],
        "reply": ["<a:poguin:933279319579561986>", "<a:pingupat:932962348908560417>", "UwU",
                  "https://tenor.com/view/noot-noot-apocalypse-gif-25788876"]
    },
    "NEO": {
        "owner": [566329261535920175],
        "reply": 'op'
    },
    "WINDOW": {
        "owner": [797274543042986024],
        "reply": 'https://tenor.com/view/monkey-gif-8660294'
    },
    "PLEB": {
        "owner": [519985798393626634],
        "reply": 'shitting on the bw gamers.'
    },
    "MEEP": {
        "owner": [681475158975971329],
        "reply": 'https://tenor.com/view/meap-phineas-and-ferb-phineas-and-ferb-meap-meep-gif-14038245'
    },
    "MEGA": {
        "owner": [675106662302089247],
        "reply": 'https://tenor.com/view/megalorian-tykhe-gif-24043314'
    },
    "HMM": {
        "owner": [283326249735028736],
        "reply": 'mhm'
    },
    "CHOMP": {
        "owner": [241589674131456000],
        "reply": 'https://tenor.com/view/cat-bite-funny-chomp-gif-16986241'
    },
    "I AGREE": {
        "owner": [309231901212672001],
        "reply": 'https://tenor.com/view/metal-gear-rising-gif-25913914'
    },
    "CANNIBALISM": {
        "owner": [606917358438580224, 241589674131456000],
        "reply": ["Pog!", "Noses!", "Toes!", "Fungus!", "https://i.imgur.com/IJ8URxl.jpg"]
    },
    "MUDKIP": {
        "owner": [895488539775598603],
        "reply": 'https://tenor.com/view/mudkip-spin-gif-24834722'
    },
    "RANDOM": {
        "owner": [491654047741509633],
        "reply": 'https://cdn.discordapp.com/emojis/967203616966459412'
    },
    "FIRE": {
        "owner": [856492201529835521],
        "reply": 'https://cdn.discordapp.com/emojis/943095611161460739.webp?size=128&quality=lossless'
    },
    "ZMAJ": {
        "owner": [852647923875446816],
        "reply": 'https://media.discordapp.net/attachments/1027212487008989284/1027212547591508070/cat-angry-cat.gif'
    },
    "MHM": {
        "owner": [665885831856128001],
        "reply": 'mhm'
    },
    "🔥🔥": {
        "owner": [149565760950239232],
        "reply": 'Go to school.'
    }
}


async def handle_trigger(msg: discord.Message) -> None:
    upper_msg = msg.content.upper()

    trigger = triggers[upper_msg]
    if msg.author.id not in trigger['owner']:
        return

    reply = trigger['reply'] if type(trigger['reply']) is str else choice(trigger['reply'])
    await msg.reply(reply)


def is_trigger(msg: str) -> bool:
    return msg.upper() in triggers.keys()
