from nextcord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='botinfo')
    async def botinfo(self, ctx):
        await ctx.send('This is a simple Discord bot!')

def setup(bot):
    bot.add_cog(Info(bot))
