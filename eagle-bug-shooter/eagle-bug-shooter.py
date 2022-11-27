import os
# Position the game window top left
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{0},{0}'

import pgzrun
from random import randint, choice

WIDTH = 480
HEIGHT = images.bg0.get_height()
TITLE = "Eagle Bug Shooter!"
EAGLE_SPEED = 7
MEANIE_SPEED = 5
BULLET_SPEED = 20
FREE_LIFE_EVERY = 5000

eagle = Actor("eagle")
bullet = Actor("bullet")
meanies = []
background_y = 0
game_ticks = 1
meanie_spawn_rate = 100
score = 0
next_free_life = FREE_LIFE_EVERY

def draw():
    screen.blit('bg0', (0, background_y))
    screen.blit('bg0', (0, background_y - images.bg0.get_height()))

    for i in range(len(meanies)):
        meanies[i].draw()
    
    if bullet.alive:
        bullet.draw()

    if eagle.health > 0:
        screen.blit("eagles", (eagle.x, eagle.y))
        eagle.draw()
    else:
        display_text("Game Over", (WIDTH // 2, HEIGHT // 2))
        display_text("Press return", (WIDTH // 2, HEIGHT // 2 + 50))
    
    for i in range(eagle.health):
        screen.blit("health", (i * 10, HEIGHT - 30))

    display_text("Score: " + str(score), (WIDTH // 2, 20))


def display_text(text, position):
    colours_and_offsets = {(50, 50, 50): 3, (210, 150, 75): 0}
    for colour, offset in colours_and_offsets.items():
        screen.draw.text(
            text,
            center = (position[0] + offset, position[1] + offset),
            color = colour,
            fontsize = 50
        )

def update():
    global background_y, game_ticks, meanies, meanie_spawn_rate, next_free_life
    game_ticks += 1
    background_y += 2
    if background_y > images.bg0.get_height(): 
        background_y = 0
        meanie_spawn_rate = max(30, meanie_spawn_rate - 5)

    move_eagle()
    move_bullet()
    spawn_meanies()
    move_meanies()
    check_bullet_meanie_collision()
    meanies = [m for m in meanies if m.alive == True]
    if score >= next_free_life:
        eagle.health += 1
        next_free_life += FREE_LIFE_EVERY
        sounds.wave0.play()


def check_bullet_meanie_collision():
    global score
    if bullet.alive:
        for i in range(len(meanies)):
            if meanies[i].collidepoint(bullet.pos):
                meanies[i].alive = False
                bullet.alive = False
                score += (meanies[i].type + 1) * 100
                sounds.trap1.play()

def move_bullet():
    if bullet.alive:
        bullet.y -= BULLET_SPEED    
        if bullet.y < -bullet.height:
            bullet.alive = False
        
def on_key_up(key):
    if key == keys.SPACE and not bullet.alive and eagle.health > 0:
        bullet.alive = True
        bullet.pos = eagle.pos

def move_meanies():
    for i in range(len(meanies)):
        meanies[i].y += MEANIE_SPEED
        meanies[i].image = "meanie" + str(meanies[i].type) + str((game_ticks // 8) % 3)
        if meanies[i].y > HEIGHT:
            meanies[i].alive = False
            if eagle.health > 0:
                sounds.eagle0.play()
            eagle.health -= 1
            

def spawn_meanies():
    if eagle.health <= 0:
        return

    if (game_ticks % meanie_spawn_rate == 0):
        meanie_type = randint(0, 2)
        meanie = Actor("meanie0" + str(meanie_type))
        meanie.pos = (randint(10, WIDTH - 10), 0)
        meanie.type = meanie_type
        meanies.append(meanie)
        meanie.alive = True


def move_eagle():
    if eagle.health <= 0:
        if keyboard.RETURN:
            reset_game()
        return 

    if keyboard.left:
        eagle.x -= EAGLE_SPEED
    elif keyboard.right:
        eagle.x += EAGLE_SPEED
    eagle.x = min(WIDTH, max(0, eagle.x))             


def reset_game():
    global score, meanie_spawn_rate, background_y
    eagle.pos = WIDTH // 2, HEIGHT - eagle.height
    eagle.health = 3
    bullet.alive = False
    background_y = 0
    score = 0
    meanie_spawn_rate = 100

reset_game()
pgzrun.go()
