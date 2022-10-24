import discord

from utils.constants import JR_MOD_ROLE_ID, MOD_ACTION_LOG_CHANNEL_ID


async def handle_warn(message: discord.Message):
    # Split the message on every space character
    split_msg = message.content.split(' ')
    # If the message is less than 2 words long then it's an invalid warn command, return
    if len(split_msg) < 3:
        return

    # Else remove the discord formatting characters from the mention
    user_id = split_msg[1].replace('<', '').replace('@', '').replace('>', '')

    # And check if it was indeed a mention
    if not user_id.isnumeric():
        return

    # Fetch the member with the specified ID
    member: discord.Member = message.guild.get_member(int(user_id))

    if member is None or member.get_role(JR_MOD_ROLE_ID) is None:
        return

    await message.guild.get_channel(MOD_ACTION_LOG_CHANNEL_ID).send(
        f"Moderator: {message.author.mention} \n"
        f"User: {member.mention} \n"
        f"Action: Warn \n"
        f"Reason: {' '.join(split_msg[2:])}")

    await message.channel.send("Log created")


def is_warn(message: str):
    return message.startswith("!warn")
