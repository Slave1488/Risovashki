from task_1 import get_y_range
import pygame
import math

none_point = None, None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

surface = None
width = None
height = None

draw_scale = 1

x_min, y_min = -300, -200
x_max, y_max = none_point

a = 200
b = 30
c = -100
d = 100
B = b * b
D = d * d

def conv_to_window(point):
    x, y = point
    xx, yy = pp = (x - x_min) / draw_scale,\
                  (y_max - y) / draw_scale
    return pp


center_xx, center_yy = center = none_point


def get_images(ppoint):
    xx, yy = ppoint
    yield xx, yy
    yield xx, 2 * center_yy - yy
    yield 2 * center_xx - xx, yy
    yield 2 * center_xx - xx, 2 * center_yy - yy


def dist_to_f(point):
    x, y = point
    dx, dy = x - a, y - c
    dx_2, dy_2 = dx * dx, dy * dy
    r = D * dx_2 - B * dy_2 - B * D
    return D * dx_2 - B * dy_2 - B * D


def init_draw(_surface: pygame.Surface):
    global surface, width, height, x_max, y_max, center_xx, center_yy, center
    surface = _surface
    surface.fill(WHITE)
    width = surface.get_width()
    height = surface.get_height()
    x_max, y_max = x_min + width * draw_scale,\
                   y_min + height * draw_scale
    center_xx, center_yy = center = conv_to_window((a, c))


def draw_point(ppoint):
    *ppoint, = map(int, ppoint)
    surface.set_at(ppoint, BLACK)


def draw_function(_surface):
    init_draw(_surface)

    last_x, last_y = p = a + b, c
    last_xx, last_yy = pp = conv_to_window(p)
    *_, = map(draw_point, get_images(pp))

    center_xx, center_yy = conv_to_window((a, c))
    bound = center_xx + max(center_xx, width - center_xx), center_yy + max(center_yy, height - center_yy)
    print(bound)
    print(pp)

    while last_xx < bound[0] and last_yy < bound[1]:
        xx, yy = pp = last_xx + 1, last_yy + 1
        x, y = p = xx * draw_scale + x_min,\
                   y_max - yy * draw_scale
        nr = dist_to_f(p)
        if nr < 0:
            p_right = x, last_y
            r_right = dist_to_f(p_right)
            if nr + r_right < 0:
                last_xx, last_yy = pp = xx, last_yy
                last_x, last_y = p = x, last_y
            else:
                last_xx, last_yy = pp = pp
                last_x, last_y = p = p
        else:
            p_down = last_x, y
            r_down = dist_to_f(p_down)
            if nr + r_down < 0:
                last_xx, last_yy = pp = pp
                last_x, last_y = p = p
            else:
                last_xx, last_yy = pp = last_xx, yy
                last_x, last_y = p = last_x, y
        *_, = map(draw_point, get_images(pp))

