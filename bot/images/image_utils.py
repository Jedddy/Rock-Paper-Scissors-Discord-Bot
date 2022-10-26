from easy_pil import Editor
from easy_pil import load_image_async

p1_pos = 55, 80
p2_pos = 424, 80
p1_move_pos = 55, 180
p2_move_pos = 424, 180
pfp_resize = 160, 160

vs_bg_path = r"bot\images\background\versus.png"
# crown_path = r"bot\images\sprites\crown.png"
moves_sprite = r"bot\images\sprites\{move}.png"

async def load_challenge_image(p1_image):
    bg = Editor(vs_bg_path)
    if p1_image:
        p1_image = await load_image_async(p1_image)
        p1_image = Editor(p1_image) 
        bg.paste(p1_image.circle_image(), position=p1_pos)
    return bg

async def vs_image(*, p1_image, p2_image):
    bg = Editor(vs_bg_path)
    if p1_image:
        p1_image = await load_image_async(p1_image)
        p1_image = Editor(p1_image)
        p1_image.resize(pfp_resize)
        bg.paste(p1_image.circle_image(), position=p1_pos)
    if p2_image:
        p2_image = await load_image_async(p2_image)
        p2_image = Editor(p2_image)
        p2_image.resize(pfp_resize)
        bg.paste(p2_image.circle_image(), position=p2_pos)
    return bg

async def result_image(*, image, p1_move, p2_move):
    p1_move = Editor(moves_sprite.format(move=p1_move)).resize(pfp_resize)
    p2_move = Editor(moves_sprite.format(move=f"{p2_move}_right")).resize(pfp_resize)
    bg = Editor(image)
    bg.paste(p1_move, position=p1_move_pos)
    bg.paste(p2_move, position=p2_move_pos)
    return bg