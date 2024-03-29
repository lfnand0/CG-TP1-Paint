from lib import *


class Paint:
    """
    Classe principal com a interface do projeto.

    Atributos:
        master (Tk): O widget raíz da aplicação (classe Tk do Tkinter).
        position_label (Label): Rótulo com a posição do cursor, apresentada no canto inferior direito e atualizada dinamicamente.
        structures (list): Uma lista com todas as estruturas desenhadas no canvas.
        first_click (tuple): A posição do primeiro click do usuário (usado para funcionalidades que usam dois clicks, como a criação de linhas, círculos e recortes).
        clip_mode (str): O modo de recorte atual (Cohen-Sutherland ou Liang-Barsky).
        draw_mode (str): O modo de desenho atual (pixel, linha DDA, linha Bresenham, círculo Bresenham).
        color (str): A cor atual selecionada para desenho (pode ser alterada pelo usuário com o color picker).
        canvas (Canvas): Basicamente onde tudo acontece.

    Métodos:
        __init__(self, master): Inicializa a interface gráfica do Paint.
        clear_canvas(self): Limpa o canvas e reseta os atributos.
        create_canvas(self): Cria o canvas, junto com os botões da aplicação e os valores padrões para cor e afins.
        display_current_position(self, event): Atualiza o rótulo position_label com as coordenadas do cursor.
        change_color(self): Abre um seletor de cores para alterar a cor de desenho.
        set_draw_mode(self, draw_mode): Define o modo de desenho atual.
        set_clip_mode(self, clip_mode): Define o modo de recorte atual.
        draw_temporary_pixel(self, click): Desenha um pixel temporário (pontinho azul que aparece para as funcionalidades com dois clicks).
        on_click(self, event): Lida com os clicks do usuário no canvas, executando a funcionalidade selecionada atualmente (draw_mode ou clip_mode).
        clip(self, start, end, algorithm): Realiza o recorte das estruturas em uma área selecionada.
        create_translate_dialog(self): Cria a janela da translação.
        translate_structures(self, x, y): Translada todas as estruturas desenhadas. Executado no confirmar da janela de translação (assim como as outras transformações descritas a seguir).
        create_rotate_dialog(self): Cria a janela da rotação.
        rotate_structures(self, angle, center_x, center_y): Rotaciona todas as estruturas desenhadas.
        create_scale_dialog(self): Cria a janela da escala.
        scale_structures(self, scale_x, scale_y): Escala todas as estruturas desenhadas.
        create_reflect_dialog(self): Cria a janela de reflexão.
        reflect_structures(self, reflect_on_x, reflect_on_y, center_x, center_y): Reflete as estruturas desenhadas.
    """

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
    """
    Representa um único pixel na tela.

    Args:
        point (tuple): As coordenadas x e y do pixel.
        color (str): A cor do pixel.
        convert (bool, optional): Indica se as coordenadas do pixel devem ser convertidas para
            coordenadas da grade. Se True, o método `convert_to_grid` será chamado para converter
            as coordenadas para coordenadas da grade. Caso contrário, as coordenadas serão usadas
            diretamente. O padrão é True.

    Atributos:
        x (int): Coordenada x do pixel.
        y (int): Coordenada y do pixel.
        color (str): Cor do pixel.

    Métodos:
        __init__(self, point, color, convert=True): Inicializa um novo pixel.
        draw(self, canvas): Desenha o pixel no canvas. Esse método é amplamente utilizado por
                outras classes (por exemplo, o método `draw` da classe `Line` chama o método
                `draw` da classe `Pixel` para cada pixel na linha).
        convert_to_grid(pos): Método estático para converter as coordenadas reais da tela para
                coordenadas da grade (valores especificados no arquivo `constants.py`).
        translate(self, x, y): Translada o pixel adicionando os valores de x e y às suas
                coordenadas.
        rotate(self, angle, center): Rotaciona o pixel em torno de um ponto central.
        scale(self, x, y): Escala a posição do pixel (multiplicação simples dos valores passados às
                coordenadas).
        reflect(self, reflect_on_x, reflect_on_y, center_x, center_y): Reflete o pixel em torno
                do(s) eixo(s) especificado(s). Os valores de center_x e center_y representam o ponto
                de origem do(s) eixo(s).
        clip(self, start, end, algorithm): Realiza o recorte verificando se o pixel está dentro da
                área especificada (Point Clipping).
    """

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

    @staticmethod
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
    """
    Interface para as outras estruturas (linhas e círculos).

    Args:
        pixels (list): Lista de pixels que compõem a estrutura.
        color (str): Cor da estrutura.

    Atributos:
        pixels (list): Lista de pixels que compõem a estrutura.
        color (str): Cor da estrutura.
        clipped (bool): Indica se a estrutura foi recortada ou não.

    Métodos:
        __init__(self, pixels, color): Cria uma nova estrutura recebendo uma lista de pixels
                e uma cor.
        add_point(self, point): Adiciona um novo ponto à estrutura.
        clear_pixels(self): Remove o array de pixels da estrutura.
        draw(self, canvas): Desenha a estrutura no canvas.
        translate(self, x, y): Translada a estrutura em x e y.
        rotate(self, angle, center): Rotaciona a estrutura em torno de um ponto central.
        scale(self, x, y): Escala a estrutura horizontalmente e verticalmente.
        reflect(self, reflect_on_x, reflect_on_y, center_x, center_y): Reflete a estrutura em
                torno do eixo especificado.
        clip(self, start, end, algorithm): Realiza o recorte da estrutura de acordo com a área
                delimitada (também Point Clipping).
    """

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
        new_pixels = []
        for pixel in self.pixels:
            remove_pixel = pixel.clip(start, end, algorithm)
            if not remove_pixel:
                new_pixels.append(pixel)

        self.clipped = True

        self.pixels = new_pixels

        return not new_pixels


class Line(Structure):
    """
    Representa uma linha desenhada entre dois pontos (ou feita com DDA, ou com Bresenham).

    Args:
        start (tuple): As coordenadas (x, y) do ponto inicial da linha.
        end (tuple): As coordenadas (x, y) do ponto final da linha.
        color (str): A cor da linha.
        line_type (str, optional): O algoritmo utilizado para desenhar a linha. Por padrão é
                selecionado o DDA.

    Atributos:
        start: Posição do início da linha (objeto Pixel).
        end: Posição do final da linha.
        line_type: Algoritmo utilizado para desenhar a linha (DDA ou Bresenham).

    Métodos:
        __init__(self, start, end, color, line_type="line_dda"): Inicializa uma nova linha com um
                ponto inicial e final, cor e tipo da linha.
        get_line(self): Encontra os pixels que formam a linha (de acordo com o atributo line_type).
        get_line_dda(self): Utiliza o algoritmo DDA para traçar a linha.
        get_line_bresenham(self): Utiliza o algoritmo de Bresenham para traçar a linha.
        translate(self, x, y): Translada os pontos de início e fim da linha, e depois gera a linha
                novamente.
        rotate(self, angle, center): Rotaciona a linha em torno de um ponto central (rotaciona ambos
                os pontos e gera de novo a linha).
        scale(self, x, y): Escala a linha horizontalmente e verticalmente (simula a translação da
                linha para a origem diminuindo as coordenadas do ponto inicial no ponto final,
                escala a posição do ponto final, inverte a translação e depois gera a linha de novo
                com base no novo ponto final).
        reflect(self, reflect_on_x, reflect_on_y, center_x, center_y): Reflete a linha em torno de
                um eixo especificado (reflete os pontos de início e fim e gera de novo a linha).
        clip(self, start, end, algorithm): Recorta a linha a partir da área entre dois pontos
                utilizando ou Cohen-Sutherland (método `clip_cohen`) ou Liang-Barsky (método
                `clip_liang`). Usei as implementações do livro (Computer Graphics C version).
        clip_cohen(self, start, end): Implementação do método de Cohen-Sutherland.
        cohen_get_code(self, x, y, x_min, x_max, y_min, y_max): Calcula o código do vértice.
        clip_liang(self, start, end): Implementação do método de Liang-Barsky.
        liang_clip_test(self, p, q, u1, u2): Calcula se a linha deve ser rejeitada ou se os
                parâmetros de interseção devem ser ajustados.
    """

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
        self.end.translate(self.start.x, self.start.y)

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
        x1, y1 = (self.start.x, self.start.y)
        x2, y2 = (self.end.x, self.end.y)

        x_min = round(min(start[0], end[0]))
        x_max = round(max(start[0], end[0]))
        y_min = round(min(start[1], end[1]))
        y_max = round(max(start[1], end[1]))

        x_int = y_int = 0

        accept = False
        done = False

        while not done:
            c1 = self.cohen_get_code(x1, y1, x_min, x_max, y_min, y_max)
            c2 = self.cohen_get_code(x2, y2, x_min, x_max, y_min, y_max)

            if c1 == 0 and c2 == 0:
                accept = True
                done = True
            elif c1 & c2:
                done = True
            else:
                c_out = c1 if c1 else c2

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
        x1, y1 = (self.start.x, self.start.y)
        x2, y2 = (self.end.x, self.end.y)

        x_min = round(min(start[0], end[0]))
        x_max = round(max(start[0], end[0]))
        y_min = round(min(start[1], end[1]))
        y_max = round(max(start[1], end[1]))

        u1 = 0
        u2 = 1
        dx = x2 - x1
        dy = y2 - y1
        u1, u2, accept = self.liang_clip_test(-dx, x1 - x_min, u1, u2)

        if accept:
            u1, u2, accept = self.liang_clip_test(dx, x_max - x1, u1, u2)
            if accept:
                u1, u2, accept = self.liang_clip_test(-dy, y1 - y_min, u1, u2)
                if accept:
                    u1, u2, accept = self.liang_clip_test(dy, y_max - y1, u1, u2)
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

    def liang_clip_test(self, p, q, u1, u2):
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
        elif q < 0:
            ret_val = False

        return u1, u2, ret_val


class Circle(Structure):
    """
    Representa um círculo através de um centro e um raio.

    Args:
        center (tuple): O centro do círculo.
        radius (float): O raio do círculo.
        color (str): A cor do círculo.

    Atributos:
        center (Pixel): O centro do círculo.
        radius (float): O raio do círculo.
        color (str): A cor do círculo.
        pixels (list): A lista com os pixels do círculo (após serem gerados com o get_circle).
        clipped (bool): Indica se o círculo foi recortado (algumas mudanças são feitas nas
                transformações caso isso seja verdadeiro - não era um requisito do projeto
                mas ficou mais bem apresentável assim enquanto não temos um algoritmo de
                recorte para círculos/polígonos).

    Métodos:
        __init__(self, center, radius, color):  Inicializa um novo círculo com centro, raio e
                cor especificados.
        get_circle(self): Calcula os pixels que formam o círculo.
        plot_points(self, xc, yc, x, y): Adiciona os pontos do círculo à estrutura.
        translate(self, x, y): Translada o ponto central do círculo.
        rotate(self, angle, center): Rotaciona o ponto central do círculo.
        scale(self, x, y):  Multiplica o tamanho do raio do círculo (apenas o x é usado, porém
                o método recebe tanto x quanto y para manter os parâmetros iguais para todas as
                classes que estendem Structure).
        reflect(self, reflect_on_x, reflect_on_y, center_x, center_y): Reflete o centro do círculo.
    """

    def __init__(self, center, radius, color):
        self.center = Pixel(center, color)
        self.radius = radius
        self.color = color
        self.pixels = []

        self.clipped = False

        self.get_circle()

    def __repr__(self):
        return f"Circle(center={self.center}, radius={self.radius}, color={self.color})"

    @staticmethod
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
