from nextcord.ext import commands
import nextcord
import platform
import sys
from datetime import datetime

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='botinfo', help='Shows information about the bot.')
    async def botinfo(self, ctx):
        embed = nextcord.Embed(
            title="🤖 Bot Information",
            color=nextcord.Color.blue()
        )
        
        # Bot basic info
        embed.add_field(
            name="Bot Name",
            value=f"{self.bot.user.name}",
            inline=True
        )
        embed.add_field(
            name="Bot ID",
            value=f"{self.bot.user.id}",
            inline=True
        )
        embed.add_field(
            name="Server Count",
            value=f"{len(self.bot.guilds)}",
            inline=True
        )
        
        # Technical info
        embed.add_field(
            name="Python Version",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Nextcord Version",
            value=f"{nextcord.__version__}",
            inline=True
        )
        embed.add_field(
            name="Command Prefix",
            value="`!`",
            inline=True
        )
        
        # Uptime (approximate)
        embed.add_field(
            name="Latency",
            value=f"{self.bot.latency * 1000:.2f} ms",
            inline=True
        )
        
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text="GDGC Binus International Bot")
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)

    @commands.command(name='gdg', aliases=['gdginfo', 'about'], help='Shows information about GDG on Campus Binus University International.')
    async def gdg_info(self, ctx):
        embed = nextcord.Embed(
            title="🚀 GDG on Campus Binus University International",
            description="Welcome to Google Developer Student Club @ Binus University International!",
            color=nextcord.Color.brand_green()
        )
        
        embed.add_field(
            name="📍 Location",
            value="Binus International Campus at FX Sudirman 6th floor\nJl. Jendral Sudirman, Jakarta Pusat, 10270",
            inline=False
        )
        
        embed.add_field(
            name="📧 Contact",
            value="dscbinusinter@gmail.com",
            inline=True
        )
        
        embed.add_field(
            name="🌐 Official Link",
            value="[Visit our GDG Community Page](https://gdg.community.dev/gdg-on-campus-binus-university-international-jakarta-indonesia/)",
            inline=False
        )
        
        embed.add_field(
            name="💬 About Us",
            value=(
                "We are a university-based community group interested in technology "
                "and Google Developer technologies. We explore all kinds of technology "
                "and are excited to embark on this journey in learning, connecting, "
                "and growing with technology. Giving back to our community is one of "
                "our key values and we would like to make an impact in our community."
            ),
            inline=False
        )
        
        embed.add_field(
            name="👥 Community",
            value="We welcome all attendees to join our events, regardless of background and experience!",
            inline=False
        )
        
        embed.set_footer(text="GDG on Campus Binus University International - Jakarta, Indonesia")
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo', aliases=['server', 'guildinfo'], help='Shows information about the server.')
    async def serverinfo(self, ctx):
        guild = ctx.guild
        
        embed = nextcord.Embed(
            title=f"📊 {guild.name}",
            color=nextcord.Color.green()
        )
        
        # Server basic info
        embed.add_field(
            name="Server ID",
            value=f"{guild.id}",
            inline=True
        )
        embed.add_field(
            name="Owner",
            value=f"{guild.owner.mention if guild.owner else 'Unknown'}",
            inline=True
        )
        embed.add_field(
            name="Created",
            value=f"<t:{int(guild.created_at.timestamp())}:R>",
            inline=True
        )
        
        # Member counts
        embed.add_field(
            name="Members",
            value=f"{guild.member_count}",
            inline=True
        )
        embed.add_field(
            name="Channels",
            value=f"{len(guild.channels)}",
            inline=True
        )
        embed.add_field(
            name="Roles",
            value=f"{len(guild.roles)}",
            inline=True
        )
        
        # Boosts
        if guild.premium_subscription_count > 0:
            embed.add_field(
                name="Boost Level",
                value=f"Level {guild.premium_tier}",
                inline=True
            )
            embed.add_field(
                name="Boosts",
                value=f"{guild.premium_subscription_count}",
                inline=True
            )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.set_footer(text=f"Server ID: {guild.id}")
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)

    @commands.command(name='userinfo', aliases=['user', 'whois'], help='Shows information about a user.')
    async def userinfo(self, ctx, member: nextcord.Member = None):
        if member is None:
            member = ctx.author
        
        embed = nextcord.Embed(
            title=f"👤 {member.display_name}",
            color=member.color if member.color != nextcord.Color.default() else nextcord.Color.blue()
        )
        
        # User basic info
        embed.add_field(
            name="Username",
            value=f"{member.name}#{member.discriminator}",
            inline=True
        )
        embed.add_field(
            name="User ID",
            value=f"{member.id}",
            inline=True
        )
        embed.add_field(
            name="Nickname",
            value=f"{member.display_name}",
            inline=True
        )
        
        # Account info
        embed.add_field(
            name="Account Created",
            value=f"<t:{int(member.created_at.timestamp())}:R>",
            inline=True
        )
        embed.add_field(
            name="Joined Server",
            value=f"<t:{int(member.joined_at.timestamp())}:R>" if member.joined_at else "Unknown",
            inline=True
        )
        
        # Roles
        roles = [role.mention for role in member.roles[1:]]  # Exclude @everyone
        roles_str = ", ".join(roles[:10]) if roles else "No roles"
        if len(roles) > 10:
            roles_str += f" (+{len(roles) - 10} more)"
        
        embed.add_field(
            name=f"Roles ({len(member.roles) - 1})",
            value=roles_str if roles_str else "No roles",
            inline=False
        )
        
        # Status
        if member.status:
            status_emoji = {
                "online": "🟢",
                "idle": "🟡",
                "dnd": "🔴",
                "offline": "⚫"
            }
            embed.add_field(
                name="Status",
                value=f"{status_emoji.get(str(member.status), '⚫')} {str(member.status).title()}",
                inline=True
            )
        
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)

    @commands.command(name='avatar', aliases=['av', 'pfp'], help='Shows a user\'s avatar.')
    async def avatar(self, ctx, member: nextcord.Member = None):
        if member is None:
            member = ctx.author
        
        embed = nextcord.Embed(
            title=f"{member.display_name}'s Avatar",
            color=member.color if member.color != nextcord.Color.default() else nextcord.Color.blue()
        )
        
        if member.avatar:
            embed.set_image(url=member.avatar.url)
            embed.add_field(
                name="Download",
                value=f"[Click here]({member.avatar.url})",
                inline=False
            )
        else:
            embed.description = "This user has no avatar."
        
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
