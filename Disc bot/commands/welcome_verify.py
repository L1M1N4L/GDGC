import nextcord
from nextcord.ext import commands
from nextcord import File
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os

class WelcomeVerify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = 1440172462322221159
        # Get the base directory (parent of commands folder)
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Sends a welcome card when a new member joins"""
        try:
            # Create and send the welcome card
            card = await self.create_welcome_card(member)
            welcome_channel = self.bot.get_channel(self.welcome_channel_id)
            if welcome_channel:
                await welcome_channel.send(f"Welcome to GDGoC Binus International, {member.mention}!", file=card)
            else:
                print(f"Warning: Welcome channel with ID {self.welcome_channel_id} not found!")
        except Exception as e:
            print(f"Error sending welcome card: {e}")
            # Try to send a simple welcome message if card creation fails
            welcome_channel = self.bot.get_channel(self.welcome_channel_id)
            if welcome_channel:
                try:
                    await welcome_channel.send(f"Welcome to GDGoC Binus International, {member.mention}! 🎉")
                except:
                    pass

    async def create_welcome_card(self, member):
        # Card dimensions and colors
        card_width, card_height = 1000, 370
        background_color = (240, 240, 240)
        text_color = (33, 33, 33)
        accent_color = (66, 133, 244)  # Google Blue

        # Create a new image with a light gray background
        card = Image.new('RGB', (card_width, card_height), color=background_color)
        draw = ImageDraw.Draw(card)

        # Load fonts
        bold_font_path = os.path.join(self.base_dir, "Assets", "Montserrat-Bold.ttf")
        italic_font_path = os.path.join(self.base_dir, "Assets", "Montserrat-Italic-VariableFont_wght.ttf")
        try:
            title_font = ImageFont.truetype(bold_font_path, 60)
            subtitle_font = ImageFont.truetype(italic_font_path, 40)
        except (OSError, IOError) as e:
            print(f"Warning: Could not load fonts: {e}")
            # Fallback to default font
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

        # Add text to the card
        draw.text((50, 50), f"Welcome, {member.name}!", fill=text_color, font=title_font)
        draw.text((50, 120), "to GDGC Binus International", fill=text_color, font=subtitle_font)

        # Add GDGC logo
        logo_path = os.path.join(self.base_dir, "Assets", "images.png")
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo = logo.resize((100, 100))
            card.paste(logo, (card_width - 150, 50), logo)
        except (OSError, IOError) as e:
            print(f"Warning: Could not load logo: {e}")

        # Add member avatar
        avatar_size = 128
        avatar_asset = member.avatar.with_size(128)
        avatar_data = io.BytesIO(await avatar_asset.read())
        avatar = Image.open(avatar_data).convert("RGBA")
        avatar = avatar.resize((avatar_size, avatar_size))
        
        # Create circular mask for avatar
        mask = Image.new('L', (avatar_size, avatar_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
        
        # Apply circular mask to avatar
        output = Image.new('RGBA', (avatar_size, avatar_size), (0, 0, 0, 0))
        output.paste(avatar, (0, 0), mask)
        
        # Add a subtle shadow to the avatar
        shadow = Image.new('RGBA', (avatar_size + 6, avatar_size + 6), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.ellipse((3, 3, avatar_size + 3, avatar_size + 3), fill=(0, 0, 0, 100))
        shadow = shadow.filter(ImageFilter.GaussianBlur(3))
        card.paste(shadow, (47, card_height - avatar_size - 53), shadow)
        
        # Paste the circular avatar onto the card
        card.paste(output, (50, card_height - avatar_size - 50), output)

        # Add a decorative element
        draw.rectangle([0, card_height - 10, card_width, card_height], fill=accent_color)

        # Save the card to a buffer
        buffer = io.BytesIO()
        card.save(buffer, format='PNG')
        buffer.seek(0)

        return File(buffer, filename='welcome_card.png')

def setup(bot):
    bot.add_cog(WelcomeVerify(bot))