# How to Enable Message Content Intent

## Why This is Needed
Your bot uses prefix commands (like `!ping`, `!help`). To read these commands, the bot needs the `MESSAGE_CONTENT` intent, which is a privileged gateway intent.

## Steps to Enable:

1. **Go to Discord Developer Portal**
   - Visit: https://discord.com/developers/applications/
   - Log in with your Discord account

2. **Select Your Bot Application**
   - Click on your bot's application

3. **Go to Bot Settings**
   - Click "Bot" in the left sidebar

4. **Enable Message Content Intent**
   - Scroll down to "Privileged Gateway Intents"
   - Toggle ON "MESSAGE CONTENT INTENT"
   - Click "Save Changes"

5. **Restart Your Bot**
   - Stop your bot (Ctrl+C)
   - Run it again: `python "Disc bot/bot.py"`

## Important Notes:
- This intent is required for prefix commands to work
- It's a privileged intent but doesn't require bot verification for bots in <100 servers
- Your bot will now be able to read message content and respond to commands

