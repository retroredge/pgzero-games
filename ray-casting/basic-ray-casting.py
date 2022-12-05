# This is a basic implementation of a ray casting engine. It renders a 1 pixel wide vertical line per
# ray cast in the 2D map onto a 300 pixel wide 3D view. 

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{0},{0}'

import pgzrun, math, pygame 
from math import *

HEIGHT = 300
WIDTH = HEIGHT * 2
MAP_WIDTH = HEIGHT
TILE_WIDTH = HEIGHT / 10
FOV = math.pi / 3  # about 60 degrees
VIEW_PORT_WIDTH = int(MAP_WIDTH)
MAX_DISTANCE = int(math.sqrt(HEIGHT ** 2 + HEIGHT ** 2))
VIEWING_DISTANCE = (MAP_WIDTH / 2) / math.tan(FOV / 2)
ACTUAL_WALL_HEIGHT = HEIGHT / 10

CYAN = (0, 200, 200)
GREEN = (0, 230, 0)
BLUE = (0, 10, 230)
MUD = (210,150,75)
GREY = (50, 50, 50)
YELLOW = (225, 225, 0)

level = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]

map_height = len(level[0])
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
        if direction == 1:
            self.facing += self.rotate_angle
        else:
            self.facing -= self.rotate_angle

    def move(self, direction):
        x = self.x
        y = self.y

        x += math.sin(self.facing) * self.speed * direction
        y -= math.cos(self.facing) * self.speed * direction

        x = min(WIDTH / 2, max(0, x))
        y = min(HEIGHT, max(0, y))

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
        wall_colour = (0, int(230 - distance / 3), 0)
        distance *= math.cos(facing - angle) # fix the fish eye effect
        wall_height = (ACTUAL_WALL_HEIGHT / distance) * VIEWING_DISTANCE
        screen.draw.line(
            (WIDTH - ray, (HEIGHT / 2) - (wall_height / 2)), 
            ((WIDTH - ray), (HEIGHT / 2) + (wall_height / 2)),
            wall_colour)

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
    screen.draw.filled_rect(sky, BLUE)
    floor = Rect((MAP_WIDTH, HEIGHT / 2), (MAP_WIDTH, HEIGHT))
    screen.draw.filled_rect(floor, MUD)

def draw():
    screen.clear()
    draw_map_grid()
    draw_floor_sky()
    player.draw()   
    ray_cast(player.x, player.y, player.facing)

def update():
    if keyboard.left or keyboard.a:
        player.turn(-1)
    elif keyboard.right or keyboard.d:
        player.turn(1)

    if keyboard.up or keyboard.w:
        player.move(1)
    elif keyboard.down or keyboard.s:
        player.move(-1)
        
def is_tile_at(x, y):
    col = int(x / TILE_WIDTH)
    row = int(y / TILE_WIDTH)
    return level[row] [col] == 1

player = Player(TILE_WIDTH * 8 + TILE_WIDTH / 2, TILE_WIDTH * 8 + TILE_WIDTH / 2)
pgzrun.go()
