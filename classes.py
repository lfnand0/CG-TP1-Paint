from lib import *


class Paint:
    def __init__(self, master):
        self.master = master
        self.master.title("Paint")

        self.clear_canvas()

        self.position_label = tk.Label(self.master, text="X: 0, Y: 0")
        self.position_label.grid(column=2, columnspan=3, row=3)

        self.structures = []

    def clear_canvas(self):
        self.structures = []
        self.first_click = None
        self.clip_mode = None
        self.draw_mode = "pixel"
        self.color = "#000000"
        self.create_canvas()

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
        )
        self.color_picker.grid(column=4, row=2)

        self.clip_cohen_button = tk.Button(
            self.master,
            text="Clip (Cohen-Sutherland)",
            command=lambda *args: self.set_clip_mode("cohen"),
        )
        self.clip_cohen_button.grid(column=0, row=3)

        self.clip_liang_button = tk.Button(
            self.master,
            text="Clip (Liang-Barsky)",
            command=lambda *args: self.set_clip_mode("liang"),
        )
        self.clip_liang_button.grid(column=1, row=3)

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
        center_x = int(center_x or 0)
        center_y = int(center_y or 0)

        self.create_canvas()
        for structure in self.structures:
            structure.reflect(reflect_on_x, reflect_on_y, center_x, center_y)
            structure.draw(self.canvas)

    def change_color(self):
        color = askcolor()
        if color:
            self.color = color[1]

    def set_draw_mode(self, draw_mode):
        self.clip_mode = None
        self.draw_mode = draw_mode

    def set_clip_mode(self, clip_mode):
        self.clip_mode = clip_mode

    def draw_temporary_pixel(self, click):
        temporary_pixel = Pixel(click, "#C7E1F6")
        temporary_pixel.draw(self.canvas)

    def on_click(self, event):
        click = (event.x, event.y)
        recreate_canvas = False
        if not self.clip_mode:
            structure = None
            if self.draw_mode == "pixel":
                structure = Pixel(click, self.color)
            elif self.first_click is None:
                self.first_click = click
                self.draw_temporary_pixel(click)
            else:
                if self.draw_mode == "line_dda" or self.draw_mode == "line_bres":
                    structure = Line(
                        self.first_click, click, self.color, self.draw_mode
                    )
                elif self.draw_mode == "circle_bres":
                    radius = Circle.distance_between_two_points(self.first_click, click)
                    structure = Circle(self.first_click, radius, self.color)

                self.first_click = None

            if structure:
                self.structures.append(structure)
                print(structure)
                recreate_canvas = True

        else:
            if self.first_click is None:
                self.first_click = click
                self.draw_temporary_pixel(click)
            else:
                if self.clip_mode == "cohen" or self.clip_mode == "liang":
                    self.clip(self.first_click, click, self.clip_mode)

                self.first_click = None
                recreate_canvas = True

        if recreate_canvas:
            self.create_canvas()
            for structure in self.structures:
                structure.draw(self.canvas)

    def clip(self, start, end, algorithm):
        start = Pixel.convert_to_grid(start)
        end = Pixel.convert_to_grid(end)

        new_structures = []
        for structure in self.structures:
            remove_structure = structure.clip(start, end, algorithm)
            if not remove_structure:
                new_structures.append(structure)

        self.structures = new_structures


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

    def clip(self, start, end, algorithm):
        min_x = round(min(start[0], end[0]))
        max_x = round(max(start[0], end[0]))
        min_y = round(min(start[1], end[1]))
        max_y = round(max(start[1], end[1]))

        return self.x < min_x or self.x > max_x or self.y < min_y or self.y > max_y


class Structure:
    def __init__(self, pixels, color):
        self.pixels = pixels
        self.color = color

        self.clipped = False

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

    def clip(self, start, end, algorithm):
        print("aaaa")
        new_pixels = []
        for pixel in self.pixels:
            keep_pixel = pixel.clip(start, end, algorithm)
            if not keep_pixel:
                new_pixels.append(pixel)

        self.clipped = True

        self.pixels = new_pixels

        return not new_pixels


class Line(Structure):
    def __init__(self, start, end, color, line_type="line_dda"):
        self.start = Pixel(start, color)
        self.end = Pixel(end, color)
        self.color = color
        self.pixels = []
        self.line_type = line_type

        self.get_line()

    def __repr__(self):
        return f"Line(start={self.start}, end={self.end}, color={self.color}, line_type={self.line_type})"

    def get_line(self):
        if self.line_type == "line_dda":
            self.get_line_dda()
        elif self.line_type == "line_bres":
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

    def clip(self, start, end, algorithm):
        res = False

        if algorithm == "cohen":
            res = self.clip_cohen(start, end)
        elif algorithm == "liang":
            res = self.clip_liang(start, end)

        return res

    def clip_cohen(self, start, end):
        print("clip cohen line")
        x1, y1 = (self.start.x, self.start.y)
        x2, y2 = (self.end.x, self.end.y)

        print("before: ", x1, y1, x2, y2)

        x_min = round(min(start[0], end[0]))
        x_max = round(max(start[0], end[0]))
        y_min = round(min(start[1], end[1]))
        y_max = round(max(start[1], end[1]))

        print("min: ", x_min, y_min, "max: ", x_max, y_max)

        x_int = y_int = 0

        accept = False
        done = False

        while not done:
            c1 = self.cohen_get_code(x1, y1, x_min, x_max, y_min, y_max)
            c2 = self.cohen_get_code(x2, y2, x_min, x_max, y_min, y_max)

            print(c1, c2)

            if c1 == 0 and c2 == 0:
                accept = True
                done = True
            elif c1 & c2:
                done = True
            else:
                c_out = c1 if c1 else c2

                print(
                    "c_out ", c_out, (c_out & 1), (c_out & 2), (c_out & 4), (c_out & 8)
                )

                # esq
                if c_out & 1:
                    x_int = x_min
                    y_int = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                # dir
                elif c_out & 2:
                    x_int = x_max
                    y_int = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                # inf
                elif c_out & 4:
                    y_int = y_min
                    x_int = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                # sup
                elif c_out & 8:
                    y_int = y_max
                    x_int = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)

                if c_out == c1:
                    x1 = x_int
                    y1 = y_int
                else:
                    x2 = x_int
                    y2 = y_int

        print("after: ", x1, y1, x2, y2)

        if accept:
            self.start = Pixel((round(x1), round(y1)), self.color, False)
            self.end = Pixel((round(x2), round(y2)), self.color, False)
            self.get_line()

        return not accept

    def cohen_get_code(self, x, y, x_min, x_max, y_min, y_max):
        code = 0
        if x < x_min:
            code |= 1
        elif x > x_max:
            code |= 2
        if y < y_min:
            code |= 4
        elif y > y_max:
            code |= 8

        return code

    def clip_liang(self, start, end):
        print("clip liang line")
        x1, y1 = (self.start.x, self.start.y)
        x2, y2 = (self.end.x, self.end.y)

        print("before: ", x1, y1, x2, y2)

        x_min = round(min(start[0], end[0]))
        x_max = round(max(start[0], end[0]))
        y_min = round(min(start[1], end[1]))
        y_max = round(max(start[1], end[1]))

        print("min: ", x_min, y_min, "max: ", x_max, y_max)

        u1 = 0
        u2 = 1
        dx = x2 - x1
        dy = y2 - y1
        u1, u2, accept = self.clip_test(-dx, x1 - x_min, u1, u2)

        if accept:
            u1, u2, accept = self.clip_test(dx, x_max - x1, u1, u2)
            if accept:
                u1, u2, accept = self.clip_test(-dy, y1 - y_min, u1, u2)
                if accept:
                    u1, u2, accept = self.clip_test(dy, y_max - y1, u1, u2)
                    if accept:
                        if u2 < 1:
                            x2 = x1 + u2 * dx
                            y2 = y1 + u2 * dy
                        if u1 > 0:
                            x1 = x1 + u1 * dx
                            y1 = y1 + u1 * dy
                        self.start = Pixel((round(x1), round(y1)), self.color, False)
                        self.end = Pixel((round(x2), round(y2)), self.color, False)
                        self.get_line()

        return not accept

    def clip_test(self, p, q, u1, u2):
        r = 0
        ret_val = True
        if p < 0:
            r = q / p
            if r > u2:
                ret_val = False
            elif r > u1:
                u1 = r
        elif p > 0:
            r = q / p
            if r < u1:
                ret_val = False
            elif r < u2:
                u2 = r
        else:
            if q < 0:
                ret_val = False

        return u1, u2, ret_val


class Circle(Structure):
    def __init__(self, center, radius, color):
        self.center = Pixel(center, color)
        self.radius = radius
        self.color = color
        self.pixels = []

        self.clipped = False

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

    def translate(self, x, y):
        if not self.clipped:
            self.center.translate(x, y)
            self.get_circle()
        else:
            for pixel in self.pixels:
                pixel.translate(x, y)

    def rotate(self, angle, center):
        if not self.clipped:
            self.center.rotate(angle, center)
            self.get_circle()
        else:
            for pixel in self.pixels:
                pixel.rotate(angle, center)

    def scale(self, x, y):
        if not self.clipped:
            self.radius *= x
            self.radius = round(self.radius)
            self.get_circle()
        else:
            for pixel in self.pixels:
                pixel.scale(x, y)

    def reflect(self, reflect_on_x, reflect_on_y, center_x, center_y):
        if not self.clipped:
            self.center.reflect(reflect_on_x, reflect_on_y, center_x, center_y)
            self.get_circle()
        else:
            for pixel in self.pixels:
                pixel.reflect(reflect_on_x, reflect_on_y, center_x, center_y)
