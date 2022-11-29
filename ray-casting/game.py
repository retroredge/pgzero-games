import os
# Position the game window top left
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{0},{0}'

import pgzrun
from pygame.math import Vector2

WIDTH = 1000
HEIGHT = 500
TILE_WIDTH = 50
CYAN = (0, 200, 200)
GREEN = (0, 200, 0)
GREY = (50, 50, 50)

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
        self.facing = Vector2(0, 20)
        self.rotate_angle = 3
        self.speed = 5

    def draw2d(self):
        screen.draw.circle((self.x, self.y), self.facing.magnitude(), GREEN)
        screen.draw.line((self.x, self.y), 
            (self.x + self.facing.x, self.y - self.facing.y), CYAN)

    def turn(self, direction):
        if direction == 1:
            self.facing = self.facing.rotate(self.rotate_angle)
        else:
            self.facing = self.facing.rotate(-self.rotate_angle)

    def move(self):
        move_vec = self.facing.normalize()
        self.x = self.x + move_vec.x * self.speed
        self.y = self.y - move_vec.y * self.speed

        radius = self.facing.magnitude()
        self.x = min(WIDTH // 2 - radius, max(radius, self.x))
        self.y = min(HEIGHT - radius, max(radius, self.y))


player = Player(TILE_WIDTH * 5, TILE_WIDTH * 8)


def draw():
    screen.clear()
    for my in range(map_height):
        for mx in range(map_width):
            if level[my] [mx] == 1:
                grid_colour = CYAN
            else:
                grid_colour = GREY

            box = Rect((mx * TILE_WIDTH, my * TILE_WIDTH), (TILE_WIDTH, TILE_WIDTH))
            screen.draw.rect(box, grid_colour)

    player.draw2d()            


def update():
    if keyboard.left or keyboard.a:
        player.turn(1)
    elif keyboard.right or keyboard.d:
        player.turn(-1)

    if keyboard.up or keyboard.w:
        player.move()

pgzrun.go()
