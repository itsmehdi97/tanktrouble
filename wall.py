import pygame


class Wall:
    def __init__(self, start_pos, end_pos, color=(255,255,255), width=3):
        self.start = start_pos
        self.end = end_pos
        self.color = color
        self.width = width

    @property
    def direction(self):
        return WallDirection.VERT if self.start[0] == self.end[0] else WallDirection.HORIZ
    
    def has_collision(self, point, offset=0):
        if self.direction == WallDirection.VERT:
            if point[1] >= self.start[1] and point[1] <= self.end[1]:
                return abs(self.start[0] - point[0]) < offset + self.width/2

        else:
            if point[0] >= self.start[0] and point[0] <= self.end[0]:
                return abs(self.start[1] - point[1]) < offset + self.width/2
        
    def draw(self, win):
        self.rect = pygame.draw.line(win, self.color, self.start, self.end, self.width)


class WallDirection:
    VERT = 'vertival'
    HORIZ = 'horizontal'