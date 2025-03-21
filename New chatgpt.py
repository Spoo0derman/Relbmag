import pygame
import random
import copy

pygame.init()
pygame.mixer.init()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()
else:
    controller = None

# Load music
lobby_music = pygame.mixer.Sound("lobby_music.mp3")
main_music = pygame.mixer.Sound("main_music.mp3")

lobby_music.play()

pygame.display.set_caption("BLACKJACK - Sam & Sid")

WIDTH, HEIGHT = 900, 800
display = pygame.display.set_mode([WIDTH, HEIGHT])

Green = (0, 50, 0)
White = (255, 255, 255)
Red = (255, 0, 9)

# Game states
MENU = 0
GAME = 1
state = MENU

# Main loop for the game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.JOYBUTTONDOWN and controller:
            if event.button == 0:  # "X" button on PS controller (or adjust for Xbox)
                state = GAME

    # Display different screens based on state
    if state == MENU:
        display.fill(Green)

        # Title text
        font = pygame.font.SysFont('Times New Roman', 66)
        text = font.render('BLACKJACK', True, Red)
        display.blit(text, (275, 50))

        pygame.draw.rect(display, (White), (350, 150, 250, 350))
        pygame.draw.rect(display, (127, 127, 127), (300, 600, 350, 100))

        small_font = pygame.font.SysFont('Times New Roman', 40)
        play_text = small_font.render('X to Play', True, White)

        # Center the text inside the button
        text_x = 300 + (350 - play_text.get_width()) // 2
        text_y = 600 + (100 - play_text.get_height()) // 2
        display.blit(play_text, (text_x, text_y))

    elif state == GAME:
        display.fill((0, 100, 0))  # Change background color for the game screen
        game_text = font.render('Deal me', True, White)
        display.blit(game_text, (275, 50))

    pygame.display.flip()

pygame.quit()
