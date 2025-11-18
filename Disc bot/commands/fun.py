from nextcord.ext import commands
import nextcord
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball', aliases=['8b', 'magic8ball'], help='Ask the magic 8-ball a question.')
    async def eight_ball(self, ctx, *, question: str = None):
        if question is None:
            await ctx.send("❌ Please ask a question!")
            return
        
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        
        embed = nextcord.Embed(
            title="🎱 Magic 8-Ball",
            color=nextcord.Color.blue()
        )
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=random.choice(responses), inline=False)
        embed.set_footer(text=f"Asked by {ctx.author.name}")
        
        await ctx.send(embed=embed)

    @commands.command(name='coinflip', aliases=['flip', 'coin'], help='Flips a coin.')
    async def coinflip(self, ctx):
        result = random.choice(["Heads", "Tails"])
        embed = nextcord.Embed(
            title="🪙 Coin Flip",
            description=f"The coin landed on **{result}**!",
            color=nextcord.Color.gold()
        )
        await ctx.send(embed=embed)

    @commands.command(name='roll', aliases=['dice'], help='Rolls a dice. Usage: !roll [sides] (default: 6)')
    async def roll(self, ctx, sides: int = 6):
        if sides < 2:
            await ctx.send("❌ Dice must have at least 2 sides.")
            return
        
        if sides > 100:
            await ctx.send("❌ Dice cannot have more than 100 sides.")
            return
        
        result = random.randint(1, sides)
        embed = nextcord.Embed(
            title="🎲 Dice Roll",
            description=f"You rolled a **{result}** on a {sides}-sided die!",
            color=nextcord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.command(name='choose', aliases=['pick'], help='Chooses randomly from given options. Usage: !choose option1 | option2 | option3')
    async def choose(self, ctx, *, choices: str):
        if '|' not in choices:
            await ctx.send("❌ Please separate options with `|`. Example: `!choose pizza | burger | pasta`")
            return
        
        options = [opt.strip() for opt in choices.split('|') if opt.strip()]
        
        if len(options) < 2:
            await ctx.send("❌ Please provide at least 2 options.")
            return
        
        chosen = random.choice(options)
        embed = nextcord.Embed(
            title="🎯 Random Choice",
            description=f"I choose: **{chosen}**",
            color=nextcord.Color.green()
        )
        embed.add_field(name="Options", value="\n".join([f"• {opt}" for opt in options]), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='poll', help='Creates a simple poll. Usage: !poll "Question" | option1 | option2')
    async def poll(self, ctx, *, poll_text: str):
        if '|' not in poll_text:
            await ctx.send("❌ Please format: `!poll \"Question\" | option1 | option2`")
            return
        
        parts = [part.strip() for part in poll_text.split('|')]
        question = parts[0].strip('"\'')
        options = parts[1:]
        
        if len(options) < 2:
            await ctx.send("❌ Please provide at least 2 options.")
            return
        
        if len(options) > 10:
            await ctx.send("❌ Maximum 10 options allowed.")
            return
        
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        embed = nextcord.Embed(
            title=f"📊 Poll: {question}",
            description="React with the number to vote!",
            color=nextcord.Color.blue()
        )
        
        options_text = "\n".join([f"{reactions[i]} {option}" for i, option in enumerate(options)])
        embed.add_field(name="Options", value=options_text, inline=False)
        embed.set_footer(text=f"Poll by {ctx.author.name}")
        
        message = await ctx.send(embed=embed)
        
        # Add reactions
        for i in range(len(options)):
            await message.add_reaction(reactions[i])

def setup(bot):
    bot.add_cog(Fun(bot))

