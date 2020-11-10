import time
import math

import pygame

from bullet import Bullet


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 3
        self.rotation_vel = 3
        self.rect = (x, y, width, height)

        self.diretion = 0 # direction in degrees
        
        self.remain_bullets = 5
        self.bullets = []

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def move_bullets(self):
        for b in self.bullets:
            b.move()

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        self.remove_expired_bullets()
        self.draw_bullets(win)
    
    def remove_expired_bullets(self):
        valid_bullets = []
        for b in self.bullets:
            if time.time() - b.fired_at <= 5 :
                valid_bullets.append(b)
            else:
                self.remain_bullets += 1
        
        self.bullets = valid_bullets

    def draw_bullets(self, win):
        for b in self.bullets:
            b.draw(win)
    
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.diretion  = (self.diretion - self.rotation_vel) % 360

        if keys[pygame.K_RIGHT]:
            self.diretion  = (self.diretion + self.rotation_vel) % 360
        
        if keys[pygame.K_UP]:
            self.y += self.vel * math.sin(math.radians(self.diretion))
            self.x += self.vel * math.cos(math.radians(self.diretion))

        
        if keys[pygame.K_DOWN]:
            self.y -= self.vel * math.sin(math.radians(self.diretion))
            self.x -= self.vel * math.cos(math.radians(self.diretion))


        self.update()
        self.move_bullets()

    def fire(self):
        if self.remain_bullets > 0:
            bullet = Bullet(self.x, self.y)
            self.bullets.append(bullet)
            self.remain_bullets -= 1
            return bullet
