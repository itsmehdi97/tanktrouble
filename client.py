import pygame 
from network import Network

from player import Player
from bullet import Bullet
from wall import Wall


width = 500
height = 300

win = pygame.display.set_mode((width, height))


def init_walls():
    return [Wall(pair[0], pair[1]) for pair in [[(2,2),(498,2)], [(498,2),(498,298)], [(2,298),(498,298)], [(2,2),(2,298)]]]

walls = init_walls()

def redrawWindow(win, *players):
    win.fill((0, 0, 0))
    for player in players:
        player.draw(win)
    


def main():
    run = True
    n = Network()
    p = n.getP()
    
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        p2 = n.send(p)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    p.fire()

        p.check_bullet_collision(p2)
        p.rotate()
        p.move(walls)
        redrawWindow(win, p, p2)

        for wall in walls:
            wall.draw(win)
            
        pygame.display.update()
        


if __name__ == '__main__':
    main()