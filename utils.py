import pygame

def draw_text(text, font, color, x, y, win):
    score_text = font.render(text, True, color)
    win.blit(score_text, (x, y))

def draw_centered_text(surface, text, font, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)
