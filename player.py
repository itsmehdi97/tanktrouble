import time
import math

import pygame

from bullet import Bullet


class Player:
    def __init__(self, x, y, width, height, color):
        self.alive = True

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 3
        self.rotation_vel = 3
        self.rect = (x, y, width, height)

        self.direction = 0 # direction in degrees
        
        self.remain_bullets = 5
        self.bullets = []

    @property
    def center(self):
        return (self.x + self.width/2, self.y + self.height/2)    

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def move_bullets(self):
        for b in self.bullets:
            b.move()

    def validate_bullets(self):
        for b in self.bullets:
            if time.time() - b.fired_at >= 5:
                b.inactive()

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        self.validate_bullets()
        self.remove_inactive_bullets()
        self.draw_bullets(win)
    
    def remove_inactive_bullets(self):
        valid_bullets = []
        for b in self.bullets:
            if b.active:
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
            self.direction  = (self.direction - self.rotation_vel) % 360

        if keys[pygame.K_RIGHT]:
            self.direction  = (self.direction + self.rotation_vel) % 360
        
        if keys[pygame.K_UP]:
            self.y += self.vel * math.sin(math.radians(self.direction))
            self.x += self.vel * math.cos(math.radians(self.direction))

        
        if keys[pygame.K_DOWN]:
            self.y -= self.vel * math.sin(math.radians(self.direction))
            self.x -= self.vel * math.cos(math.radians(self.direction))


        self.update()
        self.move_bullets()

    def fire(self):
        if self.remain_bullets > 0:
            bullet = Bullet(self.x + self.width, self.y + self.height/2, self.direction)
            self.bullets.append(bullet)
            self.remain_bullets -= 1
            return bullet

    def check_bullet_collision(self, opponent):
        if len(opponent.bullets):
            for b in opponent.bullets:
                if self.has_contact(b, self.center, self.width):
                    self.width -= 5
                    self.height -= 5

                    if self.width < 10:
                        self.alive = False

        if len(self.bullets):
            for b in self.bullets:
                if self.has_contact(b, opponent.center, opponent.width):
                    b.inactive()

    @staticmethod
    def has_contact(bullet, center, width):
        distance = math.sqrt(
            ((center[0] - bullet.x) ** 2) +
            ((center[1] - bullet.y) ** 2))
            
        return distance < (width / 2 + bullet.radius + 4)
