import pygame
import random
import copy

pygame.mixer.init()
lobby_music = pygame.mixer.Sound("lobby_music.mp3")
pygame.init()

pygame.display.set_caption("BLACKJACK - Sam & Sid")

WIDTH = 900
HEIGHT = 800
display = pygame.display.set_mode([WIDTH, HEIGHT])
Green = (0, 255, 0)

controller = pygame.joystick.Joystick(0)
lobby_music.play()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    display.fill(Green)





