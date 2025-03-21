import pygame
import random

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

# Check if a controller is connected
if pygame.joystick.get_count() > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()
else:
    controller = None

# Load music
lobby_music = pygame.mixer.Sound("lobby_music.mp3")
main_music = pygame.mixer.Sound("main_music.mp3")

# Load card image (Make sure "jack_spades.png" is in the same folder)
jack_card = pygame.image.load("jack_spades.png")
jack_card = pygame.transform.scale(jack_card, (120, 180))  # Resize for UI

# Set window title
pygame.display.set_caption("BLACKJACK - Sam & Sid")

# Play lobby music on loop
lobby_music.play(-1)

# Set display size
WIDTH, HEIGHT = 900, 800
display = pygame.display.set_mode([WIDTH, HEIGHT])

# Colors
Green = (0, 50, 0)
White = (255, 255, 255)
Red = (255, 0, 9)

# Game states
MENU = 0
GAME = 1
state = MENU  # Start at menu

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detect controller button press
        if event.type == pygame.JOYBUTTONDOWN and controller:
            if event.button == 0:  # "X" button on PS controller
                state = GAME  # Move to game screen

    # Display different screens based on state
    if state == MENU:
        display.fill(Green)

        # Title text
        font = pygame.font.SysFont('Times New Roman', 66)
        text = font.render('BLACKJACK', True, Red)
        display.blit(text, (275, 50))

        # Draw the Jack of Spades card below title
        display.blit(jack_card, (390, 200))  # Adjusted position for center alignment

        # Draw button area
        pygame.draw.rect(display, (127, 127, 127), (300, 600, 350, 100))  # Button area

        # Play text
        small_font = pygame.font.SysFont('Times New Roman', 40)
        play_text = small_font.render('X to Play', True, White)

        # Center the text inside the button
        text_x = 300 + (350 - play_text.get_width()) // 2
        text_y = 600 + (100 - play_text.get_height()) // 2
        display.blit(play_text, (text_x, text_y))

    elif state == GAME:
        display.fill((0, 100, 0))  # Change background color for the game screen
        game_text = font.render('Game Started!', True, White)
        display.blit(game_text, (275, 50))

    # Update display
    pygame.display.flip()
    pygame.time.delay(10)  # Prevents excessive CPU usage

pygame.quit()
