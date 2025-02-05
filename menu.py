import pygame
import sys
from game import game_loop
from utils import draw_centered_text


def main_menu():
    width, height = 800, 600
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Arcade Classics")

    white = (255, 255, 255)
    black = (0, 0, 0)

    menu_font = pygame.font.SysFont(None, 60)  # Título más grande
    button_font = pygame.font.SysFont(None, 50)
    selected_button = 0
    buttons = ["1 Player", "2 Players", "Controles", "Salir"]

    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_exit_message(win, black, white)  # Mostrar el mensaje de salida antes de salir
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_button = (selected_button + 1) % len(buttons)
                elif event.key == pygame.K_UP:
                    selected_button = (selected_button - 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    if buttons[selected_button] == "1 Player":
                        game_loop(players=1)
                    elif buttons[selected_button] == "2 Players":
                        game_loop(players=2)
                    elif buttons[selected_button] == "Controles":
                        show_controls(win, black, white)  # Muestra los controles
                    elif buttons[selected_button] == "Salir":
                        show_exit_message(win, black, white)  # Mostrar el mensaje de salida antes de salir
                        pygame.quit()
                        sys.exit()

        win.fill(black)
        title = menu_font.render("Emulador Pong by PeñaSoft", True, white)
        win.blit(title, (width // 2 - title.get_width() // 2, 80))

        y_pos = 200
        for i, button in enumerate(buttons):
            if i == selected_button:
                btn_text = button_font.render(button, True, (255, 0, 0))
            else:
                btn_text = button_font.render(button, True, white)
            win.blit(btn_text, (width // 2 - btn_text.get_width() // 2, y_pos + i * 80))

        pygame.display.update()


def show_exit_message(win, black, white):
    win.fill(black)
    exit_font = pygame.font.SysFont(None, 40)
    exit_text = exit_font.render("Gracias por jugar", True, white)
    win.blit(exit_text,
             (win.get_width() // 2 - exit_text.get_width() // 2, win.get_height() // 2 - exit_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(1000)  # Esperar 1 segundos antes de salir


def show_controls(win, black, white):
    win.fill(black)
    controls_font = pygame.font.SysFont(None, 40)
    controls_text = controls_font.render("Controles:", True, white)
    win.blit(controls_text, (win.get_width() // 2 - controls_text.get_width() // 2, 100))

    instructions = [
        "Jugador 1: Flechas arriba y abajo",
        "Jugador 2: Teclas W y S",
        "Pausa: Enter",
        "Salir al menú: Escape"
    ]

    y_pos = 200
    for instruction in instructions:
        inst_text = controls_font.render(instruction, True, white)
        win.blit(inst_text, (win.get_width() // 2 - inst_text.get_width() // 2, y_pos))
        y_pos += 50

    pygame.display.flip()
    pygame.time.wait(3000)  # Esperar 3 segundos antes de volver al menú
