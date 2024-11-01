import nextcord
from nextcord.ext import commands
from nextcord import Embed, Color

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rule(self, ctx):
        embed = Embed(
            title="📢 Welcome to the GDGC BINUS International University Discord Server!",
            description="Please read the rules below for a positive environment.",
            color=Color.blue()
        )

        embed.add_field(
            name="📜 General Rules",
            value=(
                "1. **Respect All Members:** Treat everyone with kindness.\n"
                "2. **No Spamming:** Avoid excessive posts and stay relevant.\n"
                "3. **No NSFW Content:** Do not share inappropriate content.\n"
                "4. **Language:** Keep conversations in **English**.\n"
                "5. **Follow TOS:** Ensure all activities comply with Discord's TOS."
            ),
            inline=False
        )

        embed.add_field(
            name="💻 Channel-Specific Rules",
            value=(
                "1. **#general-chat:** For tech discussions. Stay professional.\n"
                "2. **#off-topic:** Non-tech chats are welcome. Keep it friendly.\n"
                "3. **#project-showcase:** Share your projects and get feedback.\n"
                "4. **#resources:** Post tutorials and learning materials.\n"
                "5. **#ask-for-help:** Ask specific questions.\n"
                "6. **#tech-talk:** For in-depth technical discussions."
            ),
            inline=False
        )

        embed.add_field(
            name="⚖️ Moderation and Enforcement",
            value=(
                "1. **Warnings:** The Core Team can issue warnings for rule violations.\n"
                "2. **Reporting:** Report issues to the Core Team via DM or the **#report** channel.\n"
                "3. **Appeals:** Provide a clear explanation if you believe a punishment was unfair."
            ),
            inline=False
        )

        embed.set_footer(text="Thank you for being part of GDGC BINUS! 🚀")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Rules(bot))