import pygame
import random
import copy

pygame.init()
pygame.mixer.init()

lobby_music = pygame.mixer.Sound("lobby_music.mp3")
main_music = pygame.mixer.Sound("main_music.mp3")
pygame.display.set_caption("BLACKJACK - Sam & Sid")

lobby_music.play()

WIDTH = 900
HEIGHT = 800
display = pygame.display.set_mode([WIDTH, HEIGHT])

Green = (0, 50, 0)
White = (255, 255, 255)
Red = (255, 0, 9)

display.fill(Green)

#controller = pygame.joystick.Joystick(0)

# Hauptloop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    display.fill(Green)

# add music = Money pink floyd, Nostalgia christopher tyng

    font = pygame.font.SysFont('Times New roman', 66)
    text = font.render('BLACKJACK', True, Red)
    display.blit(text, (275, 50))

    # Hier kannst du die Karten, Spielstand, etc. zeichnen
    pygame.draw.rect(display, (White), (350, 150, 250 ,350))
    pygame.draw.rect(display, (127,127,127), (300, 600, 350 ,100))

    box_width = 300
    box_height = 100
    box_x = WIDTH // 2 - box_width // 2
    box_y = HEIGHT // 2 - box_height // 2

    play_text = font.render('X to Play', True, White)

    # Text in die Mitte der Box setzen
    text_x = box_x + (box_width - play_text.get_width()) // 2
    text_y = box_y + (box_height - play_text.get_height()) // 2
    display.blit(play_text, (350, 610, 350 ,100))


    pygame.display.flip()
#while not done:
    #if controller.get_button(0):


# Pygame beenden
pygame.quit()
