import nextcord
from nextcord.ext import commands
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the command prefix and intents
# Note: message_content is required for prefix commands (!ping, !help, etc.)
# members intent is required for welcome messages (on_member_join event)
# These must be enabled in Discord Developer Portal
intents = nextcord.Intents.default()
intents.message_content = True  # Required for reading message content
intents.members = True  # Required for welcome messages
bot = commands.Bot(command_prefix='!', intents=intents)

# Constants for the welcome system
WELCOME_CHANNEL_ID = 1440172462322221159  # Welcome channel ID

# Load extensions
initial_extensions = [
    'commands.ping',
    'commands.info',
    'commands.help',
    'commands.welcome_verify',
    'commands.rule',
    'commands.moderation',
    'commands.fun',
    'commands.relay',
    'commands.leetcode',
]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Connected to {len(bot.guilds)} guild(s)')
    print(f'Message Content Intent: {bot.intents.message_content}')
    print(f'Loaded Commands: {[cmd.name for cmd in bot.commands]}')
    
    # Set up the welcome channel
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not welcome_channel:
        print(f"Warning: Welcome channel with ID {WELCOME_CHANNEL_ID} not found!")
    
    if not bot.intents.message_content:
        print("⚠️ WARNING: Message Content Intent is NOT enabled!")
        print("⚠️ The bot will NOT be able to read messages or respond to commands!")
        print("⚠️ Please enable MESSAGE CONTENT INTENT in Discord Developer Portal")
    
    if not bot.intents.members:
        print("⚠️ WARNING: Members Intent is NOT enabled!")
        print("⚠️ Welcome messages will NOT work!")
        print("⚠️ Please enable MEMBERS INTENT in Discord Developer Portal")
    else:
        print("✓ Members Intent enabled - Welcome messages are active!")
    
    # Check relay system
    relay_channel = bot.get_channel(1423908362810167308)
    if relay_channel:
        print(f"✓ Relay system active - Target channel: {relay_channel.name} in {relay_channel.guild.name}")
    else:
        print("⚠️ WARNING: Relay target channel not found! Bot may not be in the private CM server.")
    
    print("Bot is ready!")


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors gracefully"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore command not found errors
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param.name}")
    else:
        print(f"An error occurred: {error}")
        await ctx.send("❌ An error occurred while executing the command.")


if __name__ == '__main__':
    # Load extensions with error handling
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f'✓ Loaded extension: {extension}')
        except Exception as e:
            print(f'✗ Failed to load extension {extension}: {e}')
    
    # Get bot token from .env file or environment variable
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("Error: DISCORD_BOT_TOKEN not found!")
        print("Please create a .env file in the 'Disc bot' folder with:")
        print("DISCORD_BOT_TOKEN=your_token_here")
        sys.exit(1)
    
    # Run the bot
    try:
        bot.run(token)
    except nextcord.LoginFailure:
        print("Error: Invalid bot token!")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting bot: {e}")
        sys.exit(1)
