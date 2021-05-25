import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

surface = None
width = None
height = None


def f(x):
    return x* math.cos(x * x)


def init_draw(_surface: pygame.Surface):
    global surface, width, height
    surface = _surface
    width = surface.get_width()
    height = surface.get_height()

    surface.fill(WHITE)


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
    return y_min, y_max + 1


def draw_point(point):
    surface.set_at(point, RED)


def draw_function(_surface):
    init_draw(_surface)

    x_range = x_min, x_max = 1, 6
    x_range_len = x_max - x_min
    y_range = get_y_range(x_range)
    if y_range is None:
        return
    y_min, y_max = y_range
    y_range_len = y_max - y_min
    globals().update(locals())

    pygame.draw.line(surface, BLACK, to_window((x_min, 0)), to_window((x_max, 0)), 1)
    pygame.draw.line(surface, BLACK, to_window((0, y_min)), to_window((0, y_max)), 1)

    last_yy = None
    for xx in range(width):
        x = xx * x_range_len / (width - 1) + x_min
        y = f(x)
        if y is not None:
            yy = (y_max - y) * (height - 1) / y_range_len
            if last_yy is not None:
                pygame.draw.line(surface, BLACK, (xx - 1, last_yy), (xx, yy), 1)
            last_yy = yy
        else:
            last_yy = None


def to_window(p):
    x, y = p
    xx = (x - x_min) * (width - 1) / x_range_len
    yy = (y_max - y) * (height - 1) / y_range_len
    return xx, yy


def to_real(pp):
    xx, yy = pp
    x = xx * x_range_len / (width - 1) + x_min
    y = y_max - yy * y_range_len / (height - 1)
    return x, y
