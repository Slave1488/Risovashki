import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

surface = None
width = None
height = None

a = 0
b = 250.1
c = 0
d = 1
B = b * b
D = d * d


def f(x):
    dx = x - a
    dy_2 = D * (dx * dx / B - 1)
    if dy_2 < 0:
        return
    dy = math.sqrt(dy_2)
    return c - dy, c + dy


def init_draw(_surface: pygame.Surface):
    global surface, width, height
    surface = _surface
    surface.fill(WHITE)
    width = surface.get_width()
    height = surface.get_height()
    

def get_y_range(x_range):
    x_min, x_max = x_range
    x_range_len = x_max - x_min
    y = None
    xx = 0
    while y is None and xx < width:
        x = x_min + xx * x_range_len / width
        y = f(x)
        xx += 1
    if y is None:
        return
    y_min, y_max = y
    for xx in range(xx, width):
        x = x_min + xx * x_range_len / width
        y = f(x)
        if y is not None:
            _y_min, _y_max = y
            if _y_min < y_min:
                y_min = _y_min
            if _y_max > y_max:
                y_max = _y_max
    return y_min, y_max


def draw_point(point):
    surface.set_at(point, RED)


def draw_function(_surface):
    init_draw(_surface)

    x_range = x_min, x_max = -300, 300
    x_range_len = x_max - x_min
    y_range = get_y_range(x_range)
    if y_range is None:
        return
    y_min, y_max = y_range
    y_range_len = max(y_max - y_min, 1)

    last_yy = None
    for xx in range(width):
        x = x_min + xx * x_range_len / width
        y = f(x)
        if y is not None:
            y_down, y_up = y
            yy_down, yy_up = *yy, = map(lambda y: - (y - y_max) * height / y_range_len, y)
            if last_yy is not None:
                last_yy_down, last_yy_up = last_yy
                pygame.draw.line(surface, BLACK, (xx - 1, last_yy_down), (xx, yy_down), 1)
                pygame.draw.line(surface, BLACK, (xx - 1, last_yy_up), (xx, yy_up), 1)
            else:
                pygame.draw.line(surface, BLACK, (xx, yy_down), (xx, yy_up), 1)
            last_yy = yy
        else:
            if last_yy is not None:
                pygame.draw.line(surface, BLACK, (xx - 1, yy_down), (xx - 1, yy_up), 1)
                last_yy = None
    
