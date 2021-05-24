import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

surface = None
width = None
height = None

a = 100
b = 150
c = 0
d = 1
B = b * b
D = d * d


def f(x):
    return x* math.cos(x / 100)


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
    y_min = y_max = y
    for xx in range(xx, width):
        x = x_min + xx * x_range_len / width
        y = f(x)
        if y is not None:
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y
    return y_min, y_max


def draw_point(point):
    surface.set_at(point, RED)


def draw_function(_surface):
    init_draw(_surface)

    x_range = x_min, x_max = -300, 700
    x_range_len = x_max - x_min
    y_range = get_y_range(x_range)
    if y_range is None:
        return
    y_min, y_max = y_range
    y_range_len = max(y_max - y_min, 1)

    pygame.draw.line(surface, BLACK, (-x_min / x_range_len * width, 0), (-x_min / x_range_len * width, height), 1)
    pygame.draw.line(surface, BLACK, (0, height + y_min / y_range_len * height), (width, height + y_min / y_range_len * height), 1)

    last_yy = None
    for xx in range(width):
        x = x_min + xx * x_range_len / width
        y = f(x)
        if y is not None:
            yy =  - (y - y_max) * height / y_range_len
            if last_yy is not None:
                pygame.draw.line(surface, BLACK, (xx - 1, last_yy), (xx, yy), 1)
            last_yy = yy
        else:
            last_yy = None
    
