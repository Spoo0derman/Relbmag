import pygame
pygame.init()

def set_end(display, Green, small_font, White, controller, x_button, O_button, state, GAME, MENU, BETTING):
    game_text_lost = small_font.render("Bankrupt! Grammy is upset you've spent all your college tuiton", True, White)
    game_text_won = small_font.render("You've hit Relbmag status! $5000 to add to life savings!")
    display.fill(Green)
    display.blit(game_text_won, (315, 50))
    display.blit(game_text_lost, (315, 250))
    display.blit(x_button, (240, 600))
    display.blit(O_button, (575, 595))
