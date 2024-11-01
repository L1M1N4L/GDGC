import nextcord
from nextcord.ext import commands
import json
from datetime import datetime, timedelta
from pathlib import Path

class TeamBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.teams = {}  # {team_name: {"captain": id, "members": [ids]}}
        self.invites = {}  # {team_name: {"user_id": expire_time}}
        self.load_data()

    def load_data(self):
        try:
            with open('teams.json', 'r') as f:
                self.teams = json.load(f)
        except FileNotFoundError:
            self.teams = {}
            
        try:
            with open('invites.json', 'r') as f:
                invite_data = json.load(f)
                # Convert stored string times back to datetime objects
                self.invites = {
                    team: {
                        user: datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                        for user, time in invites.items()
                    }
                    for team, invites in invite_data.items()
                }
        except FileNotFoundError:
            self.invites = {}

    def save_data(self):
        with open('teams.json', 'w') as f:
            json.dump(self.teams, f, indent=4)
            
        # Convert datetime objects to strings for JSON storage
        invite_data = {
            team: {
                user: time.strftime("%Y-%m-%d %H:%M:%S")
                for user, time in invites.items()
            }
            for team, invites in self.invites.items()
        }
        with open('invites.json', 'w') as f:
            json.dump(invite_data, f, indent=4)

    def get_player_team(self, player_id):
        for team_name, team_data in self.teams.items():
            if player_id in team_data["members"]:
                return team_name
        return None

    @commands.command()
    async def register(self, ctx, *, team_name: str):
        """Register a new team"""
        if team_name in self.teams:
            embed = nextcord.Embed(
                title="❌ Registration Failed",
                description="This team name is already taken!",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        member_id = str(ctx.author.id)
        if self.get_player_team(member_id):
            embed = nextcord.Embed(
                title="❌ Registration Failed",
                description="You are already in a team!",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        self.teams[team_name] = {
            "captain": member_id,
            "members": [member_id]
        }
        self.save_data()

        embed = nextcord.Embed(
            title="✅ Team Created",
            description=f"Team **{team_name}** has been created!",
            color=nextcord.Color.green()
        )
        embed.add_field(name="Captain", value=ctx.author.mention)
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx, member: nextcord.Member):
        """Invite a player to your team"""
        captain_id = str(ctx.author.id)
        team_name = self.get_player_team(captain_id)

        if not team_name:
            embed = nextcord.Embed(
                title="❌ Invite Failed",
                description="You are not in any team!",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if self.teams[team_name]["captain"] != captain_id:
            embed = nextcord.Embed(
                title="❌ Invite Failed",
                description="Only the team captain can invite new members!",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        member_id = str(member.id)
        if self.get_player_team(member_id):
            embed = nextcord.Embed(
                title="❌ Invite Failed",
                description="This player is already in a team!",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Create invite that expires in 24 hours
        if team_name not in self.invites:
            self.invites[team_name] = {}
        self.invites[team_name][member_id] = datetime.utcnow() + timedelta(hours=24)
        self.save_data()

        embed = nextcord.Embed(
            title="🎮 Team Invitation",
            description=f"You have been invited to join team **{team_name}**!\nUse `!accept {team_name}` to accept or `!decline {team_name}` to decline.",
            color=nextcord.Color.blue()
        )
        await member.send(embed=embed)

        embed = nextcord.Embed(
            title="✅ Invite Sent",
            description=f"Invitation sent to {member.mention}!",
            color=nextcord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def accept(self, ctx, team_name: str):
        """Accept a team invitation"""
        member_id = str(ctx.author.id)
        
        if self.get_player_team(member_id):
            embed = nextcord.Embed(
                title="❌ Accept Failed",
                description="You are already in a team!",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if team_name not in self.invites or member_id not in self.invites[team_name]:
            embed = nextcord.Embed(
                title="❌ Accept Failed",
                description="You don't have an invitation from this team!",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if datetime.utcnow() > self.invites[team_name][member_id]:
            del self.invites[team_name][member_id]
            self.save_data()
            embed = nextcord.Embed(
                title="❌ Accept Failed",
                description="This invitation has expired!",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        self.teams[team_name]["members"].append(member_id)
        del self.invites[team_name][member_id]
        self.save_data()

        embed = nextcord.Embed(
            title="✅ Team Joined",
            description=f"You have joined team **{team_name}**!",
            color=nextcord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def decline(self, ctx, team_name: str):
        """Decline a team invitation"""
        member_id = str(ctx.author.id)
        
        if team_name not in self.invites or member_id not in self.invites[team_name]:
            embed = nextcord.Embed(
                title="❌ Decline Failed",
                description="You don't have an invitation from this team!",
                color=nextcord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        del self.invites[team_name][member_id]
        self.save_data()

        embed = nextcord.Embed(
            title="✅ Invite Declined",
            description=f"You have declined the invitation to team **{team_name}**!",
            color=nextcord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name="teams")
    async def list_teams(self, ctx):
        """List all teams"""
        if not self.teams:
            embed = nextcord.Embed(
                title="📋 Team List",
                description="No teams have been registered yet!",
                color=nextcord.Color.blue()
            )
            await ctx.send(embed=embed)
            return

        embed = nextcord.Embed(
            title="📋 Team List",
            color=nextcord.Color.blue()
        )
        
        for team_name, team_data in self.teams.items():
            captain = await self.bot.fetch_user(int(team_data["captain"]))
            members = len(team_data["members"])
            value = f"Captain: {captain.name}\nMembers: {members}"
            embed.add_field(name=team_name, value=value, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='teamhelp')  # Change the command name to 'teamhelp'
    async def team_help_command(self, ctx):
        """Display help information about the team commands."""
        embed = nextcord.Embed(
            title="🆘 Team Help Command",
            description="Here are the available commands for managing teams:",
            color=nextcord.Color.blue()
        )
        
        embed.add_field(
            name="!register <team_name>",
            value="Create a new team with the specified name. You must not be in a team already.",
            inline=False
        )
        embed.add_field(
            name="!invite <@member>",
            value="Invite a member to your team. Only the team captain can use this command.",
            inline=False
        )
        embed.add_field(
            name="!accept <team_name>",
            value="Accept an invitation to join the specified team.",
            inline=False
        )
        embed.add_field(
            name="!decline <team_name>",
            value="Decline an invitation to join the specified team.",
            inline=False
        )
        embed.add_field(
            name="!teams",
            value="List all registered teams and their members.",
            inline=False
        )
        embed.add_field(
            name="disband",
            value="please contact jonathan to disband your current team",
            inline=False
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(TeamBot(bot))