import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{0},{0}'

import pgzrun, math, pygame 
from random import random, randint
from pygame.math import Vector2

TITLE = "Flocking"
HEIGHT = 600
WIDTH = 600
NUM_BIRDS = 100
LOCAL_RADIUS = 50
MAX_STEERING_FORCE = 0.1
SPEED = 5

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
    return Vector2(f * vx, f * vy)

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

        if len(locals) > 0:
            steering_vector = self.steer_to_average_heading(locals)
            self.acceleration += steering_vector 

            steering_vector = self.steer_to_average_position(locals)
            self.acceleration += steering_vector 

            steering_vector = self.steer_to_avoid_crowding(locals)
            self.acceleration += steering_vector 

        # change the velociy based on the acceleration
        self.velocity += self.acceleration
        self.acceleration = Vector2(0, 0)
        
        # move the position based on the velocity 
        self.position += self.velocity

        self.warp()

    # Alignment    
    def steer_to_average_heading(self, locals):
        average_velocity = self.average_velocity(locals)
        if (average_velocity != Vector2(0, 0)):
            average_velocity.scale_to_length(SPEED) # set a max velocity
            average_velocity -= self.velocity # steer toward the average velocity
            average_velocity = clamp(average_velocity, MAX_STEERING_FORCE) # limit the amount of steer
        return average_velocity        
    

    # Cohesion 
    def steer_to_average_position(self, locals):
        average_position = self.average_position(locals)
        if (average_position != Vector2(0, 0)):
            average_position -= self.position # steer toward the position
            average_position.scale_to_length(SPEED) # set a max velocity
            average_position -= self.velocity # adjust for current heading
            average_position = clamp(average_position, MAX_STEERING_FORCE) # limit the amount of steer
        return average_position                
    
    
    # Separation
    def steer_to_avoid_crowding(self, locals):
        steering_vector = self.inverse_position_difference(locals)
        if (steering_vector != Vector2(0, 0)):
            steering_vector.scale_to_length(SPEED) # set a max velocity
            steering_vector -= self.velocity # adjust for current heading
            steering_vector = clamp(steering_vector, MAX_STEERING_FORCE) # limit the amount of steer
        return steering_vector


    def warp(self):        
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH

        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT
        

    def average_velocity(self, locals):
        total_heading = Vector2(0, 0)
        for bird in locals:
            total_heading += bird.velocity
        return total_heading / len(locals)


    def average_position(self, locals):
        total_position = Vector2(0, 0)
        for bird in locals:
            total_position += bird.position
        return total_position / len(locals)


    def inverse_position_difference(self, locals):
        total_position = Vector2(0, 0)
        for bird in locals:
            distance_vector = self.position - bird.position
            distance_vector.scale_to_length(1 / self.distance_to(bird)) # affect is inverse proportion to the length
            total_position += distance_vector
        return total_position


    def distance_to(self, bird):
        return self.position.distance_to(bird.position) + 0.0001

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
