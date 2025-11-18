from nextcord.ext import commands
import nextcord
from datetime import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear', aliases=['purge', 'delete'], help='Deletes a specified number of messages. (Requires Manage Messages permission)', hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        if amount < 1:
            await ctx.send("❌ Please specify a number greater than 0.")
            return
        
        if amount > 100:
            await ctx.send("❌ You can only delete up to 100 messages at once.")
            return
        
        try:
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
            embed = nextcord.Embed(
                title="✅ Messages Deleted",
                description=f"Successfully deleted {len(deleted) - 1} message(s).",
                color=nextcord.Color.green()
            )
            msg = await ctx.send(embed=embed)
            # Delete the confirmation message after 3 seconds
            await msg.delete(delay=3)
        except nextcord.Forbidden:
            await ctx.send("❌ I don't have permission to delete messages in this channel.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {e}")

    @commands.command(name='kick', help='Kicks a member from the server. (Requires Kick Members permission)', hidden=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member, *, reason: str = "No reason provided"):
        if member == ctx.author:
            await ctx.send("❌ You cannot kick yourself.")
            return
        
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send("❌ You cannot kick someone with equal or higher roles.")
            return
        
        try:
            await member.kick(reason=f"Kicked by {ctx.author.name}: {reason}")
            embed = nextcord.Embed(
                title="✅ Member Kicked",
                description=f"{member.mention} has been kicked from the server.",
                color=nextcord.Color.orange()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"Kicked by {ctx.author.name}")
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
        except nextcord.Forbidden:
            await ctx.send("❌ I don't have permission to kick this member.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {e}")

    @commands.command(name='ban', help='Bans a member from the server. (Requires Ban Members permission)', hidden=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member, *, reason: str = "No reason provided"):
        if member == ctx.author:
            await ctx.send("❌ You cannot ban yourself.")
            return
        
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send("❌ You cannot ban someone with equal or higher roles.")
            return
        
        try:
            await member.ban(reason=f"Banned by {ctx.author.name}: {reason}")
            embed = nextcord.Embed(
                title="✅ Member Banned",
                description=f"{member.mention} has been banned from the server.",
                color=nextcord.Color.red()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"Banned by {ctx.author.name}")
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
        except nextcord.Forbidden:
            await ctx.send("❌ I don't have permission to ban this member.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {e}")

    @commands.command(name='unban', help='Unbans a user from the server. (Requires Ban Members permission)', hidden=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason: str = "No reason provided"):
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=f"Unbanned by {ctx.author.name}: {reason}")
            embed = nextcord.Embed(
                title="✅ User Unbanned",
                description=f"{user.name}#{user.discriminator} has been unbanned from the server.",
                color=nextcord.Color.green()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"Unbanned by {ctx.author.name}")
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
        except nextcord.NotFound:
            await ctx.send("❌ User not found or not banned.")
        except nextcord.Forbidden:
            await ctx.send("❌ I don't have permission to unban this user.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {e}")

def setup(bot):
    bot.add_cog(Moderation(bot))

