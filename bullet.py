import time 
import math

import pygame

from wall import WallDirection

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
        self.active = True
        self.px = None # previous x value
        self.py = None # previous y value


    def move(self, walls):
        self.px = self.x
        self.py = self.y

        self.y += self.vel * math.sin(math.radians(self.direction))
        self.x += self.vel * math.cos(math.radians(self.direction))

        wall = self.contact_wall(walls)
        if wall:
            self.hit_wall = True
            self.bounce(wall)
    
    def contact_wall(self, walls):
        for wall in walls:
            if wall.has_collision((self.x,self.y), self.radius):
                return wall
        
        return None
    
    def bounce(self, wall):
        if wall.direction == WallDirection.VERT:
            self.direction = 180 - self.direction
        else:
            self.direction = -(self.direction)

    def draw(self, win):
        self.rect = pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

    def inactive(self):
        self.active = False
    
    