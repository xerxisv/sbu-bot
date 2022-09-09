import discord
from discord.ext import commands
from discord.utils import get
import requests
import os


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Add the role if in guild")
    async def verify(self, ctx, arg1: str = None):
        key = os.getenv("apikey")
        if arg1 is None:
            embed = discord.Embed(title=f'Error', description='Please enter a user \n `+verify ObbyTrusty`',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        member = ctx.message.author
        temp_var = "Attempt to verify: " + str(ctx.message.author)
        print(temp_var)
        response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{arg1}')
        try:
            uuid = response.json()['id']
            print(uuid)
        except KeyError as e:
            print(e)
            embed = discord.Embed(title=f'Error',
                                  description='Error fetching information from the API. Recheck the spelling of your '
                                              'IGN',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        for role1 in ["SB Lambda Pi Member", "SB Theta Tau Member", "SB Delta Omega Member", "SB Iota Theta Member",
                      "SB University Member", "SB Rho Xi Member", "SB Kappa Eta Member", "SB Alpha Psi Member",
                      "SB Masters Member"]:

            role = discord.utils.get(ctx.guild.roles, name=role1)
            if role in member.roles:
                await member.remove_roles(role)
        response = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={uuid}')
        if response.status_code != 200:
            embed = discord.Embed(title=f'Error',
                                  description='Error fetching information from the API. Try again later',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        player = response.json()
        response = requests.get(f'https://api.hypixel.net/guild?key={key}&player={uuid}')
        guild = response.json()
        check = False
        try:
            if player['player']['socialMedia']['links']['DISCORD'] == str(ctx.author):
                pass
            else:
                embed = discord.Embed(title=f'Error',
                                      description='The discord linked with your hypixel account is not the same as '
                                                  'the one you are trying to verify with. \n You can connect your '
                                                  'discord following https://youtu.be/6ZXaZ-chzWI',
                                      colour=0xFF0000)
                await ctx.reply(embed=embed)
                return
        except KeyError:
            embed = discord.Embed(title=f'Error',
                                  description='The discord linked with your hypixel account is not the same as '
                                              'the one you are trying to verify with. \n You can connect your '
                                              'discord following https://youtu.be/6ZXaZ-chzWI',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        temp_test = False
        try:
            if guild["guild"]["name"] in ["SB Lambda Pi", "SB Theta Tau", "SB Delta Omega", "SB Iota Theta",
                                          "SB Uni", "SB Rho Xi", "SB Kappa Eta", "SB Alpha Psi", "SB Masters"]:
                pass
        except KeyError:
            temp_test = True
            embed = discord.Embed(title=f'Verification',
                                  description='You are not in any of the SBU guilds. You are now verified without '
                                              'the guild member roles.',
                                  colour=0x800080)
            pass
        if temp_test:
            pass
        else:
            if guild["guild"]["name"] in ["SB Lambda Pi", "SB Theta Tau", "SB Delta Omega", "SB Iota Theta",
                                          "SB Uni", "SB Rho Xi", "SB Kappa Eta", "SB Alpha Psi", "SB Masters"]:
                check = True
                pass
            else:
                embed = discord.Embed(title=f'Verification',
                                      description='You are not in any of the SBU guilds. You are now verified without '
                                                  'the guild member roles.',
                                      colour=0x800080)
            temp = False
            if guild["guild"]["name"] == "SB Uni":
                temp = True
                guild_role = "SB University Member"
                embed = discord.Embed(title=f'Verification',
                                      description=f'You have been verified as a member of {guild["guild"]["name"]}',
                                      colour=0x008000)
            if check and temp is not True:
                embed = discord.Embed(title=f'Verification',
                                      description=f'You have been verified as a member of {guild["guild"]["name"]}',
                                      colour=0x008000)
                guild_role = guild["guild"]["name"] + " Member"
        role = get(member.guild.roles, name="Verified")
        role1 = get(member.guild.roles, name="Guild Member")
        if check:
            role2 = get(member.guild.roles, name=guild_role)
            await member.add_roles(role1)
            await member.add_roles(role2)
        await member.add_roles(role)

        try:
            await member.edit(nick=player['player']["displayname"])
        except:
            embed.add_field(name="Nickname:", value="Unable to edit nickname.")
        member = ctx.message.author
        role = get(member.guild.roles, name="Verified")
        await member.add_roles(role)
        await ctx.reply(embed=embed)

    @commands.command()
    async def unverify(self, ctx):
        member = ctx.message.author
        for role1 in ["SB Lambda Pi Member", "SB Theta Tau Member", "SB Delta Omega Member",
                      "SB Iota Theta Member",
                      "SB University Member", "SB Rho Xi Member", "SB Kappa Eta Member", "SB Alpha Psi Member",
                      "SB Masters Member", "Verified", "MVP", "MVP+", "MVP++", "VIP", "VIP+", "Guild Member"]:
            role = discord.utils.get(ctx.guild.roles, name=role1)
            if role in member.roles:
                await member.remove_roles(role)
        embed = discord.Embed(title=f'Verification',
                              description=f'You have been unverified.',
                              colour=0x008000)
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Verify(bot))
