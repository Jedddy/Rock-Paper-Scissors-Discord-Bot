import discord
import asyncio
from views.battle import Battle
from utils.embed_helper import vs_embed


class RPS(discord.ui.View):
    """Challenge view class"""
    def __init__(self, p1: discord.Interaction, p2: discord.Member, timeout: int):
        super().__init__(timeout=timeout if timeout else 30)
        self.p1 = p1
        self.p2 = p2

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.blurple)
    async def accept_button_callback(self, interaction: discord.Interaction, button: discord.Button):
        battle_view = Battle(self.p1, (self.p1.user, self.p2))
        embed, file = await vs_embed(self.p1.user, self.p2)    
        await interaction.response.edit_message(embed=embed,
                                                    view=battle_view, 
                                                    attachments=[file])
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline_button_callback(self, interaction: discord.Interaction, button: discord.Button):
        for buttons in self.children:
            buttons.disabled = True
        await interaction.response.edit_message(embed=discord.Embed(
            color=discord.Color.red(),
            description="Duel declined!",
        ), view=self)
        self.stop()
        await asyncio.sleep(10)
        await interaction.delete_original_response()
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.p2:
            await interaction.response.send_message("Hey! This is not your button to click!", ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        await self.p1.delete_original_response()