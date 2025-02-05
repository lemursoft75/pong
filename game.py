import pygame
import sys
import random
from utils import draw_text, draw_centered_text

def pause_game(win):
    paused = True
    pause_font = pygame.font.SysFont(None, 35)
    pause_text = pause_font.render("Presiona Enter para continuar o Escape para volver al menú", True, (255, 255, 255))
    win.blit(pause_text, (win.get_width() // 2 - pause_text.get_width() // 2, win.get_height() // 2))
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
                    from menu import main_menu
                    main_menu()

def game_loop(players=1):
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

    # Cargar sonidos
    hit_sound = pygame.mixer.Sound("hit.wav")
    score_sound = pygame.mixer.Sound("score.wav")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_game(win)
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

        if players == 2:
            enemy_y += (keys[pygame.K_x] - keys[pygame.K_s]) * enemy_speed
        else:
            # Actualizar posición de la raqueta del oponente (Bot)
            enemy_y += enemy_speed * ((ball_y - (enemy_y + enemy_height / 2)) / height)

        # Ajustar posiciones
        player_y = max(0, min(height - player_height, player_y))
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

        # Punto para el oponente
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
        draw_text(str(player_score), font, white, width // 4, 20, win)
        draw_text(str(enemy_score), font, white, 3 * width // 4 - 20, 20, win)

        # Mostrar el título
        title_font = pygame.font.SysFont(None, 40)
        title_text = title_font.render("Emulador Pong", True, white)
        win.blit(title_text, (width // 2 - title_text.get_width() // 2, 10))

        # Mostrar las puntuaciones
        draw_text(str(player_score), font, white, width // 4, 20, win)
        draw_text(str(enemy_score), font, white, 3 * width // 4 - 20, 20, win)

        # Verificar si algún jugador ha alcanzado el puntaje máximo
        max_score = 5
        if player_score >= max_score or enemy_score >= max_score:
            if player_score > enemy_score:
                winner_text = "¡VICTORIA!"
                winner_color = (0, 255, 0)
            else:
                winner_text = "GAME OVER"
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
                            from menu import main_menu
                            main_menu()

            # Reiniciar posiciones y puntajes
            player_score = enemy_score = 0
            ball_x, ball_y = width // 2, height // 2
            ball_speed_x, ball_speed_y = -7, 7 * random.choice((1, -1))

        pygame.display.flip()
        pygame.time.Clock().tick(60)
