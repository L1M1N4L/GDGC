import nextcord
from nextcord.ext import commands
import os

class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Get the base directory (parent of commands folder)
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @commands.command(name='bothelp', aliases=['help', 'commands'], help='Displays the help message.')
    async def help_command(self, ctx):
        try:
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
            image_path = os.path.join(self.base_dir, "Assets", "images.png")
            file = None
            try:
                if os.path.exists(image_path):
                    file = nextcord.File(image_path, filename="images.png")
                    embed.set_thumbnail(url="attachment://images.png")
            except Exception as e:
                print(f"Warning: Could not load image: {e}")

            # Group commands by cog
            cog_commands = {}
            hidden_cogs = ["Moderation", "Rules"]  # Cogs to hide from help
            for command in self.bot.commands:
                if command.hidden:
                    continue  # Skip hidden commands
                cog_name = command.cog_name or "General"
                if cog_name in hidden_cogs:
                    continue  # Skip moderation and rules cogs
                if cog_name not in cog_commands:
                    cog_commands[cog_name] = []
                cog_commands[cog_name].append(command)

            # Add fields for each cog
            if cog_commands:
                for cog_name, commands in cog_commands.items():
                    emoji = self.get_category_emoji(cog_name)
                    command_list = "\n".join([f"`{cmd.name}` - {cmd.help or 'No description'}" for cmd in commands])
                    if command_list:  # Only add if there are commands
                        embed.add_field(name=f"{emoji} **{cog_name}**", value=command_list, inline=False)
            else:
                embed.add_field(name="⚠️ No Commands", value="No commands are currently available.", inline=False)

            # Add a footer
            embed.set_footer(text="💡 Tip: Use !commandinfo <command> for more details on a specific command.")

            # Send the embed WITH the file (if file exists)
            if file:
                await ctx.send(embed=embed, file=file)
            else:
                await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error in help command: {e}")
            await ctx.send("❌ An error occurred while displaying the help message. Please try again.")

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
        }
        return emoji_map.get(category_name, "📌")

def setup(bot):
    bot.remove_command('help')  
    bot.add_cog(CustomHelp(bot))
