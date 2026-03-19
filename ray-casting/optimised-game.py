# Simple ray casting engine that renders a vertical rectangle per ray cast in the 2D map onto a 
# 3D view. Use SCALE_FACTOR to control the width of the rectangles which effects frame rate and
# coarseness of the 3D view. FOV controls the field of view.

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{0},{0}'

import pgzrun, math, pygame 
from math import *

TITLE = "Ray Casting"
HEIGHT = 700
WIDTH = HEIGHT * 2
MAP_WIDTH = HEIGHT
TILE_WIDTH = HEIGHT / 200
FOV = math.pi / 3  # about 60 degrees
SCALE_FACTOR = 3 # larger values improve fps but increase the coarseness 
VIEW_PORT_WIDTH = int(MAP_WIDTH / SCALE_FACTOR) 
MAX_DISTANCE = int(math.sqrt(HEIGHT ** 2 + HEIGHT ** 2))
VIEWING_DISTANCE = (MAP_WIDTH / 2) / math.tan(FOV / 2)  # distance from viewer to camera plane
WALL_HEIGHT = HEIGHT / 200

CYAN = (0, 200, 200)
GREEN = (0, 230, 0)
BLUE = (0, 10, 230)
MUD = (210,150,75)
GREY = (50, 50, 50)
YELLOW = (225, 225, 0)

clock = pygame.time.Clock()

with open('level.txt') as f:
    level = [[int(c) for c in line.strip()] for line in f]


map_height = len(level)
map_width = len(level[0])

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.facing = 0
        self.rotate_angle = FOV / 10
        self.speed = TILE_WIDTH * 0.7  # must stay below TILE_WIDTH to avoid skipping through walls

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), 4, GREEN)

    def turn(self, direction):
        self.facing += self.rotate_angle * direction

    def move(self, direction, straf = False):
        facing = self.facing
        if straf:
            facing = self.facing + (math.pi / 2) # rotate facing 90 degrees for strafing movement

        dx = math.sin(facing) * self.speed * direction
        dy = -math.cos(facing) * self.speed * direction

        if not is_solid(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
        elif not is_solid(self.x + dx, self.y):
            self.x += dx
        elif not is_solid(self.x, self.y + dy):
            self.y += dy

_angle_offsets = [FOV / 2 - ray * (FOV / VIEW_PORT_WIDTH) for ray in range(VIEW_PORT_WIDTH)]
_fisheye_cos = [math.cos(offset) for offset in _angle_offsets]

def ray_cast(x, y, facing):
    for ray in range(VIEW_PORT_WIDTH):
        angle = facing + _angle_offsets[ray]
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)

        # DDA setup
        col = int(x / TILE_WIDTH)
        row = int(y / TILE_WIDTH)

        if sin_a != 0:
            delta_x = TILE_WIDTH / abs(sin_a)
            if sin_a > 0:
                step_col = 1
                side_x = ((col + 1) * TILE_WIDTH - x) / sin_a
            else:
                step_col = -1
                side_x = (col * TILE_WIDTH - x) / sin_a
        else:
            delta_x = float('inf')
            side_x = float('inf')
            step_col = 0

        ray_dir_y = -cos_a
        if ray_dir_y != 0:
            delta_y = TILE_WIDTH / abs(ray_dir_y)
            if ray_dir_y > 0:
                step_row = 1
                side_y = ((row + 1) * TILE_WIDTH - y) / ray_dir_y
            else:
                step_row = -1
                side_y = (row * TILE_WIDTH - y) / ray_dir_y
        else:
            delta_y = float('inf')
            side_y = float('inf')
            step_row = 0

        # DDA march to next tile boundary until wall hit
        distance = 0
        while True:
            if side_x < side_y:
                distance = side_x
                side_x += delta_x
                col += step_col
            else:
                distance = side_y
                side_y += delta_y
                row += step_row
            if not (0 <= col < map_width and 0 <= row < map_height):
                break
            if level[row][col] == 1:
                break

        px = x + sin_a * distance
        py = y - cos_a * distance
        screen.draw.line((x, y), (px, py), YELLOW)

        # 3D projection
        shade = max(0, int(230 - distance / 3))
        wall_colour = (0, shade, 0)
        distance *= _fisheye_cos[ray]  # fix the fish eye effect
        wall_height = (WALL_HEIGHT / distance) * VIEWING_DISTANCE if distance > 0 else HEIGHT

        box = Rect(
            (WIDTH - (ray * SCALE_FACTOR) - SCALE_FACTOR, (HEIGHT / 2) - (wall_height / 2)),
            (SCALE_FACTOR, wall_height))
        screen.draw.filled_rect(box, wall_colour)

def _make_map_surface():
    surf = pygame.Surface((MAP_WIDTH, HEIGHT))
    surf.fill((0, 0, 0))
    tile_size = max(1, int(TILE_WIDTH - 1))
    for my in range(map_height):
        for mx in range(map_width):
            color = CYAN if level[my][mx] == 1 else GREY
            tile_rect = pygame.Rect(int(mx * TILE_WIDTH), int(my * TILE_WIDTH), tile_size, tile_size)
            pygame.draw.rect(surf, color, tile_rect, 1)
    return surf

_map_surf = _make_map_surface()

def draw_map_grid():
    screen.blit(_map_surf, (0, 0))

def _make_gradient_surface(width, height, color1, color2):
    surf = pygame.Surface((width, height))
    diff = [color2[i] - color1[i] for i in range(3)]
    for y in range(height):
        color = [color1[i] + diff[i] * y / height for i in range(3)]
        pygame.draw.line(surf, color, (0, y), (width - 1, y))
    return surf

_sky_surf = _make_gradient_surface(MAP_WIDTH, HEIGHT // 2, BLUE, (0, 0, 0))
_floor_surf = _make_gradient_surface(MAP_WIDTH, HEIGHT // 2, (0, 0, 0), MUD)

def draw_floor_sky():
    screen.blit(_sky_surf, (MAP_WIDTH, 0))
    screen.blit(_floor_surf, (MAP_WIDTH, HEIGHT // 2))

def draw():
    screen.clear()
    draw_map_grid()
    draw_floor_sky()
    player.draw()   
    ray_cast(player.x, player.y, player.facing)
    screen.draw.text(str(int(clock.get_fps())), topleft = (0, 0), color="yellow")

def update():
    if keyboard.a:
        player.move(-1, True)
    elif keyboard.d:
        player.move(1, True)

    if keyboard.left:
        player.turn(-1)
    elif keyboard.right:
        player.turn(1)

    if keyboard.up or keyboard.w:
        player.move(1)
    elif keyboard.down or keyboard.s:
        player.move(-1)

    clock.tick()
        
def is_tile_at(x, y):
    col = int(x / TILE_WIDTH)
    row = int(y / TILE_WIDTH)
    if not (0 <= col < map_width and 0 <= row < map_height):
        return True
    return level[row][col] == 1

COLLISION_RADIUS = TILE_WIDTH * 0.6

def is_solid(x, y):
    r = COLLISION_RADIUS
    return (is_tile_at(x + r, y + r) or is_tile_at(x - r, y + r) or
            is_tile_at(x + r, y - r) or is_tile_at(x - r, y - r))

player = Player(TILE_WIDTH * 18, TILE_WIDTH * 18)
pgzrun.go()
