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
entered_game_state = True

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
    # Draw player cards
    for i in range(len(player)):
        x = 400 + (70 * i)
        y = 460 + (5 * i)
        pygame.draw.rect(display, 'white', [x, y, 120, 220], 0, 5)
        display.blit(small_font_1.render(player[i], True, 'black'), (x + 30, y + 5))
        display.blit(small_font_1.render(player[i], True, 'black'), (x + 30, y + 170))
        pygame.draw.rect(display, 'red', [x, y, 120, 220], 5, 5)

    # Draw dealer cards
    for i in range(len(dealer)):
        x = 400 + (70 * i)
        y = 160 + (5 * i)
        pygame.draw.rect(display, 'white', [x, y, 120, 220], 0, 5)

        if i != 0 or reveal:
            display.blit(small_font_1.render(dealer[i], True, 'black'), (x + 30, y + 5))
            display.blit(small_font_1.render(dealer[i], True, 'black'), (x + 30, y + 170))
        else:
            display.blit(small_font_1.render('???', True, 'black'), (x + 20, y + 80))

        pygame.draw.rect(display, 'blue', [x, y, 120, 220], 5, 5)

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

    # Always show Hit/Stand when active
    if act:
        hit = pygame.draw.rect(display, 'white', [0, 700, 300, 100], 0, 5)
        hit_text = small_font_1.render('Square to HIT', True, 'black')
        display.blit(hit_text, (10, 735))
        button_list.append(hit)

        stand = pygame.draw.rect(display, 'white', [600, 700, 300, 100], 0, 5)
        stand_text = small_font_1.render('O to STAND', True, 'black')
        display.blit(stand_text, (625, 735))
        button_list.append(stand)

    score_text = small_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
    display.blit(score_text, (15, 840))

    if outcome == 1:
        display.blit(small_font_1.render("You Win", True, 'white'), (15, 25))
    elif outcome == 3:
        display.blit(small_font_1.render("You Lose", True, 'white'), (15, 25))
    elif outcome == 2:
        display.blit(small_font_1.render("Draw", True, 'white'), (15, 25))

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

def check_winner(player_score, dealer_score):
    if player_score > 21:
        return -1  # Player busts
    elif dealer_score > 21:
        return 1   # Dealer busts
    elif player_score > dealer_score:
        return 1   # Player wins
    elif player_score < dealer_score:
        return -1  # Dealer wins
    else:
        return 0   # Tie

def start_new_game():
    global game_deck, my_hand, dealer_hand, outcome, hand_active, reveal_dealer, add_score, dealer_score, player_score, initial_deal
    game_deck = copy.deepcopy(decks * single_deck)
    my_hand = []
    dealer_hand = []
    outcome = 0
    hand_active = True
    reveal_dealer = False
    add_score = True
    dealer_score = 0
    player_score = 0
    initial_deal = True

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
        if keys[pygame.K_ESCAPE]:
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
        my_hand = []
        dealer_hand = []
        outcome = 0
        dealer_score = 0
        player_score = 0

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
                    entered_game_state = True
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
        if entered_game_state:
            # Initialize game variables
            game_deck = copy.deepcopy(decks * single_deck)
            my_hand = []
            dealer_hand = []
            outcome = 0
            hand_active = True
            reveal_dealer = False
            add_score = True
            active = True
            initial_deal = True

            # Reset scores
            dealer_score = 0
            player_score = 0

            # Draw intro screen
            display.fill(Green)
            Game.set_game(display, Green, poker_Chips, small_font, White, controller,
                          x_button, O_button, square_button, triangle_button, state, GAME)
            display.blit(total_displayed, (50, 50))
            pygame.display.flip()

            entered_game_state = False

        # One event loop per frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                break

            if event.type == pygame.JOYBUTTONDOWN and controller:
                if not active:
                    if event.button == 0:  # X - Start new hand
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
                else:
                    if hand_active:
                        if event.button == 2 and player_score < 21:  # Square - Hit
                            my_hand, game_deck = deal_cards(my_hand, game_deck)
                        elif event.button == 1 and not reveal_dealer:  # Circle - Stand
                            reveal_dealer = True
                            hand_active = False

            # Mouse interaction (UI button press)
            #if event.type == pygame.MOUSEBUTTONDOWN:
                #if len(buttons) == 3 and buttons[2].collidepoint(event.pos):
                    #active = True
                    #initial_deal = True
                    #game_deck = copy.deepcopy(decks * single_deck)
                    #my_hand = []
                    #dealer_hand = []
                    #outcome = 0
                    #hand_active = True
                    #reveal_dealer = False
                    #add_score = True
                    #dealer_score = 0
                    #player_score = 0

        # Handle initial deal
        if initial_deal:
            for i in range(2):
                my_hand, game_deck = deal_cards(my_hand, game_deck)
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            initial_deal = False

        # Update scores
        player_score = calculate_score(my_hand)
        dealer_score = calculate_score(dealer_hand) if reveal_dealer else 0

        # Handle automatic dealer draw
        if reveal_dealer and dealer_score < 17 and not hand_active:
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            dealer_score = calculate_score(dealer_hand)

        # Auto-stand if bust
        if hand_active and player_score >= 21:
            hand_active = False
            reveal_dealer = True

        # Only check outcome if dealer's hand is revealed and player is done
        if reveal_dealer and not hand_active:
            if player_score > 21:
                outcome = 3  # Player busts
            elif dealer_score > 21:
                outcome = 1  # Dealer busts, player wins
            elif player_score > dealer_score:
                outcome = 1  # Player wins
            elif player_score < dealer_score:
                outcome = 3  # Dealer wins
            else:
                outcome = 2  # Draw (Push)

            # Apply betting results
            if add_score:
                if outcome == 1:
                    current_money += total_bet_amount * 2  # Win: double the bet
                    total_bet_amount = 0
                    pygame.time.wait(1000)
                    state = BETTING
                elif outcome == 2:
                    current_money += total_bet_amount  # Draw: return bet
                    total_bet_amount = 0
                    pygame.time.wait(1000)
                    state = BETTING
                elif outcome == 3:
                    total_bet_amount = 0
                    pygame.time.wait(1000)
                    state = BETTING

                add_score = False
        # Redraw everything
        display.fill(Green)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        draw_scores(player_score, dealer_score)
        buttons = draw_game(active, records, outcome)
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





