import pygame
import random
import copy

pygame.init()
pygame.mixer.init()
pygame.joystick.init()

lobby_music = pygame.mixer.Sound("lobby_music.mp3")
main_music = pygame.mixer.Sound("main_music.mp3")
pygame.display.set_caption("BLACKJACK - Sam & Sid")

lobby_music.play()

WIDTH = 900
HEIGHT = 800
display = pygame.display.set_mode([WIDTH, HEIGHT])

MENU = 0
GAME = 1
state = MENU

Green = (0, 50, 0)
White = (255, 255, 255)
Red = (255, 0, 9)

display.fill(Green)

controller = pygame.joystick.Joystick(0)


# Hauptloop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.quit():
            running = False

        if event.type == pygame.JOYBUTTONDOWN and controller:
            if event.button == 0:
                state = GAME

    if state == MENU:
        display.fill(Green)

        font = pygame.font.SysFont('Times New roman', 66)
        text = font.render('BLACKJACK', True, Red)
        display.blit(text, (280, 50))

    # Hier kannst du die Karten, Spielstand, etc. zeichnen
        pygame.draw.rect(display, (White), (350, 150, 250, 350))
        pygame.draw.rect(display, (127, 127, 127), (300, 600, 350, 100))

        box_width = 300
        box_height = 100
        box_x = WIDTH // 2 - box_width // 2
        box_y = HEIGHT // 2 - box_height // 2

        play_text = font.render('X to Play', True, White)

    elif state == GAME:
        display.fill((0, 100, 0))
        game_text = font.render("mkkkkk", True, White)
        display.blit(game_text, (275, 50))


    display.blit(play_text, (350, 610, 350, 100))
    pygame.display.flip()

pygame.quit()


