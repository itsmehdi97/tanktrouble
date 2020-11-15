import time
import math

import pygame

from bullet import Bullet


class Player:
    def __init__(self, x, y, width, height, color, pipe_length=11,pipe_width=2):
        self.alive = True

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 3
        self.rotation_vel = 2.8
        self.rect = (x, y, width, height)

        self.direction = 0 # direction in degrees
        
        self.remain_bullets = 6
        self.bullets = []
        self.pipe_length = 13
        self.pipe_width = 2

    @property
    def fire_spotx(self):
        return self.center[0] + math.cos(math.radians(self.direction)) * self.pipe_length

    @property
    def fire_spoty(self):
        return self.center[1] + math.sin(math.radians(self.direction)) * self.pipe_length

    @property
    def center(self):
        return (self.x + self.width/2, self.y + self.height/2)    

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def move_bullets(self, walls):
        for b in self.bullets:
            b.move(walls)

    def validate_bullets(self):
        for b in self.bullets:
            if time.time() - b.fired_at >= 5:
                b.inactive()
    
    def draw_pipe(self,win):
        pygame.draw.line(win, (255,255,255), self.center, (self.fire_spotx,self.fire_spoty), self.pipe_width)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        self.draw_pipe(win)
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
    
    def rotate(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction  = (self.direction - self.rotation_vel) % 360

        if keys[pygame.K_RIGHT]:
            self.direction  = (self.direction + self.rotation_vel) % 360

    def is_move_valid(self, x, y, walls):
        corners = [
            (x,y), (x+self.width,y), (x,y+self.height), (x+self.width,y+self.height)
        ]
        for corner in corners:
            for wall in walls:
                if wall.has_collision(corner, self.vel/2):
                   return False
        
        return True


    def move(self, walls):
        keys = pygame.key.get_pressed()
        
        new_x = self.x
        new_y = self.y
        key_pressed = False
        if keys[pygame.K_UP]:
            key_pressed = True
            new_y = self.y + (self.vel * math.sin(math.radians(self.direction)))
            new_x = self.x + (self.vel * math.cos(math.radians(self.direction)))

        
        if keys[pygame.K_DOWN]:
            key_pressed = True
            new_y = self.y - (self.vel * math.sin(math.radians(self.direction)))
            new_x = self.x - (self.vel * math.cos(math.radians(self.direction)))

        if key_pressed and self.is_move_valid(new_x, new_y, walls):
            self.x = new_x
            self.y = new_y
            self.update()

        self.move_bullets(walls)

    def fire(self):
        if self.remain_bullets > 0:
            bullet = Bullet(self.fire_spotx, self.fire_spoty, self.direction)
            self.bullets.append(bullet)
            self.remain_bullets -= 1
            return bullet

    def check_bullet_collision(self, opponent):
        if len(opponent.bullets):
            for b in opponent.bullets:
                if self.has_contact(b, self.center, self.width):
                    self.punish()

        if len(self.bullets):
            for b in self.bullets:
                if self.has_contact(b, opponent.center, opponent.width):
                    b.inactive()
                
                if self.has_contact(b, self.center, self.width) and b.hit_wall:
                    b.inactive()
                    self.punish()

    def punish(self):
        self.width -= 2
        self.height -= 2

        if self.width < 10:
            self.alive = False

    @staticmethod
    def has_contact(bullet, center, width):
        distance = math.sqrt(
            ((center[0] - bullet.x) ** 2) +
            ((center[1] - bullet.y) ** 2))
             
        return distance < (width / 2 + bullet.radius + 4)
