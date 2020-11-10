import pygame
import time

class Bullet:
    def __init__(self, x, y, radius=2, color=(255,255,255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.fired_at = time.time()


    def move(self):
        self.x += 2

    def draw(self, win):
        self.rect = pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
         