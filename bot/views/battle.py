import discord
import random
from models.models import Rock, Paper, Scissors
from images.image_utils import vs_image, result_image
from database.db import add_wins


class Battle(discord.ui.View):
    """Battle View class"""
    style = discord.ButtonStyle.blurple

    def __init__(self, interaction: discord.Interaction, interactors: tuple[discord.Member, discord.Member]):
        super().__init__(timeout=30)
        self.interaction = interaction
        self.p1, self.p2 = str(interactors[0]), str(interactors[1])
        self.p1_pfp_url, self.p2_pfp_url = str(interactors[0].avatar), str(interactors[1].avatar)
        self.interactors = interactors
        self._ready = set()
        self.moves = {}

    @discord.ui.button(label="Rock!", style=style)
    async def rock(self, interaction: discord.Interaction, button: discord.Button):
        self.moves[str(interaction.user)] = Rock()
        await interaction.response.send_message("You picked Rock.", ephemeral=True)

    @discord.ui.button(label="Paper!", style=style)
    async def paper(self, interaction: discord.Interaction, button: discord.Button):
        self.moves[str(interaction.user)] = Paper()
        await interaction.response.send_message("You picked Paper.", ephemeral=True)

    @discord.ui.button(label="Scissors!", style=style)
    async def scissors(self, interaction: discord.Interaction, button: discord.Button):
        self.moves[str(interaction.user)] = Scissors()
        await interaction.response.send_message("You picked Scissors.", ephemeral=True)

    @discord.ui.button(label="Ready!", style=discord.ButtonStyle.green)
    async def ready(self, interaction: discord.Interaction, button: discord.Button):
        if (str(interaction.user) not in self.moves) and (interaction.user in self.interactors):
            rps_random = random.choice([Rock(), Paper(), Scissors()])
            self._ready.add(str(interaction.user))
            self.moves[str(interaction.user)] = rps_random
            await interaction.response.send_message(f"You did not choose a move, you will now get a random move.\nRandom chosen move: {rps_random}",
                                                    ephemeral=True)
        else:
            self._ready.add(str(interaction.user))
            await interaction.response.send_message("Choice saved!", ephemeral=True)
            
        if len(self._ready) == 2:
            for buttons in self.children:
                buttons.disabled = True
            self.stop()
            p1_move = self.moves[self.p1]
            p2_move = self.moves[self.p2]
            winner = await self.checker(p1=self.interactors[0], 
                                p2=self.interactors[1],
                                p1_move=p1_move, 
                                p2_move=p2_move)
            if not winner:
                await interaction.followup.send(embed=discord.Embed(
                    title="It's a draw!"
                ))
            else:
                bg = await vs_image(p1_image=self.p1_pfp_url, p2_image=self.p2_pfp_url)
                img = await result_image(image=bg,
                                        p1_move=str(p1_move), 
                                        p2_move=str(p2_move))
                file = discord.File(fp=img.image_bytes, filename="result.png")
                embed = discord.Embed(
                    title=f"{winner} wins!",
                ).set_image(url="attachment://result.png")
                await interaction.followup.send(embed=embed, file=file)
                await add_wins(winner.id, str(winner), interaction.guild_id)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user not in self.interactors:
            await interaction.response.send_message("Hey! This is not for you!", ephemeral=True)
            return False
        if str(interaction.user) in self._ready:
            await interaction.response.send_message("Your move is already saved!", ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        if len(self._ready) < 2:
            embed = discord.Embed(
                title="Timed out.",
                description="The battle timed out, one player did not press ready."
            ) 
        else:
            embed = discord.Embed(
                title="Battle timed out."
            )
        await self.interaction.edit_original_response(embed=embed)

    async def checker(self, *, p1, p2, p1_move, p2_move) -> discord.Member:
        """A checker for checking the winner"""
        winner = None
        if p1_move > p2_move:
            winner = p1
        elif p1_move < p2_move:
            winner = p2
        return winner
