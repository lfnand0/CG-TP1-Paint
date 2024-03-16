from lib import *


class Paint:
    def __init__(self, master):
        self.master = master
        self.master.title("Paint")

        self.first_click = None
        self.draw_mode = "pixel"

        self.create_canvas()

        self.structures = []

    def create_canvas(self):
        print("aaa")
        self.canvas = Canvas(
            self.master, width=REAL_WIDTH, height=REAL_HEIGHT, bg="white"
        )
        self.canvas.grid(column=0, columnspan=6, row=0)

        self.button1 = tk.Button(
            self.master,
            text="Draw Line (DDA)",
            command=lambda *args: self.set_draw_mode("line_dda"),
        )
        self.button1.grid(column=0, row=1)

        self.button2 = tk.Button(
            self.master,
            text="Draw Line (Bresenham)",
            command=lambda *args: self.set_draw_mode("line_bres"),
        )
        self.button2.grid(column=1, row=1)

        self.button3 = tk.Button(
            self.master,
            text="Draw Circle (Bresenham)",
            command=lambda *args: self.set_draw_mode("circle_bres"),
        )
        self.button3.grid(column=2, row=1)

        self.button4 = tk.Button(
            self.master,
            text="Draw Pixel",
            command=lambda *args: self.set_draw_mode("pixel"),
        )
        self.button4.grid(column=3, row=1)

        self.button5 = tk.Button(
            self.master,
            text="Transform",
            command=lambda *args: self.set_draw_mode("pixel"),
        )
        self.button5.grid(column=4, row=1)

        self.button6 = tk.Button(
            self.master,
            text="Clear",
            command=lambda *args: self.clear_canvas(),
        )
        self.button6.grid(column=5, row=1)

        self.canvas.bind("<Button-1>", self.on_click)

    def clear_canvas(self):
        self.structures = []
        self.first_click = None
        self.draw_mode = "pixel"
        self.create_canvas()

    def set_draw_mode(self, draw_mode):
        print(draw_mode)
        self.draw_mode = draw_mode

    def on_click(self, event):
        # self.canvas.delete("all")

        click = (event.x, event.y)
        print(event.x, event.y, self.draw_mode)
        if self.draw_mode == "pixel":
            # draw_pixel(self.canvas, click, (0, 0, 0))
            self.structures.append(Pixel(click, (0, 0, 0)))
        else:
            if self.first_click is None:
                self.first_click = click
            else:
                if self.draw_mode == "line_dda":
                    line = Line(self.first_click, click, (0, 0, 0))
                    line.get_line_dda()
                    self.structures.append(line)
                    # draw_line_dda(self.canvas, self.first_click, click, (0, 0, 0))
                elif self.draw_mode == "line_bres":
                    line = Line(self.first_click, click, (0, 0, 0))
                    line.get_line_bresenham()
                    self.structures.append(line)
                    # draw_line_bresenham(self.canvas, self.first_click, click, (0, 0, 0))
                elif self.draw_mode == "circle_bres":
                    radius = Circle.distance_between_two_points(self.first_click, click)
                    print(radius)
                    circle = Circle(self.first_click, radius, (0, 0, 0))
                    self.structures.append(circle)
                self.first_click = None

        self.create_canvas()
        for structure in self.structures:
            structure.draw(self.canvas)


class Pixel:
    def __init__(self, point, color, convert=True):
        if convert:
            self.x, self.y = Pixel.convert_to_grid(point)
        else:
            self.x, self.y = point

        self.color = color

    def draw(self, canvas):
        print("draw - x:", self.x, ", y:", self.y)
        canvas.create_rectangle(
            self.x * PIXEL_SIZE,
            self.y * PIXEL_SIZE,
            (self.x + 1) * PIXEL_SIZE,
            (self.y + 1) * PIXEL_SIZE,
            fill="#000000",
            outline="",
        )

    def convert_to_grid(pos):
        x, y = pos
        # Converte as coordenadas do mouse para a grade
        return x // PIXEL_SIZE, y // PIXEL_SIZE


class Structure:
    def __init__(self, pixels, color):
        self.pixels = pixels
        self.color = color

    def add_point(self, point):
        self.pixels.append(Pixel(point, self.color, False))

    def clear_pixels(self):
        self.pixels = []

    def draw(self, canvas):
        for pixel in self.pixels:
            pixel.draw(canvas)


class Line(Structure):
    def __init__(self, start, end, color):
        self.start = Pixel(start, color)
        self.end = Pixel(end, color)
        self.color = color
        self.pixels = []

    def get_line_dda(self):
        self.clear_pixels()
        x1, y1 = (self.start.x, self.start.y)
        x2, y2 = (self.end.x, self.end.y)

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
        # draw_pixel(screen, (x, y), color)
        self.add_point((x, y))
        for i in range(steps):
            x += xincr
            y += yincr
            self.add_point((round(x), round(y)))
            # draw_pixel(screen, (round(x), round(y)), self.color)

    def get_line_bresenham(self):
        self.clear_pixels()
        x1, y1 = (self.start.x, self.start.y)
        x2, y2 = (self.end.x, self.end.y)

        dx = x2 - x1
        dy = y2 - y1
        const1 = const2 = p = incrx = incry = 0
        if dx >= 0:
            incrx = 1
        else:
            incrx = -1
            dx = -dx

        if dy >= 0:
            incry = 1
        else:
            incry = -1
            dy = -dy

        x = x1
        y = y1

        # draw_pixel(screen, (x, y), color)
        self.add_point((x, y))
        if dy < dx:
            p = 2 * dy - dx
            const1 = 2 * dy
            const2 = 2 * (dy - dx)
            for i in range(dx):
                x = x + incrx
                if p < 0:
                    p = p + const1
                else:
                    y = y + incry
                    p = p + const2
                self.add_point((x, y))
        else:
            p = 2 * dx - dy
            const1 = 2 * dx
            const2 = 2 * (dx - dy)
            for i in range(dy):
                y = y + incry
                if p < 0:
                    p = p + const1
                else:
                    x = x + incrx
                    p = p + const2
                self.add_point((x, y))


class Circle(Structure):
    def __init__(self, center, radius, color):
        self.center = Pixel(center, color)
        self.radius = radius
        self.color = color
        self.pixels = []

        print(self.center.x, self.center.y, radius)

        self.get_circle()
        print([(p.x, p.y) for p in self.pixels])

    def distance_between_two_points(start, end):
        x1, y1 = Pixel.convert_to_grid(start)
        x2, y2 = Pixel.convert_to_grid(end)
        return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

    def get_circle(self):
        self.clear_pixels()
        xc = self.center.x
        yc = self.center.y
        r = self.radius

        x = 0
        y = r
        p = 3 - 2 * r

        self.plot_points(xc, yc, x, y)

        while x < y:
            if p < 0:
                p = p + 4 * x + 6
            else:
                p = p + 4 * (x - y) + 10
                y = y - 1
            x = x + 1
            self.plot_points(xc, yc, x, y)

    def plot_points(self, xc, yc, x, y):
        self.add_point((x + xc, y + yc))
        self.add_point((y + xc, x + yc))
        self.add_point((-x + xc, y + yc))
        self.add_point((-y + xc, x + yc))
        self.add_point((x + xc, -y + yc))
        self.add_point((y + xc, -x + yc))
        self.add_point((-x + xc, -y + yc))
        self.add_point((-y + xc, -x + yc))
