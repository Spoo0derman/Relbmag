import pygame
import Game
pygame.init()

def set_betting(display, Green, poker_Chips, small_font, White, O_button, square_button, triangle_button, x_button, total_bet_amount):
    display.fill(Green)
    game_text = small_font.render('Bet amount', True, White)
    total_text = small_font.render('Total:', True, White)
    advance_text = small_font.render('to advance', True, White)
    display.blit(game_text, (315, 50))
    display.blit(total_text, (200, 245))
    display.blit(poker_Chips, (215, 450))
    display.blit(square_button, (240, 600))
    display.blit(triangle_button, (410, 605))
    display.blit(O_button, (575, 595))
    if total_bet_amount > 0:
        display.blit(advance_text, (590, 250))
        display.blit(x_button, (475, 225))






    #if controller.get_button(0):  # A for playstation = X / Colour is Red
        #state = GAME
    #if controller.get_button(1):  # B for playstation = O / Colour is Green
        #pygame.draw.rect(display, (0, 255, 0), [0, 0, 800, 600])
    #elif controller.get_button(2):  # X for playstation = SQUARE / Colour is Blue
        #pygame.draw.rect(display, (0, 0, 255), [0, 0, 800, 600])
    #elif controller.get_button(3):  # Y for playstation = Triangle / Colour is Orange
        #pygame.draw.rect(display, (255, 165, 0), [0, 0, 800, 600])