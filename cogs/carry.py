import discord
from discord.ext import commands
import json


class Reputations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def repgive(self, ctx, member: discord.Member, *, reason):
        if ctx.author.id == member.id:
            await ctx.send("You can't rep yourself.")
            return
        with open('reputation.json') as fp:
            listObj = json.load(fp)
        num1 = len(listObj) + 1
        count = 0

        for value in range(len(listObj)):
            if listObj[value]["repgiven"] == member.id:
                count = count + 1
        count = count + 1
        repembed = discord.Embed(
            title=f'Reputation Given',
            description=f'Reason: {reason}',
            colour=0x8F49EA
        )
        repembed.set_author(name=f'Reputation by {ctx.message.author}')
        repembed.set_footer(text=f'Global reputation number {num1} | Reputation Number {count} for {member}')
        repembed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/937099605265485936/8a5d786e369fdda9f355f12eaf0487fb.png?size=4096")
        channel = self.bot.get_channel(957773469431525396)
        message = await channel.send(embed=repembed)
        await ctx.send(f"Reputation added for {member}")
        data = {
            "number": num1,
            "messageid": message.id,
            "reason": reason,
            "authorid": ctx.author.id,
            "repgiven": member.id
        }
        listvar = list(listObj)
        listvar.append(data)

        with open('reputation.json', 'w') as json_file:
            json.dump(listvar, json_file,
                      indent=4,
                      separators=(',', ': '))

    @repgive.error
    async def repgive_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Incorrect format. Use `+repgive @mention Reason`")

    @commands.command()
    @commands.has_role("Administrator")
    async def delrep(self, ctx, number: int):
        with open('reputation.json', 'r') as f:
            reputation = json.load(f)
        check = False
        for s in range(len(reputation)):
            if reputation[s]["number"] == number:
                check = True
                var = s

        if not check:
            embed = discord.Embed(title=f'Error', description=f'Reputation number {number} not found.',
                                  colour=0xFF0000)
            await ctx.reply(embed=embed)
            return
        message = self.bot.get_channel(957773469431525396).get_partial_message(reputation[var]["messageid"])
        await message.delete()
        for i in range(len(reputation)):
            if reputation[i]["number"] == number:
                reputation.pop(i)
                break
        with open('reputation.json', 'w') as f:
            json.dump(reputation, f, indent=4)
        embed = discord.Embed(title=f'Completed Successfully', description=f'Reputation number {number} removed.',
                              colour=0xFF0000)
        await ctx.reply(embed=embed)
        return

    @delrep.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Insufficient Permissions, only administrators can remove reputations.")


def setup(bot):
    bot.add_cog(Reputations(bot))

