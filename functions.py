from lib import *


def draw_line_dda(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1

    steps = 0
    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)

    if steps == 0:
        return

    x = x1
    y = y1
    xincr = dx / steps
    yincr = dy / steps
    draw_pixel(screen, (x, y), color)
    for i in range(steps):
        x += xincr
        y += yincr
        draw_pixel(screen, (x, y), color)

    # pygame.draw.line(screen, color, start, end, PIXEL_SIZE)


def draw_line_bresenham(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    p = 2 * dy - dx
    two_dy = 2 * dy
    two_dy_dx = 2 * (dy - dx)

    x = x1
    y = y1
    xEnd = x2

    if x1 > x2:
        x = x2
        y = y2
        xEnd = x1
    
    draw_pixel(screen, (x, y), color)

    while x < xEnd:
        x += 1
        if p < 0:
            p += two_dy
        else:
            y += 1 # if y1 < y2 else -1
            p += two_dy_dx
        draw_pixel(screen, (x, y), color)


def draw_pixel(screen, pos, color):
    x, y = convert_to_grid(pos)
    pygame.draw.rect(
        screen, color, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
    )


def convert_to_grid(pos):
    x, y = pos
    # Converte as coordenadas do mouse para a grade
    return math.floor(x / PIXEL_SIZE), math.floor(y / PIXEL_SIZE)
