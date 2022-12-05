# Simple map editor for the 2D map arry in game.py. Draw walls with left mouse button, erase walls with right mouse
# button. When you quit the map editor the map array is printed to the console. Copy the array and replace the one
# in game.py on line 28. Make sure you leave the outer walls in place as the ray casting engine does not currently 
# protect against rays that go out of bounds.

import pygame

pygame.init()

screen = pygame.display.set_mode((400, 400))

GREY = (50, 50, 50)
MUD = (128, 97, 60)
MAP_DIMENSION = 20
TILE_DIMENSION = 20

map = [[0 for x in range(MAP_DIMENSION)] for y in range(MAP_DIMENSION)]
for i in range(MAP_DIMENSION):
  map[0][i] = 1
  map[MAP_DIMENSION-1][i] = 1
  map[i][0] = 1
  map[i][MAP_DIMENSION-1] = 1

while True:
  screen.fill(GREY)

  for x in range(MAP_DIMENSION):
    for y in range(MAP_DIMENSION):
      value = map[x][y]

      if value == 0:
        color = MUD
      else:
        color = GREY

      surface = pygame.Surface((TILE_DIMENSION, TILE_DIMENSION))
      surface.fill(color)

      screen_x = x * TILE_DIMENSION
      screen_y = y * TILE_DIMENSION
      screen.blit(surface, (screen_x, screen_y))

    mouse1, mouse2, mouse3 = pygame.mouse.get_pressed()

    val = -1
    if mouse1:
        val = 1
    elif mouse3:
        val = 0

    if val != -1:
        x, y = pygame.mouse.get_pos()
        map_x = x // TILE_DIMENSION
        map_y = y // TILE_DIMENSION
        map[map_x] [map_y] = val

  pygame.display.update()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      print(map)
      pygame.quit()
      exit()

  