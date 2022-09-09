import discord
from discord.ext import commands
from io import BytesIO
from petpetgif import petpet as petpetgif


class Pat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Active")
    @commands.cooldown(1, 20, commands.BucketType.member)
    async def pat(self, ctx, image: discord.member.Member = None):
        if image == None:
            image = await ctx.author.avatar.read()
        if type(image) == discord.member.Member:
            image = await image.avatar.read()  # retrieve the image bytes
        source = BytesIO(image)
        dest = BytesIO()
        petpetgif.make(source, dest)
        dest.seek(0)
        await ctx.send(file=discord.File(dest, filename=f"{image[0]}-petpet.gif"))

    @pat.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Insufficient Permissions, you need active role or higher to use this command.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    @commands.command()
    async def convert(self, ctx, value : str):
        temp = int(value[:-1])
        if value[-1].upper() == 'C':
            fahrenheit = (temp * 9/5) + 32
            await ctx.send(f'{temp} celcius is {round(fahrenheit,2)} in fahrenheit.')
        elif value[-1].upper() == 'F':
            celsius = (temp - 32) * 5/9
            await ctx.send(f'{temp} fahrenheit is {round(celsius,2)} in celsius.')
        else:
            await ctx.send(f'Input values as `+convert 200f` to convert 200 fahrenheit to celsius')
def setup(bot):
    bot.add_cog(Pat(bot))
