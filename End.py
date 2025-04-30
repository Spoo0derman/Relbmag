import pygame
pygame.init()

def set_end(display, Green, small_font, White, controller, x_button, O_button, state, GAME, MENU, BETTING):
    display.fill(Green)
    display.blit(x_button, (240, 600))
    display.blit(O_button, (575, 595))
    #pygame.display.flip()
