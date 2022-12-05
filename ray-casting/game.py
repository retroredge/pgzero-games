# Simple ray casting engine that renders a vertical rectangle per ray cast in the 2D map onto a 
# 3D view. Use SCALE_FACTOR to control the width of the rectangles which effects frame rate and
# courseness of the 3D view. FOV controls the field of view.

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{0},{0}'

import pgzrun, math, pygame 
from math import *

TITLE = "Ray Casting"
HEIGHT = 500
WIDTH = HEIGHT * 2
MAP_WIDTH = HEIGHT
TILE_WIDTH = HEIGHT / 20
FOV = math.pi / 3  # about 60 degrees
SCALE_FACTOR = 3 # larger values improve fps but increase the coarseness 
VIEW_PORT_WIDTH = int(MAP_WIDTH / SCALE_FACTOR) 
MAX_DISTANCE = int(math.sqrt(HEIGHT ** 2 + HEIGHT ** 2))
VIEWING_DISTANCE = (MAP_WIDTH / 2) / math.tan(FOV / 2)  # distance from viewer to camera plane
WALL_HEIGHT = HEIGHT / 20

CYAN = (0, 200, 200)
GREEN = (0, 230, 0)
BLUE = (0, 10, 230)
MUD = (210,150,75)
GREY = (50, 50, 50)
YELLOW = (225, 225, 0)

clock = pygame.time.Clock()

level = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,1,0,0,0,0,1,1,1,0,0,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,1,0,0,0,0,1,1,0,1,1,0,0,0,1,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1,0,1,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

map_height = len(level)
map_width = len(level[0])

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.facing = 0
        self.rotate_angle = FOV / 10
        self.speed = 5

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), 4, GREEN)

    def turn(self, direction):
        self.facing += self.rotate_angle * direction

    def move(self, direction):
        x = self.x
        y = self.y

        x += math.sin(self.facing) * self.speed * direction
        y -= math.cos(self.facing) * self.speed * direction

        if not is_tile_at(x, y):
            self.x = x
            self.y = y

def ray_cast(x, y, facing):
    angle = facing + (FOV / 2)
    for ray in range(VIEW_PORT_WIDTH):
        for distance in range(MAX_DISTANCE):
            px = x + math.sin(angle) * distance
            py = y - math.cos(angle) * distance
            if is_tile_at(px, py):
                break
        
        screen.draw.line((x, y), (px, py), YELLOW)

        # 3D projection
        shade = max(0, int(230 - distance / 3))
        wall_colour = (0, shade, 0)
        distance *= math.cos(facing - angle) # fix the fish eye effect
        wall_height = (WALL_HEIGHT / distance) * VIEWING_DISTANCE
        
        box = Rect(
            (WIDTH - (ray * SCALE_FACTOR) - SCALE_FACTOR, (HEIGHT / 2) - (wall_height / 2)), 
            (SCALE_FACTOR, wall_height))
        screen.draw.filled_rect(box, wall_colour)

        angle -= FOV / VIEW_PORT_WIDTH

def draw_map_grid():
    for my in range(map_height):
        for mx in range(map_width):
            if level[my] [mx] == 1:
                grid_colour = CYAN
            else:
                grid_colour = GREY

            box = Rect((mx * TILE_WIDTH, my * TILE_WIDTH), (TILE_WIDTH - 1, TILE_WIDTH - 1))
            screen.draw.rect(box, grid_colour)

def draw_floor_sky():
    sky = Rect((MAP_WIDTH, 0), (MAP_WIDTH, HEIGHT / 2))
    gradient_fill(BLUE, (0,0,0), sky)
    floor = Rect((MAP_WIDTH, HEIGHT / 2), (MAP_WIDTH, HEIGHT))
    gradient_fill((0,0,0), MUD, floor)

def gradient_fill(color1, color2, rectangele):
    difference = [color2[i] - color1[i] for i in range(3)]
    for y in range(rectangele.height):
        color = [color1[i] + (difference[i] * y / rectangele.height) for i in range(3)]
        surface = pygame.Surface((rectangele.width, 1))
        surface.fill(color)
        screen.blit(surface, (rectangele.x, rectangele.y + y))

def draw():
    screen.clear()
    draw_map_grid()
    draw_floor_sky()
    player.draw()   
    ray_cast(player.x, player.y, player.facing)
    screen.draw.text(str(int(clock.get_fps())), topleft = (0, 0), color="yellow")

def update():
    if keyboard.left or keyboard.a:
        player.turn(-1)
    elif keyboard.right or keyboard.d:
        player.turn(1)

    if keyboard.up or keyboard.w:
        player.move(1)
    elif keyboard.down or keyboard.s:
        player.move(-1)

    clock.tick()
        
def is_tile_at(x, y):
    col = int(x / TILE_WIDTH)
    row = int(y / TILE_WIDTH)
    return level[row] [col] == 1

player = Player(TILE_WIDTH * 18, TILE_WIDTH * 18)
pgzrun.go()
