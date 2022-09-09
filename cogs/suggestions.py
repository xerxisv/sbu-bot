import discord
from discord.ext import commands
import datetime
import json


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        with open('suggestions.json') as fp:
            listObj = json.load(fp)
        num1 = len(listObj) + 1

        suggestembed = discord.Embed(
            title=f'Suggestion',
            description=f'{suggestion}',
            timestamp=datetime.datetime.utcnow(),
            colour=0x8F49EA
        )
        if ctx.message.author.avatar == None:
                suggestembed.set_author(name=f'Suggested by {ctx.message.author}')
        else:
            suggestembed.set_author(name=f'Suggested by {ctx.message.author}', icon_url=ctx.message.author.avatar)
        suggestembed.set_footer(text=f'Suggestion number {num1}')
        suggestembed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/937099605265485936/8a5d786e369fdda9f355f12eaf0487fb.png?size=4096")
        channel = self.bot.get_channel(803320921393856602)
        message = await channel.send(embed=suggestembed)
        await ctx.send("Suggestion sent to <#803320921393856602>")
        await message.add_reaction('✅')
        await message.add_reaction('❌')

        data = {
            "number": num1,
            "messageid": message.id,
            "suggestion": str(suggestion),
            "author": str(ctx.author),
            "authorid": ctx.author.id
        }
        listvar = list(listObj)
        listvar.append(data)

        with open('suggestions.json', 'w') as json_file:
            json.dump(listvar, json_file,
                    indent=4,
                    separators=(',', ': '))

    @commands.command()
    @commands.has_role("Administrator")
    async def approve(self, ctx, number: int, *, reason=None):
        with open('suggestions.json') as fp:
            listObj = json.load(fp)
        check = False
        for s in range(len(listObj)):
            if listObj[s]["number"] == number:
                check = True
                var = s
        if not check:
            await ctx.send("Suggestion not found.")
            return
        suggestembed = discord.Embed(
            title=f'Approved',
            description=f'{listObj[var]["suggestion"]}',
            timestamp=datetime.datetime.utcnow(),
            colour=0x0CE60C
        )
        suggestembed.set_author(name=f'Suggested by {listObj[var]["author"]}')
        suggestembed.set_footer(text=f'Suggestion number {number} | Approved by {ctx.author}')
        suggestembed.add_field(name="Reason", value=f"{reason}", inline=False)
        suggestembed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/937099605265485936/8a5d786e369fdda9f355f12eaf0487fb.png?size=4096")
        message = self.bot.get_channel(803320921393856602).get_partial_message(listObj[var]["messageid"])
        await message.edit(embed=suggestembed)
        approveembed = discord.Embed(
            title=f'Approved',
            description=f'Suggestion number {number} approved successfully.',
            timestamp=datetime.datetime.utcnow(),
            colour=0x0CE60C
        )
        try:
            member = await self.bot.fetch_user(listObj[var]["authorid"])
            await member.send(embed=suggestembed)
            approveembed.add_field(name="Direct Message", value=f"{member} dmed successfully", inline=False)
            await ctx.send(embed=approveembed)
        except:
            approveembed.add_field(name="Direct Message", value=f"Member unable to be dmed", inline=False)
            await ctx.send(embed=approveembed)
        await ctx.delete()

    @commands.command()
    @commands.has_role("Administrator")
    async def deny(self, ctx, number: int, *, reason=None):
        with open('suggestions.json') as fp:
            listObj = json.load(fp)
        check = False
        for s in range(len(listObj)):
            if listObj[s]["number"] == number:
                check = True
                var = s
        if not check:
            await ctx.send("Suggestion not found.")
            return
        suggestembed = discord.Embed(
            title=f'Denied',
            description=f'{listObj[var]["suggestion"]}',
            timestamp=datetime.datetime.utcnow(),
            colour=0xFF0000
        )
        suggestembed.set_author(name=f'Suggested by {listObj[var]["author"]}')
        suggestembed.set_footer(text=f'Suggestion number {number} | Denied by {ctx.author}')
        suggestembed.add_field(name="Reason", value=f"{reason}", inline=False)
        suggestembed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/937099605265485936/8a5d786e369fdda9f355f12eaf0487fb.png?size=4096")
        message = self.bot.get_channel(803320921393856602).get_partial_message(listObj[var]["messageid"])
        await message.edit(embed=suggestembed)
        approveembed = discord.Embed(
            title=f'Denied',
            description=f'Suggestion number {number} denied successfully.',
            timestamp=datetime.datetime.utcnow(),
            colour=0x0CE60C
        )
        try:
            member = await self.bot.fetch_user(listObj[var]["authorid"])
            await member.send(embed=suggestembed)
            approveembed.add_field(name="Direct Message", value=f"{member} dmed successfully", inline=False)
            await ctx.send(embed=approveembed)
        except:
            approveembed.add_field(name="Direct Message", value=f"Member unable to be dmed", inline=False)
            await ctx.send(embed=approveembed)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Suggestions(bot))
