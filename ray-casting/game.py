import os
# Position the game window top left
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{0},{0}'

import pgzrun, math, pygame 
from math import *

WIDTH = 1000
MAP_WIDTH = WIDTH / 2
HEIGHT = int(WIDTH / 2)
TILE_WIDTH = HEIGHT / 10
CYAN = (0, 200, 200)
GREEN = (0, 230, 0)
GREY = (50, 50, 50)
YELLOW = (225, 225, 0)
FOV = math.pi / 3  # about 60 degrees
VIEW_PORT_WIDTH = int(MAP_WIDTH / 10)

level = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,1],
    [1,0,0,0,0,0,0,1,0,1],
    [1,0,0,1,1,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,1],
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
        self.speed = 4

    def draw(self):
        screen.draw.circle((self.x, self.y), 10, GREEN)
        screen.draw.line((self.x, self.y), (self.x + math.sin(self.facing) * 10, self.y - math.cos(self.facing) * 10), GREEN)

    def turn(self, direction):
        if direction == 1:
            self.facing += self.rotate_angle
        else:
            self.facing -= self.rotate_angle

    def move(self):
        x = self.x
        y = self.y

        x += math.sin(self.facing) * self.speed
        y -= math.cos(self.facing) * self.speed

        x = min(WIDTH / 2, max(0, x))
        y = min(HEIGHT, max(0, y))

        if not is_tile_at(x, y):
            self.x = x
            self.y = y

def ray_cast(x, y, facing):
    angle = facing + (FOV / 2)
    for ray in range(VIEW_PORT_WIDTH):
        # todo need HEIGHT to be far enough to cross the diagonal screen
        for distance in range(HEIGHT):
            px = x + math.sin(angle) * distance
            py = y - math.cos(angle) * distance
            if is_tile_at(px, py):
                break
            screen.draw.line((x, y), (px, py), YELLOW)
        angle -= FOV / VIEW_PORT_WIDTH

def draw():
    screen.clear()
    # map grid
    for my in range(map_height):
        for mx in range(map_width):
            if level[my] [mx] == 1:
                grid_colour = CYAN
            else:
                grid_colour = GREY

            box = Rect((mx * TILE_WIDTH, my * TILE_WIDTH), (TILE_WIDTH - 1, TILE_WIDTH - 1))
            screen.draw.rect(box, grid_colour)

    player.draw()   

    ray_cast(player.x, player.y, player.facing)        

def update():
    if keyboard.left or keyboard.a:
        player.turn(-1)
    elif keyboard.right or keyboard.d:
        player.turn(1)

    if keyboard.up or keyboard.w:
        player.move()

def is_tile_at(x, y):
    col = int(x / TILE_WIDTH)
    row = int(y / TILE_WIDTH)
    return level[row] [col] == 1

player = Player(TILE_WIDTH * 5 + 25, TILE_WIDTH * 8 + 25)
pgzrun.go()
