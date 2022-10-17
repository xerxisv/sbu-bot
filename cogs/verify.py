import os
import aiosqlite

import discord
import requests
from discord.ext import commands

from utils.constants import GUILD_MEMBER_ROLES_IDS, GUILD_MEMBER_ROLE_ID, GUILDS_INFO, \
    VERIFIED_ROLE_ID
from utils.database import DBConnection
from utils.error_utils import log_error
from utils.database.schemas import User

error_embed = discord.Embed(title=f'Error',
                            description='Something went wrong. Please try again later',
                            colour=0xFF0000)


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db: aiosqlite.Connection = DBConnection().get_db()
        self.key = os.getenv("apikey")

    @commands.command(description="Add the role if in guild")
    @commands.cooldown(1, 5)
    async def verify(self, ctx: commands.Context, ign: str = None):
        await ctx.trigger_typing()

        if ign is None:  # No IGN was inputted
            embed = discord.Embed(title=f'Error', description='Please enter a user \n `+verify RealMSpeed`',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return

        try:
            # Convert IGN to UUID
            response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}')

            assert response.status_code != 204  # Only returns 204 when the name inputted is wrong

            uuid = response.json()['id']
            ign = response.json()["name"]

            del response
        except AssertionError:  # In case of a 204
            embed = discord.Embed(title=f'Error',
                                  description='Error fetching information from the API. Recheck the spelling of your '
                                              'IGN',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        except Exception as exception:  # In case of anything else
            await log_error(ctx, exception)

            await ctx.reply(embed=error_embed)
            return

        # Remove the previous guild member role from the command invoker
        member: discord.Member = ctx.message.author
        await member \
            .remove_roles(*[discord.Object(_id) for _id in GUILD_MEMBER_ROLES_IDS],
                          reason='verification process',
                          atomic=False)

        try:
            # Fetch player data
            response = requests.get(f'https://api.hypixel.net/player?key={self.key}&uuid={uuid}')
            assert response.status_code == 200, 'api.hypixel.net/player did not return a 200'
            player = response.json()['player']

            # Fetch guild data
            response = requests.get(f'https://api.hypixel.net/guild?key={self.key}&player={uuid}')
            assert response.status_code == 200, 'api.hypixel.net/guild did not return a 200'
            guild = response.json()['guild']

        except Exception as exception:  # Log any errors that might araise
            await log_error(ctx, exception)

            await ctx.reply(embed=error_embed)
            return

        try:
            if player['socialMedia']['links']['DISCORD'] != str(ctx.author):
                embed = discord.Embed(title=f'Error',
                                      description='The discord linked with your hypixel account is not the same as '
                                                  'the one you are trying to verify with. \n You can connect your '
                                                  'discord following https://youtu.be/6ZXaZ-chzWI',
                                      colour=0xFF0000)
                await ctx.reply(embed=embed)
                return
        except KeyError:
            embed = discord.Embed(title=f'Error',
                                  description='You haven\'t linked your discord with your hypixel account yet\n'
                                              'You can connect your discord following https://youtu.be/6ZXaZ-chzWI',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        except Exception as exception:
            await log_error(ctx, exception)

            await ctx.reply(embed=error_embed)
            return

        embed = discord.Embed()

        is_in_guild = False

        if guild is None \
                or guild["name"] not in ["SB Lambda Pi", "SB Theta Tau", "SB Delta Omega", "SB Iota Theta",
                                         "SB Uni", "SB Rho Xi", "SB Kappa Eta", "SB Alpha Psi", "SB Masters"]:

            embed = discord.Embed(title=f'Verification',
                                  description='You are not in any of the SBU guilds. You are now verified without '
                                              'the guild member roles.',
                                  colour=0x800080)

        else:
            is_in_guild = True

        await member \
            .add_roles(*[discord.Object(_id) for _id in [VERIFIED_ROLE_ID, GUILD_MEMBER_ROLE_ID]],
                       reason='Verification Complete', atomic=False)

        verified_member = User(uuid, member.id, ign)

        if is_in_guild:
            await member\
                .add_roles(discord.Object(GUILDS_INFO[guild["name"].upper()]['role_id']), atomic=False)

            embed = discord.Embed(title=f'Verification',
                                  description=f'You have been verified as a member of {guild["name"]}',
                                  colour=0x008000)

            verified_member.guild_uuid = guild['_id']

        await self.db.execute(*(verified_member.insert()))
        await self.db.commit()

        try:
            await member.edit(nick=player["displayname"])

        except Exception as exception:
            embed.add_field(name="Nickname:", value="Unable to edit nickname.")

            await log_error(ctx, exception)

        await ctx.reply(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5)
    async def unverify(self, ctx: commands.Context):
        await ctx.trigger_typing()
        member: discord.Member = ctx.message.author

        await member \
            .remove_roles(*[discord.Object(_id) for _id in
                            [*GUILD_MEMBER_ROLES_IDS, GUILD_MEMBER_ROLE_ID, VERIFIED_ROLE_ID]],
                          atomic=False
                          )

        await self.db.execute(User.delete_row_with_id(member.id))
        await self.db.commit()

        embed = discord.Embed(title=f'Verification',
                              description=f'You have been unverified.',
                              colour=0x008000)
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Verify(bot))
