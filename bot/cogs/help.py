import discord
from discord.ext import commands
from discord import app_commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name="help", description="Displays all the bot commands available.")
    async def help(self, interaction: discord.Interaction):
        helps_list = (
            "`/find_challenger`\n\tFind a challenger!",
            "`/duel`\n\tDuel a chosen opponent!",
            "`/leadearboards`\n\tView Top 10 players in the server",
        )
        embed = discord.Embed(
            title="Commands for Rock, Paper, Scissors!",
            description="Some fun commands!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Fun", value="\n\n".join(helps_list))
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
