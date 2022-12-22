import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{0},{0}'

import pgzrun, math, pygame 
from random import random, randint
from pygame.math import Vector2

TITLE = "Flocking"
HEIGHT = 600
WIDTH = 800
NUM_BIRDS = 100
LOCAL_RADIUS = 50
MAX_STEERING_FORCE = 0.1
SPEED = 3

GREEN = (0, 230, 0)
RED = (230, 0, 0)

birds = []

def clamp(vec, max_magnitude):
    vx = vec.x
    vy = vec.y
    n = math.sqrt(vx**2 + vy**2)
    if n == 0:
        return vec
    f = min(n, max_magnitude) / n
    return [f * vx, f * vy]

class Bird:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.5 - random(), 0.5 - random())
        self.velocity *= SPEED
        self.acceleration = Vector2(0, 0)

    
    def draw(self):
        xx = self.velocity.normalize().x * 10 + self.position.x
        yy = self.velocity.normalize().y * 10 + self.position.y
        screen.draw.line((self.position.x, self.position.y), (xx, yy), GREEN)


    def update(self):
        locals = []
        for bird in birds:
            if self != bird and self.distance_to(bird) < LOCAL_RADIUS:
                locals.append(bird)

        # steer towards the average heading of the local birds
        if len(locals) > 0:
            steering_force = self.average_heading(locals)
            if (steering_force != Vector2(0, 0)):
                steering_force.scale_to_length(SPEED) # set a max velocity
                steering_force -= self.velocity # steer toward the heading
                steering_force = clamp(steering_force, MAX_STEERING_FORCE) # limit the about of steer
                self.acceleration = steering_force # apply the steering force

        # change the velociy based on the acceleration
        self.velocity += self.acceleration

        # move the position based on the velocity 
        self.position += self.velocity

        self.warp()

    def warp(self):        
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH

        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT
        

    def average_heading(self, locals):
        total_heading = Vector2(0, 0)
        for bird in locals:
            total_heading += bird.velocity

        return total_heading / len(locals)



    def distance_to(self, bird):
        return self.position.distance_to(bird.position)

def draw():
    screen.clear()
    for bird in birds:
        bird.draw()

def update():
    for bird in birds:
        bird.update()   

for i in range(NUM_BIRDS):
    bird = Bird(randint(0, WIDTH), randint(0, HEIGHT))
    birds.append(bird)

pgzrun.go()
