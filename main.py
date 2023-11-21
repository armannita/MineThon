from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

terrain_size = 20
terrain_height = 5 

wood_texture = load_texture('textures/wood.png')
stone_texture = load_texture('textures/stone.png')
grass_texture = load_texture('textures/grass.png')
dirt_texture = load_texture('textures/dirt.png')

chat_input = InputField(parent=scene, position=(-0.5, -0.4), scale=(0.2, 0.05), text='', multiline=False, max_lines=1, on_submit=lambda: send_chat())
chat_history = Text(parent=scene, position=(-0.5, -0.35), scale=(0.2, 0.05), text='', origin=(0, 0))

def send_chat():
    message = chat_input.text.strip()
    if message:
        chat_history.text += '\n' + message
        chat_input.text = ''

baseplate = Entity(model='plane', texture=grass_texture, scale=terrain_size)

blocks = []

wood_block = wood_texture
stone_block = stone_texture
grass_block = grass_texture
dirt_block = dirt_texture

def add_block(position, block_texture):
    new_block = Entity(
        model='cube',
        texture=block_texture,
        position=position,
        collider='box'
    )
    blocks.append(new_block)

for x in range(terrain_size):
    for z in range(terrain_size):
        for y in range(terrain_height):
            if y == 0:
                add_block((x, y, z), stone_block)
            elif y < 3:
                add_block((x, y, z), dirt_block)
            else:
                add_block((x, y, z), grass_block)

player = FirstPersonController(position=(terrain_size / 2, terrain_height + 1, terrain_size / 2), collider='box')
Sky()

def input(key):
    global current_block_template
    
    for block in blocks:
        if block.hovered:
            if key == "right mouse down":
                add_block(block.position + mouse.normal, current_block_template)
            if key == "left mouse down":
                blocks.remove(block)
                destroy(block)

    if key.isdigit() and 1 <= int(key) <= 4:
        block_types = [wood_block, stone_block, grass_block, dirt_block]
        current_block_template = block_types[int(key) - 1]

    if key == 't':
        chat_input.enabled = not chat_input.enabled
        chat_input.text = ''

app.run()
