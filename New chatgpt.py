import pygame
import random
import copy

from pygame.examples.moveit import GameObject

pygame.init()
pygame.mixer.init()
pygame.joystick.init()

WIDTH, HEIGHT = 900, 800
display = pygame.display.set_mode([WIDTH, HEIGHT])

if pygame.joystick.get_count() > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()
else:
    controller = None

# Load music
lobby_music = pygame.mixer.Sound("lobby_music.mp3")
main_music = pygame.mixer.Sound("main_music.mp3")

home_Screen = pygame.image.load("19-playing-cards-png.png").convert_alpha()
home_Screen = pygame.transform.scale_by(home_Screen, 0.3)
poker_Chips = pygame.image.load("chips-poker 1.png").convert_alpha()
poker_Chips = pygame.transform.scale_by(poker_Chips, 0.3)
lobby_music.play()

pygame.display.set_caption("BLACKJACK - Sam & Sid")

Green = (0, 50, 0)
White = (255, 255, 255)
Red = (255, 0, 9)

# Game states
MENU = 0
BETTING = 1
GAME = 2
END = 3

state = MENU

# Main loop for the game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.JOYBUTTONDOWN and controller:
            if event.button == 0:  # "X" button on PS controller (or adjust for Xbox)
                state = BETTING

    # Display different screens based on state
    if state == MENU:
        display.fill(Green)

        # Title text
        font = pygame.font.SysFont('Times New Roman', 66)
        text = font.render('BLACKJACK', True, Red)
        display.blit(text, (275, 50))

        #Home Screen Cards image & Button
        display.blit(home_Screen, (225, 175))
        pygame.draw.rect(display, (127, 127, 127), (300, 600, 350, 100))

        small_font = pygame.font.SysFont('Times New Roman', 40)
        play_text = small_font.render('X to Play', True, White)

        # Center the text inside the button
        text_x = 300 + (350 - play_text.get_width()) // 2
        text_y = 600 + (100 - play_text.get_height()) // 2
        display.blit(play_text, (text_x, text_y))

    elif state == BETTING:
        display.fill((0, 100, 0))  # Change background color for the game screen
        game_text = font.render('Bet amount', True, White)
        display.blit(game_text, (300, 50))

        if controller.get_button(0):  # A for playstation = X / Colour is Red
            pygame.draw.rect(display, (255, 0, 0), [0, 0, 800, 600])
        elif controller.get_button(1):  # B for playstation = O / Colour is Green
            pygame.draw.rect(display, (0, 255, 0), [0, 0, 800, 600])
        elif controller.get_button(2):  # X for playstation = SQUARE / Colour is Blue
            pygame.draw.rect(display, (0, 0, 255), [0, 0, 800, 600])
        elif controller.get_button(3):  # Y for playstation = Triangle / Colour is Orange
            pygame.draw.rect(display, (255, 165, 0), [0, 0, 800, 600])

    pygame.display.flip()

pygame.quit()
