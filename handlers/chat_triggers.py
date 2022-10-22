import discord
from random import choice

triggers = {
    "LINKS": {
        "owner": [491654047741509633, 351827324758523905, 309231901212672001,
                  606917358438580224, 519985798393626634, 241589674131456000],
        "reply": "MEE6 Dashboard: <https://mee6.xyz/dashboard/>\n"
                 "Ticket Tool: <https://tickettool.xyz/manage-servers>\n"
                 "YAGPDB: <https://yagpdb.xyz/>\n"
                 "Giveaway Boat: <https://giveaway.boats/dashboard/>\n"
                 "Tatsu Dashboard: <https://tatsu.gg/>\n"
                 "Dyno: <https://dyno.gg/>\n"
                 "Wick Dashboard: <https://wickbot.com/>\n"
                 "SBU Bot: <https://github.com/xerxisv/sbu-bot/>"
    },
    "MEOW": {
        "owner": [397389995113185293],
        "reply": 'Meow'
    },
    "MEOWO": {
        "owner": [397389995113185293],
        "reply": 'UwU meow'
    },
    "PLEB": {
        "owner": [519985798393626634],
        "reply": 'shitting on the bw gamers.'
    },
    "I AGREE": {
        "owner": [309231901212672001],
        "reply": 'https://tenor.com/view/metal-gear-rising-gif-25913914'
    },
    "CANNIBALISM": {
        "owner": [606917358438580224, 241589674131456000],
        "reply": ["Pog!", "Noses!", "Toes!", "Fungus!", "https://i.imgur.com/IJ8URxl.jpg"]
    },
    "RANDOM": {
        "owner": [491654047741509633],
        "reply": 'https://cdn.discordapp.com/emojis/967203616966459412'
    },
    "MHM": {
        "owner": [665885831856128001],
        "reply": 'mhm'
    },
    "TOASTER": {
        "owner": [220578609335631872],
        "reply": 'https://cdn.discordapp.com/attachments/1031248294627790989/1033067050245050489/icystickercomm.png'
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
