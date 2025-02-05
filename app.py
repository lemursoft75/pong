import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Inicializar el mezclador de sonido
pygame.mixer.init()

# Cargar sonidos
hit_sound = pygame.mixer.Sound("hit.wav")
score_sound = pygame.mixer.Sound("score.wav")

# Configuración de la ventana
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Arcade Classics")

# Colores
white = (255, 255, 255)
black = (0, 0, 0)

# Raquetas y pelota
player_width, player_height = 15, 100
enemy_width, enemy_height = 15, 100
ball_size = 15

# Inicializar posiciones
player_x, player_y = 50, height // 2 - player_height // 2
enemy_x, enemy_y = width - 50 - enemy_width, height // 2 - enemy_height // 2
ball_x, ball_y = width // 2, height // 2
ball_speed_x, ball_speed_y = -7, 7 * random.choice((1, -1))

# Velocidad de las raquetas
player_speed, enemy_speed = 40, 40

# Puntuación
player_score, enemy_score = 0, 0
font = pygame.font.SysFont(None, 55)


def draw_text(text, font, color, x, y):
    score_text = font.render(text, True, color)
    win.blit(score_text, (x, y))


def draw_centered_text(surface, text, font, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)



def main_menu():
    menu_font = pygame.font.SysFont(None, 60)  # Título más grande
    button_font = pygame.font.SysFont(None, 50)
    selected_button = 0
    buttons = ["1 Player", "2 Players", "Controles", "Salir"]

    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_exit_message()  # Mostrar el mensaje de salida antes de salir
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_button = (selected_button + 1) % len(buttons)
                elif event.key == pygame.K_UP:
                    selected_button = (selected_button - 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    if buttons[selected_button] == "1 Player":
                        game_loop()
                    elif buttons[selected_button] == "2 Players":
                        # Aquí puedes agregar funcionalidad para 2 jugadores
                        pass
                    elif buttons[selected_button] == "Controles":
                        # Aquí puedes mostrar los controles
                        pass
                    elif buttons[selected_button] == "Salir":
                        show_exit_message()  # Mostrar el mensaje de salida antes de salir
                        pygame.quit()
                        sys.exit()

        win.fill(black)
        title = menu_font.render("Emulador by PeñaSoft", True, white)
        win.blit(title, (width // 2 - title.get_width() // 2, 80))

        y_pos = 200
        for i, button in enumerate(buttons):
            if i == selected_button:
                btn_text = button_font.render(button, True, (255, 0, 0))
            else:
                btn_text = button_font.render(button, True, white)
            win.blit(btn_text, (width // 2 - btn_text.get_width() // 2, y_pos + i * 80))

        pygame.display.update()

def show_exit_message():
    win.fill(black)
    exit_font = pygame.font.SysFont(None, 40)
    exit_text = exit_font.render("Gracias por jugar", True, white)
    win.blit(exit_text, (width // 2 - exit_text.get_width() // 2, height // 2 - exit_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(1000)  # Esperar 1 segundos antes de salir

def pause_game():
    paused = True
    pause_font = pygame.font.SysFont(None, 35)
    pause_text = pause_font.render("Presiona Enter para continuar o Escape para volver al menú", True, white)
    win.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2))
    pygame.display.flip()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    main_menu()


def game_loop():
    global player_x, player_y, enemy_x, enemy_y, ball_x, ball_y, ball_speed_x, ball_speed_y, player_score, enemy_score, player_speed, font

    # Declarar la fuente dentro de game_loop
    font = pygame.font.SysFont(None, 55)

    # Bucle principal
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_game()
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # Suponiendo que el botón 0 sea el de disparo
                    player_speed = 60
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 0:
                    player_speed = 40

        # Detectar controladores
        joystick_count = pygame.joystick.get_count()
        if joystick_count > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            player_y += joystick.get_axis(1) * player_speed

        keys = pygame.key.get_pressed()
        player_y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player_speed

        # Actualizar posición de la raqueta del jugador
        player_y = max(0, min(height - player_height, player_y))

        # Actualizar posición de la raqueta del oponente (Bot)
        enemy_y += enemy_speed * ((ball_y - (enemy_y + enemy_height / 2)) / height)
        enemy_y = max(0, min(height - enemy_height, enemy_y))

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Colisiones con las paredes
        if ball_y <= 0 or ball_y >= height - ball_size:
            ball_speed_y *= -1

        # Colisiones con las raquetas
        if (
                (player_x <= ball_x <= player_x + player_width and
                 player_y <= ball_y <= player_y + player_height) or
                (enemy_x <= ball_x <= enemy_x + enemy_width and
                 enemy_y <= ball_y <= enemy_y + enemy_height)
        ):
            ball_speed_x *= -1
            hit_sound.play()

        # Punto para el oponente (Bot)
        if ball_x <= 0:
            enemy_score += 1
            ball_x, ball_y = width // 2, height // 2
            ball_speed_x *= random.choice((1, -1))
            score_sound.play()

        # Punto para el jugador
        if ball_x >= width - ball_size:
            player_score += 1
            ball_x, ball_y = width // 2, height // 2
            ball_speed_x *= random.choice((1, -1))
            score_sound.play()

        # Dibujar en la ventana
        win.fill(black)
        pygame.draw.rect(win, (0, 0, 255), (player_x, player_y, player_width, player_height))
        pygame.draw.rect(win, (255, 0, 0), (enemy_x, enemy_y, enemy_width, enemy_height))
        pygame.draw.ellipse(win, white, (ball_x, ball_y, ball_size, ball_size))
        draw_text(str(player_score), font, white, width // 4, 20)
        draw_text(str(enemy_score), font, white, 3 * width // 4 - 20, 20)

        # Mostrar el título
        title_font = pygame.font.SysFont(None, 40)
        title_text = title_font.render("Emulador Pong", True, white)
        win.blit(title_text, (width // 2 - title_text.get_width() // 2, 10))

        # Mostrar las puntuaciones
        draw_text(str(player_score), font, white, width // 4, 20)
        draw_text(str(enemy_score), font, white, 3 * width // 4 - 20, 20)

        # Verificar si algún jugador ha alcanzado el puntaje máximo
        max_score = 5
        if player_score >= max_score or enemy_score >= max_score:
            if player_score > enemy_score:
                winner_text = "¡¡¡VENCEDOR!!!"
                winner_color = (0, 255, 0)
            else:
                winner_text = "¡¡¡DERROTADO!!!"
                winner_color = (255, 0, 0)

            font = pygame.font.SysFont(None, 40)
            draw_centered_text(win, winner_text, font, winner_color, win.get_rect())
            pygame.display.flip()
            pygame.time.wait(1500)  # Esperar 1.5 segundos antes de continuar

            # Mostrar mensaje para continuar
            continue_font = pygame.font.SysFont(None, 30)
            continue_text = continue_font.render("Presiona Enter para jugar de nuevo o Escape para volver al menú", True, white)
            win.blit(continue_text, (width // 2 - continue_text.get_width() // 2, height // 2 + 50))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            main_menu()

            # Reiniciar posiciones y puntajes
            player_score = enemy_score = 0
            ball_x, ball_y = width // 2, height // 2
            ball_speed_x, ball_speed_y = -7, 7 * random.choice((1, -1))

        pygame.display.flip()
        pygame.time.Clock().tick(60)


main_menu()
