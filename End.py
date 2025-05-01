import pygame
pygame.init()

def set_end(display, Green, x_button, O_button, small_font_1):
    display.fill(Green)
    replay_text = small_font_1.render('to Play Again', True, "white")
    exit_text = small_font_1.render('to Exit', True, "white")
    display.blit(x_button, (240, 425))
    display.blit(replay_text, (190, 525))
    display.blit(O_button, (575, 420))
    display.blit(exit_text, (550, 520))

