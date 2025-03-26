
import pygame

import Game
import Menu
import Betting
#import Game
#import End

from pygame.examples.moveit import GameObject

pygame.init()
pygame.mixer.init()
pygame.joystick.init()

#variables
WIDTH, HEIGHT = 900, 800
display = pygame.display.set_mode([WIDTH, HEIGHT])

small_font = pygame.font.SysFont('Times New Roman', 55)

if pygame.joystick.get_count() > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()
else:
    controller = None

# Load music
lobby_music = pygame.mixer.Sound("Audio/lobby_music.mp3")
main_music = pygame.mixer.Sound("Audio/main_music.mp3")

home_Screen = pygame.image.load("Sprites/19-playing-cards-png.png").convert_alpha()
home_Screen = pygame.transform.scale_by(home_Screen, 0.3)
poker_Chips = pygame.image.load("Sprites/chips-poker 1-Photoroom.png").convert_alpha()
poker_Chips = pygame.transform.scale_by(poker_Chips, 0.4)

# all ps button variables
x_button = pygame.image.load("Sprites/Screenshot_2025-03-25_103206-removebg-preview.png").convert_alpha()
x_button = pygame.transform.scale_by(x_button, 0.2)
O_button = pygame.image.load("Sprites/Screenshot_2025-03-25_103112-removebg-preview.png").convert_alpha()
O_button = pygame.transform.scale_by(O_button, 0.2)
square_button = pygame.image.load("Sprites/Screenshot_2025-03-25_103052-removebg-preview.png").convert_alpha()
square_button = pygame.transform.scale_by(square_button, 0.2)
triangle_button = pygame.image.load("Sprites/Screenshot_2025-03-25_103122-removebg-preview.png").convert_alpha()
triangle_button = pygame.transform.scale_by(triangle_button, 0.2)
#change after game state changes to BETTING
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
            pygame.quit()
        if state == MENU:
            Menu.set_menu(display=display, Green=Green, Red=Red, home_Screen=home_Screen, small_font=small_font,
                          White=White)

        if event.type == pygame.JOYBUTTONDOWN and controller:
            if event.button == 0:  # "X" button on PS controller (or adjust for Xbox)
                state = BETTING
                print("State: Betting")
        pygame.display.flip()
    # Display different screens based on state

    while state == BETTING:
        Betting.set_betting(display=display, Green=Green, poker_Chips=poker_Chips, small_font=small_font, White=White, controller=controller, x_button=x_button, O_button=O_button, square_button=square_button, triangle_button=triangle_button, state=state, GAME=GAME)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.JOYBUTTONDOWN and controller:
                if event.button == 0:  # "X" button on PS controller (or adjust for Xbox)
                    state = GAME
                    print("State: Game")
            if event.type == pygame.JOYBUTTONDOWN and controller:
                if event.button == 1:
                    print(" added 50")
            pygame.display.flip()

    while state == GAME:
        Game.set_game(display, Green, poker_Chips, small_font, White, controller, x_button, O_button, square_button, triangle_button, state, GAME)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            pygame.display.flip()



pygame.quit()