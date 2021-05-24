import pygame
import math

None_Point = None, None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

surface = None

width = None
height = None

draw_scale = None

x_min, x_max = x_range = None_Point
x_range_len = None
y_min, y_max = x_range = None_Point
y_range_len = None

vertexs = None


def draw_function(surface):
    init_draw(surface)
    init_task()

    pp_1, rad_1, pp_2, rad_2 = find_solution()

    pygame.draw.circle(surface, BLACK, pp_1, rad_1)
    pygame.draw.circle(surface, BLACK, pp_2, rad_2)


def init_draw(surface):
    width = surface.get_width()
    height = surface.get_height()

    draw_scale = 1

    x_range_len = width // draw_scale
    x_min, x_max = x_range = (-x_range_len + 1) // 2, (x_range_len + 1) // 2 - 1
    y_range_len = height // draw_scale
    y_min, y_max = y_range = (-y_range_len + 1) // 2, (y_range_len + 1) // 2 - 1

    globals().update(locals())

    surface.fill(WHITE)


def init_task():
    global vertexs
    vertexs = (
        (-200, -100),
        (-200,  100),
        (   0,  110),
        ( 200,  100),
        ( 200, -100),
    )
    draw_path(vertexs)


def find_solution():
    res_space = 0
    res_pp = None_Point
    res_rad = None
    res_pp_n = None_Point
    res_rad_n = None
    for pp in ppoints():
        p = to_real(pp)
        radius = dist_to_shell(p)
        if radius is not None:
            for pp_n in ppoints(pp):
                p_n = to_real(pp_n)
                radius_n = dist_to_shell(p_n)
                if radius_n is not None:
                    dist_2 = distance_2(p, p_n)
                    if dist_2 > radius * radius:
                        max_radius_n = math.sqrt(dist_2) - radius
                        radius_n = min(radius_n, max_radius_n)
                        space = radius * radius + radius_n * radius_n
                        if space > res_space:
                            res_space = space
                            res_pp = pp
                            res_rad = radius / draw_scale
                            res_pp_n = pp_n
                            res_rad_n = radius_n / draw_scale
    return res_pp, res_rad, res_pp_n, res_rad_n


def ppoints(pp_start=(-1, 0)):
    xx_start, yy_start = pp_start
    for xx in range(xx_start + 1, width, 10):
        yield xx, yy_start
    for yy in range(yy_start + 1, height, 10):
        for xx in range(0, width, 10):
            yield xx, yy


def dist_to_shell(p):
    vs = (v for v in vertexs)
    first_vertex = next(vs)
    last_vertex = first_vertex
    res = float('inf')
    for vertex in vs:
        dist = distance_to_line(p, last_vertex, vertex)
        if dist is None:
            return
        if dist < res:
            res = dist
        last_vertex = vertex
    dist = distance_to_line(p, last_vertex, first_vertex)
    if dist is None:
        return
    if dist < res:
        res = dist
    return res


def distance_2(p_from, p_to):
    x_from, y_from = p_from
    x_to, y_to = p_to
    dx = x_to - x_from
    dy = y_to - y_from
    return dx * dx + dy * dy


def distance_to_line(p, line_from, line_to):
    x, y = p
    x_from, y_from = line_from
    x_to, y_to = line_to
    dx = x_to - x_from
    dy = y_to - y_from
    res = dy * x - dx * y + x_to * y_from - x_from * y_to
    if res < 0:
        return
    return res / math.sqrt(dx * dx + dy * dy)


def draw_line(p_from, p_to):
    pp_from = to_window(p_from)
    pp_to = to_window(p_to)
    pygame.draw.line(surface, BLACK, pp_from, pp_to, 1)


def draw_path(vertexs):
    pps = tuple(map(to_window, vertexs))
    pygame.draw.lines(surface, BLACK, True, pps, 1)


def to_window(p):
    x, y = p
    xx = (x - x_min) * width // x_range_len
    yy = (y_max - y) * height // y_range_len
    return xx, yy


def to_real(pp):
    xx, yy = pp
    x = xx * x_range_len // width + x_min
    y = y_max - yy * y_range_len // height
    return x, y
