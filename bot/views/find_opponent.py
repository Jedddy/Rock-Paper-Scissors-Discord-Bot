import discord
from views.battle import Battle
from utils.embed_helper import vs_embed

class FindOpponent(discord.ui.View):
    def __init__(self, p1: discord.Member, timeout):
        super().__init__(timeout=timeout)
        self.p1 = p1

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def opponent_accepted(self, interaction: discord.Interaction, button: discord.Button):
        opponent = interaction.user
        battle_view = Battle(interaction, (self.p1, opponent))
        embed, file = await vs_embed(self.p1, opponent)
        await interaction.response.edit_message(embed=embed, view=battle_view, attachments=[file])

    async def interaction_check(self, interaction: discord.Interaction):
        if self.p1 == interaction.user:
            await interaction.response.send_message("Hey! You can't duel yourself!", ephemeral=True)
            return False
        return True