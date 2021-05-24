import pygame
import math

None_Pair = None, None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

surface = None

width = None
height = None

density = None

x_min, x_max = x_range = None_Pair
x_range_len = None
y_min, y_max = x_range = None_Pair
y_range_len = None
z_min, z_max = z_range = None_Pair
z_range_len = None

top = None,
bot = None,
new_top = None,
new_bot = None,


def f(x, y):
    return math.cos(x * y)


def draw_function(surface):
    init_draw(surface)

    y = y_max
    xs = line_x_points(2 * width)
    x = next(xs)
    z = f(x, y)
    p_last = x, y, z
    for x in xs:
        z = f(x, y)
        p = x, y, z
        draw_point(p)
        p_last = x, y, z
    update_separator()

    for x in line_x_points(revers=True):
        ys = line_y_points(2 * width)
        y = next(ys)
        z = f(x, y)
        p_last = x, y, z
        for y in ys:
            z = f(x, y)
            p = x, y, z
            draw_point(p)
            p_last = x, y, z
        update_separator()

    refresh_separator()

    x = x_max
    ys = line_y_points(2 * width)
    y = next(ys)
    z = f(x, y)
    p_last = x, y, z
    for y in ys:
        z = f(x, y)
        p = x, y, z
        draw_point(p)
        p_last = x, y, z
    update_separator()

    for y in line_y_points(revers=True):
        xs = line_x_points(2 * width)
        x = next(xs)
        z = f(x, y)
        p_last = x, y, z
        for x in xs:
            z = f(x, y)
            p = x, y, z
            draw_point(p)
            p_last = x, y, z
        update_separator()


def init_draw(surface):
    width = surface.get_width()
    height = surface.get_height()

    density = 25

    x_min, x_max = x_range = -3, 3
    x_range_len = x_max - x_min
    y_min, y_max = y_range = -3, 3
    y_range_len = y_max - y_min

    globals().update(locals())

    z_min, z_max = z_range = get_range()
    z_range_len = z_max - z_min

    globals().update(locals())

    refresh_separator()

    surface.fill(WHITE)


def refresh_separator():
    top = [height for _ in range(width)]
    bot = [0 for _ in range(width)]
    new_top = top.copy()
    new_bot = bot.copy()
    globals().update(locals())


def update_separator():
    global new_top, new_bot
    top = new_top
    bot = new_bot
    new_top = top.copy()
    new_bot = bot.copy()
    globals().update(locals())


def get_range():
    z_min = float('inf')
    z_max = float('-inf')
    for p in plane_points():
        x, y = p
        z = f(x, y)
        if z < z_min:
            z_min = z
        if z > z_max:
            z_max = z
    return z_min, z_max


def plane_points():
    for x in line_x_points():
        for y in line_y_points():
            yield x, y


def line_x_points(density=None, revers=False):
    if density is None:
        density = globals()['density']
    xrange = range(density, -1, -1) if revers else range(density + 1)
    for xi in xrange:
        yield x_min + xi * x_range_len / density


def line_y_points(density=None, revers=False):
    if density is None:
        density = globals()['density']
    yrange = range(density , -1, -1) if revers else range(density + 1)
    for yi in yrange:
        yield y_min + yi * y_range_len / density


def draw_line(p_from, p_to):
    pp_from = to_window(p_from)
    pp_to = to_window(p_to)
    pygame.draw.line(surface, BLACK, pp_from, pp_to, 1)


def draw_point(point):
    global new_top, new_bot
    xx, yy = to_window(point)
    xx, yy = pp = int(xx), int(yy)
    if yy < top[xx]:
        surface.set_at(pp, BLACK)
    elif yy > bot[xx]:
        surface.set_at(pp, BLUE)
    if yy < top[xx]:
        new_top[xx] = yy
    if yy > new_bot[xx]:
        new_bot[xx] = yy


def to_window(p):
    x, y, z = p
    xx = ((x_max - x) + (y - y_min)) * (width - 1) /\
        (x_range_len + y_range_len)
    yy = ((x - x_min) + (y - y_min) + 2 * (z_max - z)) * (height - 1) /\
        (x_range_len + y_range_len + 2 * z_range_len)
    return xx, yy
