import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{0},{0}'

import pgzrun, math, pygame 
from math import *
from random import randint

TITLE = "Conway's Game of Life"
HEIGHT = 600
WIDTH = 800
CELL_SIZE = 10
MAP_HEIGHT = HEIGHT // CELL_SIZE
MAP_WIDTH = WIDTH // CELL_SIZE
DENSITY = int(MAP_HEIGHT * MAP_WIDTH * 0.3)

BLUE = (50, 100, 200)
YELLOW = (255, 215, 0)

ticks = 0
grid = [ [0] * (MAP_HEIGHT) for i in range(MAP_WIDTH)]
next_grid = [ [0] * (MAP_HEIGHT) for i in range(MAP_WIDTH)]
for i in range(DENSITY):
    x = randint(1, MAP_WIDTH - 2)
    y = randint(1, MAP_HEIGHT - 2)
    grid[x][y] = 1


def draw():
    global ticks, grid
    screen.clear()

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            box = Rect((x * CELL_SIZE, y * CELL_SIZE), (CELL_SIZE - 1, CELL_SIZE - 1))
            if grid[x][y] == 0:
                screen.draw.rect(box, BLUE)
            else:
                screen.draw.filled_rect(box, YELLOW)

def update():
    global ticks, grid, next_grid

    ticks += 1
    if ticks % 10 != 0:
        return

    next_grid = [ [0] * (MAP_HEIGHT) for i in range(MAP_WIDTH)]
    for y in range(1, MAP_HEIGHT - 1):
        for x in range(1, MAP_WIDTH - 1):
            num_neighbours = neighbours(x, y)
            
            if grid[x][y] == 1 and num_neighbours < 2:
                # Death by under population
                next_grid[x][y] = 0
            elif grid[x][y] == 1 and num_neighbours > 3:
                # Death by over population
                next_grid[x][y] = 0
            elif grid[x][y] == 0 and num_neighbours == 3:
                # Brith
                next_grid[x][y] = 1
            else:
                # Survive
                next_grid[x][y] = grid[x][y]
    
    grid = next_grid
    

def neighbours(x, y):
    return (grid[x][y-1] + 
        grid[x+1][y-1] + 
        grid[x+1][y] + 
        grid[x+1][y+1] + 
        grid[x][y+1] + 
        grid[x-1][y+1] + 
        grid[x-1][y] + 
        grid[x-1][y-1])

pgzrun.go()

