from ursina import *
app = Ursina()

bat_texture = load_texture('assets/bat.png')
knight_texture = load_texture('assets/knight.png')

from ursina.prefabs.platformer_controller_2d import PlatformerController2d
player = PlatformerController2d(y=1, z=.01, scale_y=1.5, scale_x=1.5, max_jumps=1  , texture = knight_texture,)

ground = Entity(model='quad', scale_x=10, collider='box', color=color.black)

quad = load_model('quad', use_deepcopy=True)

enemy = Entity(model='cube', collider='box', color=color.red, position=(16,5,-.1), texture= bat_texture,)
enemy.add_script(SmoothFollow(target=player, speed=2))
enemy.look_at(player)

sky = Entity(model = 'quad', scale = 1500, texture = 'sky_sunset',z = .5, origin = -0.2, double_sided = True,)

level_parent = Entity(model=Mesh(vertices=[], uvs=[]), texture='black_cube')
def make_level(texture):
    # ! Destroi os tiles ja existentes
    # ! Caso dê refresh
    # ! Não deixa o jogo lagar
    [destroy(c) for c in level_parent.children]

    for y in range(texture.height):
        collider = None
        for x in range(texture.width):
            col = texture.get_pixel(x,y)

            # Se for preto ele vai colocar um tijolo ali
            if col == color.black:
                level_parent.model.vertices += [Vec3(*e) + Vec3(x+.5,y+.5,0) for e in quad.generated_vertices]
                level_parent.model.uvs += quad.uvs
              
                if not collider:
                    collider = Entity(parent=level_parent, position=(x,y), model='quad', origin=(-.5,-.5), collider='box', visible=False)
                else:
                    # * Não criar vários colliders pra cada tile, só colocar em sequência
                    collider.scale_x += 1
            else:
                collider = None

            # * Setta o spawn no ponto verde
            if col == color.green:
                player.start_position = (x, y)
                player.position = player.start_position

    level_parent.model.generate()

make_level(load_texture('platformer_tutorial_level'))   # gera o level

camera.orthographic = True
camera.position = (30/2,8)
camera.fov = 16


player.traverse_target = level_parent

def update():
    if player.intersects(enemy).hit:
        print('Game over')
        player.position = player.start_position


input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'space')
input_handler.bind('gamepad dpad right', 'd')
input_handler.bind('gamepad dpad left', 'a')
input_handler.bind('gamepad a', 'space')

            # ? Puxar mais estilos de tile, pensar num jeito de arrumar a movimentação do morcego e procurar estilo de sprites pra animar
            # ? Mecânicas importantes:
            # * Dash, Sistema de health bar em coração (meio),  Espada com MS.
            # ! Arrumar um jeito de usar Group e GroupSingle

Sky = Sky()
app.run()
