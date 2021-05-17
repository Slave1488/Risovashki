import pygame
from task_2 import draw_function

FPS = 60

pygame.init()
surface = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

draw_function(surface)

pygame.display.update()

work = True
while work:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            work = False

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
