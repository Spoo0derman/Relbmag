
import pygame, Game, Menu, Betting, End

from pygame.examples.moveit import GameObject

pygame.init()
pygame.mixer.init()
pygame.joystick.init()

#variables
WIDTH, HEIGHT = 900, 800
display = pygame.display.set_mode([WIDTH, HEIGHT])

fps = 120
timer = pygame.time.Clock()

small_font = pygame.font.SysFont('Times New Roman', 55)
small_font_1 = pygame.font.SysFont('Times New Roman', 50)
total_bet_amount = 0
total_displayed = small_font_1.render("$" + str(total_bet_amount), True, (0, 255, 170))
current_money = 500
money_displayed_betting_screen = small_font.render("$" + str(current_money), True, (240, 0, 255))

# GAME state variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
# Because there are 4 of each card type in a deck, we must create 4x of each card type in the list for each deck
single_deck = 4 * cards
#4 decks is Casino standard
decks = 4
active = False
player_hand = []
dealer_hand = []
player_score = 0
dealer_score = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'YOU LOST', 'YOU WIN', 'DEALER WINS :(', 'TIE GAME...']
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return current_hand, current_deck


# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))

def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

        # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
           screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
           screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)

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
Blue = (0, 255, 170)
Purple = (240, 0, 255)

# Game states
MENU = 0
BETTING = 1
GAME = 2
END = 3
state = MENU

total_bet_amount = 0

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
        Betting.set_betting(display=display, Green=Green, poker_Chips=poker_Chips, small_font=small_font, White=White, controller=controller, x_button=x_button, O_button=O_button, square_button=square_button, triangle_button=triangle_button, state=state, GAME=GAME, MENU=MENU, BETTING=BETTING)
        display.blit(money_displayed_betting_screen, (50, 50))
        display.blit(total_displayed, (355,250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.JOYBUTTONDOWN and controller:
                if event.button == 0:  # "X" button on PS controller (or adjust for Xbox)
                    state = GAME
                    break
            if event.type == pygame.JOYBUTTONDOWN and controller:
                if event.button == 2:
                    if current_money - 50 >= 0:
                        total_bet_amount += 50
                        total_displayed = small_font_1.render("$" + str(total_bet_amount), True, Blue)
                        current_money -= 50
                        money_displayed_betting_screen = small_font.render("$" + str(current_money), True, Purple)

                elif event.button == 3:
                    if current_money - 100 >= 0:
                        total_bet_amount += 100
                        total_displayed = small_font_1.render("$" + str(total_bet_amount), True, Blue)
                        current_money -= 100
                        money_displayed_betting_screen = small_font.render("$" + str(current_money), True, Purple)

                elif event.button == 1:
                    if current_money - 250 >= 0:
                        total_bet_amount += 250
                        total_displayed = small_font_1.render("$" + str(total_bet_amount), True, Blue)
                        current_money -= 250
                        money_displayed_betting_screen = small_font.render("$" + str(current_money), True, Purple)

            display.blit(total_displayed, (355, 250))
            display.blit(money_displayed_betting_screen, (50, 50))
            pygame.display.flip()

    while state == GAME:
        Game.set_game(display, Green, poker_Chips, small_font, White, controller, x_button, O_button, square_button, triangle_button, state, GAME)
        display.blit(total_displayed, (355, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            #we check first the button press and the score and then these if statements
            if current_money >= 5000:
                state = END
            elif current_money <= 50:
                state = END
            elif current_money >= 50 and current_money <= 5000:
                state = BETTING
        pygame.display.flip()

    while state == END:
        END.set_end(display=display, Green=Green, small_font=small_font, White=White, controller=controller, x_button=x_button, O_button=O_button, state=state, GAME=GAME, MENU=MENU, BETTING=BETTING)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.JOYBUTTONDOWN and controller:
                if event.button == 0:  # "X" button on PS controller (or adjust for Xbox)
                    state = MENU
                    break
            if event.type == pygame.JOYBUTTONDOWN and controller:
                if event.button == 2:
                    pygame.quit()
        pygame.display.flip()





