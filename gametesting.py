import pygame, random, Game, Menu, Betting, copy, End

from pygame.examples.moveit import GameObject

pygame.init()
pygame.mixer.init()
pygame.joystick.init()

#variables
WIDTH, HEIGHT = 900, 800
display = pygame.display.set_mode([WIDTH, HEIGHT])


fps = 120
timer = pygame.time.Clock()

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
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
player_hand = []
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'YOU LOST', 'YOU WIN', 'DEALER WINS', 'TIE GAME']

#Game definitions
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return current_hand, current_deck


# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    display.blit(small_font.render(f'Score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        display.blit(small_font.render(f'Score[{dealer}]', True, 'white'), (350, 100))

def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(display, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        display.blit(small_font_1.render(player[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
        display.blit(small_font_1.render(player[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
        pygame.draw.rect(display, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

        # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(display, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
           display.blit(small_font_1.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
           display.blit(small_font_1.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else:
            display.blit(small_font_1.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            display.blit(small_font_1.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(display, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)

# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # for 2,3,4,5,6,7,8,9 - just add the number to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10 and face cards, add 10
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, we'll check if we need to reduce afterwards
        elif hand[i] == 'A':
            hand_score += 11
    # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score


# draw game conditions and buttons
def draw_game(act, record, result):
    button_list = []
    # initially on startup (not active) only option is to deal new hand
    if not act:
        hit = pygame.draw.rect(display, 'white', [50, 700, 300, 100], 0, 5)
        #pygame.draw.rect(display, Green, [100, 700, 300, 100], 3, 5)
        hit_text = small_font_1.render('◻ to HIT', True, 'black')
        display.blit(hit_text, (100, 735))
        button_list.append(hit)
        stand = pygame.draw.rect(display, 'white', [525, 700, 300, 100], 0, 5)
        #pygame.draw.rect(display, 'green', [300, 700, 300, 100], 3, 5)
        stand_text = small_font_1.render('O to STAND', True, 'black')
        display.blit(stand_text, (535, 735))
        button_list.append(stand)
        score_text = small_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        display.blit(score_text, (15, 840))
    # if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0:
        display.blit(small_font_1.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(display, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(display, 'green', [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(display, 'black', [153, 223, 294, 94], 3, 5)
        deal_text = small_font.render('NEW HAND', True, 'black')
        display.blit(deal_text, (165, 250))
        button_list.append(deal)
    return button_list


# check endgame conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # check end game scenarios is player has stood, busted or blackjacked
    # result 1- player bust, 2-win, 3-loss, 4-push
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
            return result, totals, add

# Main loop for the game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if state == MENU:
            Menu.set_menu(display=display, Green=Green, Red=Red, home_Screen=home_Screen, small_font=small_font,
                          White=White)
        if event.type == keys[pygame.K_ESCAPE]:
            running = False
            pygame.quit()

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
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                pygame.quit()
                break
            if event.type == pygame.JOYBUTTONDOWN and controller:
                if event.button == 0 and total_bet_amount > 0:  # "X" button on PS controller (or adjust for Xbox)
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
        display.blit(total_displayed, (50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                pygame.quit()
                break
        if initial_deal:
            for i in range(2):
                my_hand, game_deck = deal_cards(my_hand, game_deck)
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            initial_deal = False
        if active:
            player_score = calculate_score(my_hand)
            draw_cards(my_hand, dealer_hand, reveal_dealer)
            if reveal_dealer:
                dealer_score = calculate_score(dealer_hand)
                if dealer_score < 17:
                    dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            draw_scores(player_score, dealer_score)
        buttons = draw_game(active, records, outcome)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False
            if event.type == pygame.JOYBUTTONDOWN and controller:
                if not active:
                    if controller.get_button(0):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * single_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        add_score = True
                else:
                    # if player can hit, allow them to draw a card
                    if controller.get_button(0) and player_score < 21 and hand_active:
                        my_hand, game_deck = deal_cards(my_hand, game_deck)
                    # allow player to end turn (stand)
                    elif controller.get_button(1) and not reveal_dealer:
                        reveal_dealer = True
                        hand_active = False
                    elif len(buttons) == 3:
                        if buttons[2].collidepoint(event.pos):
                            active = True
                            initial_deal = True
                            game_deck = copy.deepcopy(decks * single_deck)
                            my_hand = []
                            dealer_hand = []
                            outcome = 0
                            hand_active = True
                            reveal_dealer = False
                            add_score = True
                            dealer_score = 0
                            player_score = 0

        # if player busts, automatically end turn - treat like a stand
        if hand_active and player_score >= 21:
            hand_active = False
            reveal_dealer = True

        #outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

        #we check first the button press and the score and then these if statements
            #if current_money >= 5000:
            #    state = END
            #elif current_money <= 50:
             #   state = END
            #elif current_money >= 50 and current_money <= 5000:
            #    state = BETTING
        pygame.display.flip()

    while state == END:
        END.set_end(display=display, Green=Green, small_font=small_font, White=White, controller=controller, x_button=x_button, O_button=O_button, state=state, GAME=GAME, MENU=MENU, BETTING=BETTING)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                pygame.quit()
                break
            if event.type == pygame.JOYBUTTONDOWN and controller:
                if event.button == 0:  # "X" button on PS controller (or adjust for Xbox)
                    state = MENU and current_money == 500 and total_bet_amount == 0
                    break
            if event.type == pygame.JOYBUTTONDOWN and controller:
                if event.button == 2:
                    pygame.quit()
        pygame.display.flip()





