import pygame 
from network import Network

from player import Player
from bullet import Bullet


width = 500
height = 500

win = pygame.display.set_mode((width, height))


def redrawWindow(win, *players):
    win.fill((0, 0, 0))
    
    for player in players:
        player.draw(win)

    pygame.display.update()


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

        p.move()
        p.check_bullet_collision(p2.bullets)
        redrawWindow(win, p, p2)
        


if __name__ == '__main__':
    main()