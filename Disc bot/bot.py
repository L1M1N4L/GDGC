import nextcord
from nextcord.ext import commands
import os

# Set the command prefix and intents
intents = nextcord.Intents.all()
intents.members = True  # Ensure member intents are enabled
bot = commands.Bot(command_prefix='!', intents=intents)

# Load extensions
initial_extensions = [
    'commands.ping',
    'commands.info',
    'commands.help',
    'commands.welcome_verify',
    'commands.rule',  # Add the new rule cog
    'commands.minecraft_team',
]


# Constants for the welcome and verify system
WELCOME_CHANNEL_ID = 1288646513051832350  # Replace with your actual channel ID
VERIFIED_ROLE_ID = 1288647613905764362  # Replace with your actual role ID


if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    # Set up the welcome channel and roles
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not welcome_channel:
        print(f"Warning: Welcome channel with ID {WELCOME_CHANNEL_ID} not found!")
    
    verified_role = bot.guilds[0].get_role(VERIFIED_ROLE_ID)
    if not verified_role:
        print(f"Warning: Verified role with ID {VERIFIED_ROLE_ID} not found!")
    
    print("Bot is ready!")

# Run the bot
bot.run('TOKEN')
