import time 
import math

import pygame

class Bullet:
    def __init__(self, x, y, direction, radius=2, color=(255,255,255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.fired_at = time.time()

        self.vel = 3.5
        self.direction = direction

        self.hit_wall = False

    def move(self):
        self.y += self.vel * math.sin(math.radians(self.direction))
        self.x += self.vel * math.cos(math.radians(self.direction))

    def draw(self, win):
        self.rect = pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
    