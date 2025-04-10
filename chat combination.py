import pygame
import random
import copy

# Initialize pygame
pygame.init()

# Define Colors
Green = (0, 255, 0)
Red = (255, 0, 0)
White = (255, 255, 255)

# Setup window dimensions
screen_width = 800
screen_height = 600
display = pygame.display.set_mode((screen_width, screen_height))

# Load images (dummy placeholders)
home_Screen = pygame.Surface((100, 100))
home_Screen.fill((200, 200, 200))
poker_Chips = pygame.Surface((100, 100))
poker_Chips.fill((255, 255, 255))
x_button = pygame.Surface((50, 50))
x_button.fill((255, 0, 0))
O_button = pygame.Surface((50, 50))
O_button.fill((0, 255, 0))
square_button = pygame.Surface((50, 50))
square_button.fill((0, 0, 255))
triangle_button = pygame.Surface((50, 50))
triangle_button.fill((255, 165, 0))

# Initialize fonts
small_font = pygame.font.SysFont('Arial', 30)

# Game States
GAME = 1
MENU = 0
BETTING = 2
END = 3

# Player State
player_chips = 1000  # Starting chips
state = MENU  # Starting state

# Controller placeholder (dummy input for now)
controller = None  # Replace with your actual controller input handling

# Game Logic

def set_menu(display, Green, Red, home_Screen, small_font, White):
    display.fill(Green)

    # Title text
    font = pygame.font.SysFont('Times New Roman', 66)
    text = font.render('BLACKJACK', True, Red)
    display.blit(text, (275, 50))

    # Home Screen Cards image & Button
    display.blit(home_Screen, (225, 200))

    play_text = small_font.render('X to Play', True, White)

    # Center the text inside the button
    text_x = 300 + (350 - play_text.get_width()) // 2
    text_y = 600 + (100 - play_text.get_height()) // 2
    display.blit(play_text, (text_x, text_y))

def set_betting(display, Green, poker_Chips, small_font, White, controller, x_button, O_button, square_button, triangle_button, state, GAME, MENU, BETTING):
    display.fill(Green)
    game_text = small_font.render('Bet amount', True, White)
    total_text = small_font.render('Total:', True, White)
    display.blit(game_text, (315, 50))
    display.blit(total_text, (200, 250))
    display.blit(poker_Chips, (215, 450))
    display.blit(square_button, (240, 600))
    display.blit(triangle_button, (410, 605))
    display.blit(O_button, (575, 595))

    # Event handling for buttons (this can be enhanced with controller input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Handle button presses to change states (dummy for now)
        if controller and controller.get_button(x_button):  # X to play
            state = GAME
        if controller and controller.get_button(O_button):  # O for menu
            state = MENU
    pygame.display.flip()
    return state

def set_game(display, Green, poker_Chips, small_font, White, controller, x_button, O_button, square_button, triangle_button, state, GAME):
    display.fill(Green)
    game_text = small_font.render('Game in progress', True, White)
    total_text = small_font.render('Dealer', True, White)
    display.blit(game_text, (315, 50))
    display.blit(total_text, (200, 250))

    # Here you can handle the gameplay logic, update cards, etc.
    # Display the buttons
    display.blit(poker_Chips, (215, 450))
    display.blit(square_button, (240, 600))
    display.blit(triangle_button, (410, 605))
    display.blit(O_button, (575, 595))

    pygame.display.flip()

    # Handle events (gameplay buttons)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Placeholder for button press handling, can be expanded
        if controller and controller.get_button(x_button):  # Placeholder for button X
            pass

    return state

def set_end(display, Green, small_font, White, controller, x_button, O_button, state, GAME, MENU, BETTING, player_chips):
    # Display messages for winning and losing
    game_text_lost = small_font.render("Bankrupt! Grammy is upset you've spent all your college tuition.", True, White)
    game_text_won = small_font.render("You've hit Relbmag status! $5000 added to your life savings!", True, White)

    display.fill(Green)

    # Display the game over message (winning or losing)
    if player_chips <= 0:
        display.blit(game_text_lost, (50, 250))  # Losing message
    else:
        display.blit(game_text_won, (50, 50))  # Winning message

    # Display the buttons
    display.blit(x_button, (240, 600))  # Button for restarting
    display.blit(O_button, (575, 595))  # Button for returning to the menu

    # Check controller inputs for state transition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if controller and controller.get_button(x_button):  # X button to restart the game
            state = BETTING  # Transition to betting phase
            return state

        if controller and controller.get_button(O_button):  # O button to return to the menu
            state = MENU  # Go back to the main menu
            return state

    pygame.display.flip()  # Update the screen
    return state

# Main Game Loop
running = True
while running:
    if state == MENU:
        set_menu(display, Green, Red, home_Screen, small_font, White)
        pygame.display.flip()
        state = set_betting(display, Green, poker_Chips, small_font, White, controller, x_button, O_button, square_button, triangle_button, state, GAME, MENU, BETTING)

    elif state == BETTING:
        state = set_betting(display, Green, poker_Chips, small_font, White, controller, x_button, O_button, square_button, triangle_button, state, GAME, MENU, BETTING)

    elif state == GAME:
        state = set_game(display, Green, poker_Chips, small_font, White, controller, x_button, O_button, square_button, triangle_button, state, GAME)

    elif state == END:
        state = set_end(display, Green, small_font, White, controller, x_button, O_button, state, GAME, MENU, BETTING, player_chips)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
exit()
