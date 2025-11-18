import nextcord
from nextcord.ext import commands

class Relay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.community_manager_id = 512996440486969345
        self.target_channel_id = 1423908362810167308

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from bots
        if message.author.bot:
            return
        
        # Ignore DMs
        if not message.guild:
            return
        
        # Debug: Log all messages from the CM
        if message.author.id == self.community_manager_id:
            print(f"[RELAY DEBUG] Message from CM in server: {message.guild.name} (ID: {message.guild.id}), channel: {message.channel.name} (ID: {message.channel.id})")
        
        # Check if message is from the community manager
        if message.author.id != self.community_manager_id:
            return
        
        # Get target channel (in private CM server)
        target_channel = self.bot.get_channel(self.target_channel_id)
        if not target_channel:
            print(f"[RELAY ERROR] Target channel with ID {self.target_channel_id} not found!")
            return
        
        print(f"[RELAY DEBUG] Target channel found: {target_channel.name} in server: {target_channel.guild.name} (ID: {target_channel.guild.id})")
        
        # Only relay if message is from a DIFFERENT server than the private CM server
        # (Don't relay messages that are already in the private CM server)
        if message.guild.id == target_channel.guild.id:
            # Message is already in the private CM server - don't relay
            print(f"[RELAY DEBUG] Message is in same server as target - skipping relay")
            return
        
        print(f"[RELAY DEBUG] Relaying message from {message.guild.name} to {target_channel.guild.name}")
        
        # Check if message contains "announcement" keyword (case-insensitive)
        message_content = message.content if message.content else ""
        is_announcement = "announcement" in message_content.lower()
        
        try:
            if is_announcement:
                # Format as embed for announcements
                embed = nextcord.Embed(
                    title="📢 Message from Community Manager",
                    description=message_content if message_content else "*No text content*",
                    color=nextcord.Color.blue()
                )
                
                # Add attachments if any
                if message.attachments:
                    attachment_list = []
                    for attachment in message.attachments:
                        attachment_list.append(f"[{attachment.filename}]({attachment.url})")
                    embed.add_field(
                        name="Attachments",
                        value="\n".join(attachment_list),
                        inline=False
                    )
                    # Set image if first attachment is an image
                    if message.attachments[0].content_type and message.attachments[0].content_type.startswith('image/'):
                        embed.set_image(url=message.attachments[0].url)
                
                # Add embeds if any
                if message.embeds:
                    embed.add_field(
                        name="Note",
                        value="Original message contained embeds (see above)",
                        inline=False
                    )
                
                await target_channel.send(embed=embed)
            else:
                # Default: Send as plain text (not formatted)
                content_to_send = message_content if message_content else "*No text content*"
                
                # Add attachments as links if any
                if message.attachments:
                    attachment_links = []
                    for attachment in message.attachments:
                        attachment_links.append(f"{attachment.filename}: {attachment.url}")
                    if attachment_links:
                        content_to_send += "\n\n" + "\n".join(attachment_links)
                
                await target_channel.send(content_to_send)
            
            print(f"[RELAY SUCCESS] Relayed message from {message.author.name} in {message.guild.name} to channel {target_channel.name} in {target_channel.guild.name}")
        except nextcord.Forbidden:
            print(f"[RELAY ERROR] No permission to send messages to channel {self.target_channel_id}")
        except Exception as e:
            print(f"[RELAY ERROR] Error relaying message: {e}")
            import traceback
            traceback.print_exc()

def setup(bot):
    bot.add_cog(Relay(bot))

