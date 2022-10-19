import discord
from views.find_opponent import FindOpponent
from views.rps import RPS
from database.db import check_leaderboards
from discord import app_commands
from discord.ext import commands


class Game(commands.Cog):
    """Game Cog"""
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="find_challenger", description="Find a challenger")
    @app_commands.describe(timeout="Timeout before the view expires.")
    async def find_challenger(self, interaction: discord.Interaction, timeout: int = 30):
        embed = discord.Embed(
            title=f"{interaction.user} is looking for an opponent!",
            description="Press accept to accept duel.",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Will timeouut after {timeout} seconds.")
        p1 = interaction.user
        find_opponent_view = FindOpponent(p1, timeout=timeout)
        await interaction.response.send_message(embed=embed, view=find_opponent_view)

    @app_commands.command(name="duel", description="Duel with another player")
    @app_commands.describe(member="The chosen opponent", timeout="Timeout before the view expires.")
    async def duel(self, interaction: discord.Interaction, member: discord.Member, timeout: int = 30):
        challenge_view = RPS(interaction, member, timeout)
        duel_embed = discord.Embed(
                    description=f"{member.mention}!, {interaction.user.mention} challenged you into a duel!",
                    color=discord.Color.blue()
                    )
        duel_embed.set_footer(text=f"Will timeout after {timeout} seconds.")
        if member.bot:
            await interaction.response.send_message("You cannot duel a bot!", ephemeral=True)
        elif member.id != interaction.user.id: # Gets triggered if the mentioned opponent accepts the duel
            await interaction.response.send_message(
                embed=duel_embed,
                view=challenge_view)
        elif member.id == interaction.user.id:
            await interaction.response.send_message("You cannot duel yourself!", ephemeral=True)
        else:
            await interaction.response.send_message("An error has occured", ephemeral=True)

    @app_commands.command(name="leaderboards", description="View Top 10 Rock Paper, Scissors players.")
    async def leaderboard(self, interaction: discord.Interaction):
        desc = ""
        leaderboards = await check_leaderboards(server_id=interaction.guild_id) # Returns a list of tuples [(username, wins)]
        if not leaderboards:
            embed = discord.Embed(
                color=discord.Color.blue(),
                title="No players yet..."
            )
        else:
            for rank, name in enumerate(leaderboards, start=1):
                desc += f"**{rank}**. {name[0]} `[{name[1]}] wins\n`"
            embed = discord.Embed( 
            color=discord.Color.blue(),
            title=f"Top 10 Rock, Paper, Scissors players in {interaction.guild}",
            description=desc
            )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Game(bot))
