from lib import *


class Paint:
    def __init__(self, master):
        self.master = master
        self.master.title("Paint")

        self.color = "#000000"
        self.first_click = None
        self.draw_mode = "pixel"

        self.create_canvas()

        self.position_label = tk.Label(self.master, text="X: 0, Y: 0")
        self.position_label.grid(column=0, columnspan=5, row=3)

        self.structures = []

    def create_canvas(self):
        self.canvas = tk.Canvas(
            self.master, width=REAL_WIDTH, height=REAL_HEIGHT, bg="white"
        )
        self.canvas.grid(column=0, columnspan=5, row=0)

        self.dda_button = tk.Button(
            self.master,
            text="Draw Line (DDA)",
            command=lambda *args: self.set_draw_mode("line_dda"),
        )
        self.dda_button.grid(column=0, row=1)

        self.bres_button = tk.Button(
            self.master,
            text="Draw Line (Bresenham)",
            command=lambda *args: self.set_draw_mode("line_bres"),
        )
        self.bres_button.grid(column=1, row=1)

        self.circle_button = tk.Button(
            self.master,
            text="Draw Circle (Bresenham)",
            command=lambda *args: self.set_draw_mode("circle_bres"),
        )
        self.circle_button.grid(column=2, row=1)

        self.pixel_button = tk.Button(
            self.master,
            text="Draw Pixel",
            command=lambda *args: self.set_draw_mode("pixel"),
        )
        self.pixel_button.grid(column=3, row=1)

        self.clear_button = tk.Button(
            self.master,
            text="Clear",
            command=lambda *args: self.clear_canvas(),
        )
        self.clear_button.grid(column=4, row=1)

        ##### TRANSFORMAÇÕES #####
        self.translate_button = tk.Button(
            self.master,
            text="Translate",
            command=lambda *args: self.create_translate_dialog(),
        )

        self.translate_button.grid(column=0, row=2)

        self.rotation_button = tk.Button(
            self.master,
            text="Rotate",
            command=lambda *args: self.create_rotate_dialog(),
        )
        self.rotation_button.grid(column=1, row=2)

        self.scale_button = tk.Button(
            self.master,
            text="Scale",
            command=lambda *args: self.create_scale_dialog(),
        )
        self.scale_button.grid(column=2, row=2)

        self.reflect_button = tk.Button(
            self.master,
            text="Reflect",
            command=lambda *args: self.create_reflect_dialog(),
        )
        self.reflect_button.grid(column=3, row=2)

        self.color_picker = tk.Button(
            text="Color Picker", command=lambda *args: self.change_color()
        ).grid(column=4, row=2)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.display_current_position)

    def display_current_position(self, event):
        x, y = Pixel.convert_to_grid((event.x, event.y))
        self.position_label.config(text=f"X: {x}, Y: {y}")

    def create_translate_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.geometry("200x100")
        dialog.title("Translate")

        x_label = tk.Label(dialog, text="X:")
        x_label.grid(column=0, row=0)

        x_entry = tk.Entry(dialog)
        x_entry.grid(column=1, row=0)

        y_label = tk.Label(dialog, text="Y:")
        y_label.grid(column=0, row=1)

        y_entry = tk.Entry(dialog)
        y_entry.grid(column=1, row=1)

        confirm_button = tk.Button(
            dialog,
            text="Confirm",
            command=lambda *args: self.translate_structures(
                (x_entry.get()), (y_entry.get())
            ),
        )
        confirm_button.grid(column=0, columnspan=2, row=2)

    def translate_structures(self, x, y):
        x = int(x or 0)
        y = int(y or 0)

        self.create_canvas()
        for structure in self.structures:
            structure.translate(int(x), int(y))
            structure.draw(self.canvas)

    def create_rotate_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.geometry("200x100")
        dialog.title("Rotate")

        angle_label = tk.Label(dialog, text="Angle:")
        angle_label.grid(column=0, row=0)

        angle_entry = tk.Entry(dialog)
        angle_entry.grid(column=1, row=0)

        center_x_label = tk.Label(dialog, text="Center X:")
        center_x_label.grid(column=0, row=1)

        center_x_entry = tk.Entry(dialog)
        center_x_entry.grid(column=1, row=1)

        center_y_label = tk.Label(dialog, text="Center Y:")
        center_y_label.grid(column=0, row=2)

        center_y_entry = tk.Entry(dialog)
        center_y_entry.grid(column=1, row=2)

        confirm_button = tk.Button(
            dialog,
            text="Confirm",
            command=lambda *args: self.rotate_structures(
                angle_entry.get(),
                center_x_entry.get(),
                center_y_entry.get(),
            ),
        )
        confirm_button.grid(column=0, columnspan=2, row=3)

    def rotate_structures(self, angle, center_x, center_y):
        angle = int(angle or 0)
        center_x = int(center_x or 0)
        center_y = int(center_y or 0)

        self.create_canvas()
        for structure in self.structures:
            structure.rotate(angle, (center_x, center_y))
            structure.draw(self.canvas)

    def create_scale_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.geometry("200x100")
        dialog.title("Scale")

        info_text = tk.Label(dialog, text="Para círculos, preencha apenas o X")
        info_text.grid(column=0, columnspan=2, row=0)

        x_label = tk.Label(dialog, text="X:")
        x_label.grid(column=0, row=1)

        x_entry = tk.Entry(dialog)
        x_entry.grid(column=1, row=1)

        y_label = tk.Label(dialog, text="Y:")
        y_label.grid(column=0, row=2)

        y_entry = tk.Entry(dialog)
        y_entry.grid(column=1, row=2)

        confirm_button = tk.Button(
            dialog,
            text="Confirm",
            command=lambda *args: self.scale_structures(x_entry.get(), y_entry.get()),
        )
        confirm_button.grid(column=0, columnspan=2, row=3)

    def scale_structures(self, scale_x, scale_y):
        # setando pra 1 caso nada seja preenchido
        scale_x = float(scale_x or 1)
        scale_y = float(scale_y or 1)

        self.create_canvas()
        for structure in self.structures:
            structure.scale(scale_x, scale_y)
            structure.draw(self.canvas)

    def create_reflect_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.geometry("250x125")
        dialog.title("Reflect")

        reflect_on_x = tk.BooleanVar()
        x_switch = tk.Checkbutton(dialog, text="Reflect on X axis", var=reflect_on_x)
        x_switch.grid(column=0, row=0)

        reflect_on_y = tk.BooleanVar()
        y_switch = tk.Checkbutton(dialog, text="Reflect on Y axis", var=reflect_on_y)
        y_switch.grid(column=0, row=1)

        center_x_label = tk.Label(dialog, text="Center X:")
        center_x_label.grid(column=0, row=2)

        center_x_entry = tk.Entry(dialog)
        center_x_entry.grid(column=1, row=2)

        center_y_label = tk.Label(dialog, text="Center Y:")
        center_y_label.grid(column=0, row=3)

        center_y_entry = tk.Entry(dialog)
        center_y_entry.grid(column=1, row=3)

        confirm_button = tk.Button(
            dialog,
            text="Confirm",
            command=lambda *args: self.reflect_structures(
                reflect_on_x.get(),
                reflect_on_y.get(),
                center_x_entry.get(),
                center_y_entry.get(),
            ),
        )
        confirm_button.grid(column=0, columnspan=2, row=4)

    def reflect_structures(self, reflect_on_x, reflect_on_y, center_x, center_y):
        self.create_canvas()

        center_x = int(center_x or 0)
        center_y = int(center_x or 0)

        for structure in self.structures:
            structure.reflect(reflect_on_x, reflect_on_y, center_x, center_y)
            structure.draw(self.canvas)

    def change_color(self):
        color = askcolor()
        if color:
            self.color = color[1]

    def clear_canvas(self):
        self.structures = []
        self.first_click = None
        self.draw_mode = "pixel"
        self.create_canvas()

    def set_draw_mode(self, draw_mode):
        self.draw_mode = draw_mode

    def on_click(self, event):

        click = (event.x, event.y)
        if self.draw_mode == "pixel":
            pixel = Pixel(click, self.color)
            self.structures.append(pixel)
            print(pixel)
        else:
            if self.first_click is None:
                self.first_click = click
            else:
                if self.draw_mode == "line_dda":
                    line = Line(self.first_click, click, self.color, "dda")
                    line.get_line()
                    self.structures.append(line)
                    print(line)
                elif self.draw_mode == "line_bres":
                    line = Line(self.first_click, click, self.color, "bres")
                    line.get_line()
                    self.structures.append(line)
                    print(line)
                elif self.draw_mode == "circle_bres":
                    radius = Circle.distance_between_two_points(self.first_click, click)
                    circle = Circle(self.first_click, radius, self.color)
                    self.structures.append(circle)
                    print(circle)
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
        
    def __repr__(self):
        return f"Pixel({self.x}, {self.y}, {self.color})"

    def draw(self, canvas):
        canvas.create_rectangle(
            self.x * PIXEL_SIZE,
            self.y * PIXEL_SIZE,
            (self.x + 1) * PIXEL_SIZE,
            (self.y + 1) * PIXEL_SIZE,
            fill=(self.color or "#000000"),
            outline="",
        )

    def convert_to_grid(pos):
        x, y = pos
        return x // PIXEL_SIZE, y // PIXEL_SIZE

    def translate(self, x, y):
        self.x += x
        self.y += y

    def rotate(self, angle, center):
        cx = center[0]
        cy = center[1]

        self.translate(-1 * cx, -1 * cy)

        x = round(
            self.x * math.cos(math.radians(angle))
            - self.y * math.sin(math.radians(angle))
        )
        y = round(
            self.x * math.sin(math.radians(angle))
            + self.y * math.cos(math.radians(angle))
        )

        self.x = x
        self.y = y

        self.translate(cx, cy)

    def scale(self, x, y):
        self.x = round(self.x * x)
        self.y = round(self.y * y)

    def reflect(self, reflect_on_x, reflect_on_y, center_x, center_y):
        self.translate(-1 * center_x, -1 * center_y)

        if reflect_on_x:
            self.y *= -1
        if reflect_on_y:
            self.x *= -1

        self.translate(center_x, center_y)


class Structure:
    def __init__(self, pixels, color):
        self.pixels = pixels
        self.color = color

    def __repr__(self):
        return f"Structure(pixels=[{self.pixels}], color={self.color})"

    def add_point(self, point):
        self.pixels.append(Pixel(point, self.color, False))

    def clear_pixels(self):
        self.pixels = []

    def draw(self, canvas):
        for pixel in self.pixels:
            pixel.draw(canvas)

    def translate(self, x, y):
        for pixel in self.pixels:
            pixel.translate(x, y)

    def rotate(self, angle, center):
        for pixel in self.pixels:
            pixel.rotate(angle, center)

    def scale(self, x, y):
        for pixel in self.pixels:
            pixel.scale(x, y)

    def reflect(self, reflect_on_x, reflect_on_y, center_x, center_y):
        for pixel in self.pixels:
            self.pixel.translate(-1 * center_x, -1 * center_y)

            if reflect_on_x:
                pixel.y *= -1
            if reflect_on_y:
                pixel.x *= -1

            self.pixel.translate(center_x, center_y)


class Line(Structure):
    def __init__(self, start, end, color, line_type="dda"):
        self.start = Pixel(start, color)
        self.end = Pixel(end, color)
        self.color = color
        self.pixels = []
        self.line_type = line_type
        
    def __repr__(self):
        return f"Line(start={self.start}, end={self.end}, color={self.color}, line_type={self.line_type})"

    def get_line(self):
        if self.line_type == "dda":
            self.get_line_dda()
        elif self.line_type == "bres":
            self.get_line_bresenham()

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
        self.add_point((x, y))
        for i in range(steps):
            x += xincr
            y += yincr
            self.add_point((round(x), round(y)))

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

    def translate(self, x, y):
        self.start.translate(x, y)
        self.end.translate(x, y)
        self.get_line()

    def rotate(self, angle, center):
        self.start.rotate(angle, center)
        self.end.rotate(angle, center)
        self.get_line()

    def scale(self, x, y):
        self.end.translate(-1 * self.start.x, -1 * self.start.y)
        self.end.scale(x, y)
        self.end = Pixel(
            (self.end.x + self.start.x, self.end.y + self.start.y), self.color, False
        )

        self.get_line()

    def reflect(self, reflect_on_x, reflect_on_y, center_x, center_y):
        self.start.reflect(reflect_on_x, reflect_on_y, center_x, center_y)
        self.end.reflect(reflect_on_x, reflect_on_y, center_x, center_y)

        self.get_line()


class Circle(Structure):
    def __init__(self, center, radius, color):
        self.center = Pixel(center, color)
        self.radius = radius
        self.color = color
        self.pixels = []

        self.get_circle()

    def __repr__(self):
        return f"Circle(center={self.center}, radius={self.radius}, color={self.color})"

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

    def rotate(self, angle, center):
        self.center.rotate(angle, center)
        self.get_circle()

    def scale(self, x, y):
        self.radius *= x
        self.radius = round(self.radius)
        self.get_circle()

    def reflect(self, reflect_on_x, reflect_on_y, center_x, center_y):
        self.center.reflect(reflect_on_x, reflect_on_y, center_x, center_y)
        self.get_circle()
