import discord
from images.image_utils import vs_image

async def vs_embed(p1, p2):        
    img = await vs_image(p1_image=str(p1.avatar), p2_image=str(p2.avatar))
    file = discord.File(fp=img.image_bytes, filename="vs.png")
    embed = discord.Embed(color=discord.Color.blue(),
                        title=f"{p1} vs. {p2}")
    embed.set_image(url="attachment://vs.png")
    embed.set_footer(text="Remember to press `Ready!` after picking a choice!")
    return embed, file