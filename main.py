from lib import *

def main():
    pygame.init()

    screen = pygame.display.set_mode((REAL_WIDTH, REAL_HEIGHT))
    pygame.display.set_caption("Paint")

    screen.fill([255, 255, 255])

    button1 = Button("teste", (100, 50), (100, 50), (0, 0, 0), screen)
    first_click = None
    second_click = None

    draw_line_button_clicked = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(*event.pos)
                if draw_line_button_clicked:
                    if first_click is None:
                        first_click = event.pos
                    elif second_click is None:
                        second_click = event.pos

                        # draw_line_dda(screen, first_click, second_click, (0, 0, 0))
                        draw_line_bresenham(screen, first_click, second_click, (0, 0, 0))
                        
                        first_click = None
                        second_click = None
                else:
                    draw_pixel(screen, event.pos, (0, 0, 0))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
