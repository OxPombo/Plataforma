from asyncore import loop
import time
from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

app = Ursina()

window.color = color.light_gray
camera.orthographic = True
camera.fov = 20
window.borderless = False 

player = PlatformerController2d(
         y=1, 
         z=.01,
         scale_y= 2,
         scale_x = 1.5,
         color = color.blue,
         max_jumps = 100,
         )
         
camera.add_script(SmoothFollow(target = player, offset=[0,5,-30], speed=4))


chao = Entity (
    model = 'cube',
    color = color.green.tint( -0.4),
    z = -1,
    y = -1,
    origin_y = 0.5,
    scale = (1000, 100, 10),
    collider = 'box',
    ignore = True,
)

quad = load_model('quad', use_deepcopy=True)

level_parent = Entity(model=Mesh(vertices=[], uvs=[]), texture='white_cube')


def make_level(texture):
    [destroy(c) for c in level_parent.children]

    for y in range(texture.height):
        collider = None
        for x in range(texture.width):
            col = texture.get_pixel(x,y)
            if col == color.black:
                level_parent.model.vertices += [Vec3(*e) + Vec3(x+.5,y+.5,0) for e in quad.generated_vertices]
                level_parent.model.uvs += quad.uvs
                Entity(parent=level_parent, position=(x,y), model='cube', origin=(-.5,-.5), color=color.gray, texture='white_cube', visible=True)
                if not collider:
                    collider = Entity(
                        parent=level_parent,
                        position=(x,y),
                        model = 'quad',
                        origin = (-.5, -.5),
                        collider = 'box',
                        visible = False,

                    )
                else:
                    collider.scale_x += 1
        else: 
            collider = None

            if col == color.green:

                player.start_position = (x, y)
                player.position = player.start_position

level_parent.model.generate()
make_level(load_texture('platformer_tutorial_level'))
        

sky = Entity(
    model = 'quad',
    scale = 1500,
    texture = 'sky_sunset',
    z = .5,
    origin = -0.2,
    double_sided = True,
)


input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'space')
input_handler.bind('gamepad dpad right', 'd')
input_handler.bind('gamepad dpad left', 'a')
input_handler.bind('gamepad a', 'space')




player.add_script(NoclipMode2d())
Sky = Sky()

app.run()



