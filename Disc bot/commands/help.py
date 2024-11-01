import nextcord
from nextcord.ext import commands

class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bothelp', aliases=['commands'], help='Displays the help message.')
    async def help_command(self, ctx):
        embed = nextcord.Embed(
            title="🚀 Welcome to GDGC Binus International ! 🚀",
            description=(
                "Greetings, tech enthusiast! 👋 Ready to explore the world of Google Developer "
                "technologies? This bot is your companion in the exciting journey through GDGC "
                "Binus International. Whether you're looking to learn, collaborate, or innovate, "
                "we've got you covered!\n\n"
                "Here's your toolkit of awesome commands:"
            ),
            color=nextcord.Color.brand_green()
        )

        # Add a thumbnail
        embed.set_thumbnail(url="https://example.com/path/to/your/bot/logo.png")

        # Group commands by cog
        cog_commands = {}
        for command in self.bot.commands:
            if command.hidden:
                continue  # Skip hidden commands
            cog_name = command.cog_name or "General"
            if cog_name not in cog_commands:
                cog_commands[cog_name] = []
            cog_commands[cog_name].append(command)

        # Add fields for each cog
        for cog_name, commands in cog_commands.items():
            emoji = self.get_category_emoji(cog_name)
            command_list = "\n".join([f"`{cmd.name}` - {cmd.help or 'No description'}" for cmd in commands])
            embed.add_field(name=f"{emoji} **{cog_name}**", value=command_list, inline=False)

        # Add a footer
        embed.set_footer(text="💡 Tip: Use !commandinfo <command> for more details on a specific command.")

        await ctx.send(embed=embed)

    @commands.command(name='commandinfo', help='Get detailed info about a specific command.')
    async def help_specific_command(self, ctx, command_name: str):
        command = self.bot.get_command(command_name)
        if command is None:
            await ctx.send(f"🔍 Oops! No command named '{command_name}' found. Double-check and try again!")
            return

        embed = nextcord.Embed(
            title=f"📚 Command Details: {command.name}",
            description=command.help or "No description available.",
            color=nextcord.Color.brand_green()
        )
        
        if command.aliases:
            embed.add_field(name="✨ Aliases", value=", ".join(command.aliases), inline=False)
        
        usage = f"!{command.name}"
        if command.signature:
            usage += f" {command.signature}"
        embed.add_field(name="🛠️ Usage", value=f"`{usage}`", inline=False)

        embed.set_footer(text="Remember: Practice makes perfect! Don't hesitate to experiment with commands.")

        await ctx.send(embed=embed)

    def get_category_emoji(self, category_name):
        emoji_map = {
            "General": "🌟",
            "Moderation": "🛡️",
            "Fun": "🎉",
            "Utility": "🔧",
            "Google Cloud": "☁️",
            "Android": "📱",
            "Web": "🌐",
            "AI/ML": "🤖",
            "Events": "📅",
            # Add more categories and emojis as needed
        }
        return emoji_map.get(category_name, "📌")

def setup(bot):
    bot.remove_command('help')  # Remove the default help command
    bot.add_cog(CustomHelp(bot))