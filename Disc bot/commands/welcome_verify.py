import nextcord
from nextcord.ext import commands
from nextcord import Embed, Color, File
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import random
import string

class WelcomeVerify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verification_codes = {}
        self.welcome_channel_id = 1288646513051832350
        self.verified_role_id = 1288647613905764362

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Create and send the welcome card
        card = await self.create_welcome_card(member)
        welcome_channel = self.bot.get_channel(self.welcome_channel_id)
        await welcome_channel.send(f"Welcome to GDGC Binus International, {member.mention}!", file=card)
        
        # Send verification instructions
        verification_code = self.generate_verification_code()
        self.verification_codes[member.id] = verification_code
        await self.send_verification_dm(member, verification_code)

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
        title_font = ImageFont.truetype("Disc bot/Assets/Montserrat-Bold.ttf", 60)
        subtitle_font = ImageFont.truetype("Disc bot/Assets/Montserrat-Italic-VariableFont_wght.ttf", 40)

        # Add text to the card
        draw.text((50, 50), f"Welcome, {member.name}!", fill=text_color, font=title_font)
        draw.text((50, 120), "to GDGC Binus International", fill=text_color, font=subtitle_font)

        # Add GDGC logo
        logo = Image.open("Disc bot/Assets/images.png").convert("RGBA")
        logo = logo.resize((100, 100))
        card.paste(logo, (card_width - 150, 50), logo)

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

    def generate_verification_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    async def send_verification_dm(self, member, code):
        embed = Embed(
            title="Welcome to GDGC Binus International!",
            description="Please verify your account to access the server.",
            color=Color.blue()
        )
        embed.add_field(
            name="Verification Code",
            value=f"`!verify {code}`",
            inline=False
        )
        embed.add_field(
            name="Instructions",
            value="Use the command above in any channel to verify your account.",
            inline=False
        )
        embed.add_field(
            name="Expiration",
            value="This code will expire in 24 hours.",
            inline=False
        )
        embed.add_field(
            name="Important Note",
            value="By verifying, you confirm that you have read, understood, and agree to adhere to the server rules and terms. If you do not agree, please do not verify your account.",
            inline=False
        )
        embed.set_footer(text="GDGC Binus International")

        try:
            await member.send(embed=embed)
        except nextcord.Forbidden:
            welcome_channel = self.bot.get_channel(self.welcome_channel_id)
            if welcome_channel:
                error_embed = Embed(
                    title="DM Delivery Failed",
                    description=f"{member.mention}, I couldn't send you a direct message.",
                    color=Color.red()
                )
                error_embed.add_field(
                    name="Action Required",
                    value="Please enable DMs from server members to receive your verification code.",
                    inline=False
                )
                await welcome_channel.send(embed=error_embed)
            else:
                print(f"Error: Welcome channel with ID {self.welcome_channel_id} not found.")

    @commands.command()
    async def verify(self, ctx, code: str):
        if ctx.author.id in self.verification_codes:
            if code == self.verification_codes[ctx.author.id]:
                verified_role = ctx.guild.get_role(self.verified_role_id)
                await ctx.author.add_roles(verified_role)
                del self.verification_codes[ctx.author.id]
                await ctx.send(f"Congratulations, {ctx.author.mention}! You've been verified. Welcome to GDGC Binus International!")
            else:
                await ctx.send("Invalid verification code. Please try again.")
        else:
            await ctx.send("You don't have a pending verification. If you need a new code, please contact an admin.")

def setup(bot):
    bot.add_cog(WelcomeVerify(bot))