import os
# Position the game window top left
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{0},{0}'

import pgzrun
from random import randint, choice

WIDTH = 800
HEIGHT = 480
TITLE = "Fruit Monkey!"
MONKEY_SPEED = 7
NUMBER_OF_FRUIT = 10
BORDER_OFFSET = 10

monkey = Actor("still")
fruit_images = ["fruit00", "fruit10", "fruit20"]
fruit_list = []
baddie = Actor("flame")    
game_ticks = 1

# PGZero engine calls this 60 times per second. Draw sprites and backgrounds here
def draw():
    screen.blit("table", (0,0))

    for i in range(len(fruit_list)):
        fruit_list[i].draw()

    monkey.draw()
    baddie.draw()

    if monkey.dead:
       display_text("Monkey Dead :(")

    if monkey.won:
        display_text('Monkey Wins!!!')
    


def display_text(text):
    colours_and_offsets = {(10, 10, 10): 3, (255, 0, 255): 0}
    for colour, offset in colours_and_offsets.items():
        screen.draw.text(
            text,
            center = ((WIDTH // 2) + offset, 100 + offset),
            color = colour,
            fontsize = 50
        )


# PGZero engine calls this 60 times per second. Update game state here
def update():
    global game_ticks
    game_ticks += 1
    move_monkey()
    check_monkey_fruit_collision()
    move_baddie()
    check_monkey_baddie_collision()


def move_baddie():
    if baddie.dead:
        return

    # Baddie gets faster and jittery once he's near the monkey
    if baddie.distance_to(monkey) < 150:
        baddie_speed = randint(6, 7)
    else:
        baddie_speed = 6
    
    # Home in on the monkey's position
    dx = 0
    dy = 0
    if (baddie.x > monkey.x):
        dx = -1
    elif (baddie.x < monkey.x):
        dx = 1

    if (baddie.y > monkey.y):
        dy = -1
    elif (baddie.y < monkey.y):
        dy = 1

    if dx != 0 and dy != 0:
        dx = dx * 0.707
        dy = dy * 0.707

    baddie.x = baddie.x + (dx * baddie_speed)
    baddie.y = baddie.y + (dy * baddie_speed)


# colliderect gives monkey a generous chance to grab the fruit when he's near it
def check_monkey_fruit_collision():
    global fruit_list 
    for i in range(len(fruit_list)):
        fruit = fruit_list[i]
        if monkey.colliderect(fruit) and fruit.state == "ready":
            fruit.state = "eaten"
            sounds.score0.play()
            animate(fruit, tween="accelerate", duration=0.1, pos=(fruit.x, -50), on_finished=remove_fruit(fruit))

    # Use list comprehension to filter out the eaten fruit from the list
    fruit_list = [fruit for fruit in fruit_list if fruit.state != "gone"]

    if len(fruit_list) == 0:
        baddie.dead = True             
        monkey.won = True


# collidepoint gives monkey an easier time than if we use colliderect
def check_monkey_baddie_collision():
    if baddie.dead:
        return

    if monkey.collidepoint(baddie.pos):
        monkey.dead = True
        baddie.dead = True


def remove_fruit(fruit):
    fruit.state = "gone"


def move_monkey():
    global game_ticks

    if monkey.dead or monkey.won:
        if keyboard.RETURN:
            reset_game()
        return 

    dx = -1
    if keyboard.left:
        monkey.x -= MONKEY_SPEED
        dx = 0

    if keyboard.right:
        monkey.x += MONKEY_SPEED
        dx = 1

    if keyboard.up:
        monkey.y -= MONKEY_SPEED

    if keyboard.down:
        monkey.y += MONKEY_SPEED       

    monkey.y = min(407, max(15, monkey.y))     
    monkey.x = min(755, max(40, monkey.x))  

    if (dx == -1):
        monkey.image = "still"
    else:
        monkey.image = "run" + str(dx) + str((game_ticks // 4) % 4)

def reset_game():
    global fruit_list 
    monkey.pos = WIDTH // 2, HEIGHT // 2
    monkey.dead = False
    monkey.won = False
    
    fruit_list = []
    for i in range(NUMBER_OF_FRUIT):
        fruit = Actor(choice(fruit_images))
        fruit.topleft = randint(BORDER_OFFSET, WIDTH - BORDER_OFFSET - fruit.width), \
                randint(BORDER_OFFSET, HEIGHT - BORDER_OFFSET - fruit.height)
        fruit.state = "ready"
        fruit_list.append(fruit)

    baddie.topleft = BORDER_OFFSET, BORDER_OFFSET
    baddie.dead = False

reset_game()
pgzrun.go()