import pygame
pygame.init()

def set_menu(display, Green, Red, home_Screen, small_font, White):
    """

    :param display:
    :param Green:
    :param Red:
    :param home_Screen:
    :return:
    """

    display.fill(Green)

    # Title text
    font = pygame.font.SysFont('Times New Roman', 66)
    text = font.render('BLACKJACK', True, Red)
    display.blit(text, (275, 50))

    #Home Screen Cards image & Button
    display.blit(home_Screen, (225, 200))

    play_text = small_font.render('X to Play', True, White)

    # Center the text inside the button
    text_x = 300 + (350 - play_text.get_width()) // 2
    text_y = 600 + (100 - play_text.get_height()) // 2
    display.blit(play_text, (text_x, text_y))