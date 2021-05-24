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

    draw_path(vertexs)

    solve = find_solution()
    res, err = next(solve)
    (p_1, rad_1, p_2, rad_2) = res
    x, y = err
    while x + y > 1:
        print(x, y)

        pp_1 = to_window(p_1)
        pp_2 = to_window(p_2)

        pygame.draw.circle(surface, BLACK, pp_1, rad_1)
        pygame.draw.circle(surface, BLACK, pp_2, rad_2)

        pygame.display.update()

        res, err = next(solve)
        (p_1, rad_1, p_2, rad_2) = res
        print( rad_1 + rad_2)
        x, y = err

    pp_1 = to_window(p_1)
    pp_2 = to_window(p_2)

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


def find_solution():
    area1 = area2 = get_simple_area()
    space = 0
    res_c1, res_r1, res_c2, res_r2 = None, None, None, None
    while True:
        for a1 in split_area(area1):
            c1 = center(a1)
            radius1 = dist_to_shell(c1)
            if radius1 is not None:
                for a2 in split_area(area2):
                    c2 = center(a2)
                    radius2 = dist_to_shell(c2)
                    if radius2 is not None:
                        dist_2 = distance_2(c1, c2)
                        if dist_2 > radius1 * radius1:
                            radius2_max = math.sqrt(dist_2) - radius1
                            radius2 = min(radius2, radius2_max)
                            space_n = radius1 * radius1 + radius2 * radius2
                            if space_n > space:
                                res_c1, res_r1, res_c2, res_r2 =\
                                    c1 ,radius1, c2, radius2
                                space = space_n
        yield (res_c1, res_r1, res_c2, res_r2), calc_err(a1)
        area1 = new_area(c1, area1[1], area2[2])
        area2 = new_area(c2, area2[1], area2[2])


def get_simple_area():
    l, r = x_max, x_min
    d, u = y_max, y_min
    for v in vertexs:
        x, y = v
        if x < l:
            l = x
        if x > r:
            r = x
        if y < d:
            d = y
        if y > u:
            u = y
    return (l, u), (r - l, 0), (0, d - u)


def new_area(center, v1, v2, mult=2/3):
    x, y = center
    x1, y1 = v1
    x1 *= mult
    y1 *= mult
    v1 = x1, y1
    x2, y2 = v2
    x2 *= mult
    y2 *= mult
    v2 = x2, y2
    start = x - x1 / 2 - x2 / 2, y - y1 / 2 - y2 / 2
    return start, v1, v2


def center(area):
    start, v1, v2 = area
    x, y = start
    x1, y1 = v1
    x2, y2 = v2
    return x + x1 / 2 + x2 / 2, y + y1 / 2 + y2 / 2


def split_area(area, quality=30):
    start, v1, v2 = area
    x, y = start
    x1, y1 = v1
    x2, y2 = v2
    x1_n, y1_n = v1_n = x1 / quality, y1 / quality
    x2_n, y2_n = v2_n = x2 / quality, y2 / quality
    for c1 in range(quality):
        for c2 in range(quality):
            start_n = x + c1 * x1_n + c2 * x2_n,\
                      y + c1 * y1_n + c2 * y2_n
            yield start_n, v1_n, v2_n


def calc_err(area):
    _, v1, v2 = area
    x1, y1 = v1
    x2, y2 = v2
    return x1 + x2, y1 + y2



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
    xx = (x - x_min) * width / x_range_len
    yy = (y_max - y) * height / y_range_len
    return xx, yy


def to_real(pp):
    xx, yy = pp
    x = xx * x_range_len // width + x_min
    y = y_max - yy * y_range_len // height
    return x, y
