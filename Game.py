import pygame
import random
import copy
pygame.init()

def set_game(display, Green, poker_Chips, small_font, White, controller, x_button, O_button, square_button, triangle_button, state, GAME, current_hand, current_deck):
    display.fill(Green)
    game_text = small_font.render('Bet amount', True, White)
    total_text = small_font.render('Dealer', True, White)
    display.blit(game_text, (315, 50))
    display.blit(total_text, (200, 250))
