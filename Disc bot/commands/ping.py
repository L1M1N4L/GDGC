from nextcord.ext import commands
import nextcord
import time

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        # Measure the round-trip time for the ping
        start_time = time.time()
        message = await ctx.send('Pinging...')
        end_time = time.time()

        # Calculate the ping (in milliseconds)
        latency = (end_time - start_time) * 1000

        # Create an embed to display the ping information
        embed = nextcord.Embed(
            title="🏓 Pong!",
            description=f"**Bot Latency:** {latency:.2f} ms\n**API Latency:** {self.bot.latency * 1000:.2f} ms",
            color=nextcord.Color.green()  # Change the color as needed
        )

        # Edit the original message to include the embed
        await message.edit(content=None, embed=embed)

def setup(bot):
    bot.add_cog(Ping(bot))
