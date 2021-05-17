import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

surface = None


def f(x, y):
    return math.cos(x * y)


def init_draw(_surface: pygame.Surface):
    global surface
    surface = _surface
    surface.fill(WHITE)


def draw_function(_surface):
    init_draw(_surface)
