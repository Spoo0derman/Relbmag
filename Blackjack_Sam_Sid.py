import pygame, random, Game, Menu, Betting, copy, End


from pygame.examples.moveit import GameObject

pygame.init()
pygame.mixer.init()
pygame.joystick.init()

#variablen für die allgemeine Bildschrimdarstellung
WIDTH, HEIGHT = 900, 800
display = pygame.display.set_mode([WIDTH, HEIGHT])


# Prüfen, ob ein Controller angeschlossen ist, sonst funktioniert es nicht.
# Wir haben es auch so gemacht, dass es nicht funktioniert, wenn er eingesteckt ist, bevor das Spiel startet.
if pygame.joystick.get_count() > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()
else:
    controller = None

# Diese Codezeile ist sehr wichtig, da sie uns erlaubt zu prüfen, ob eine Taste gedrückt wurde.
button_pressed = False

# Alle musik wird hier geladen
lobby_music = pygame.mixer.Sound("Audio/lobby_music.mp3")
main_music = pygame.mixer.Sound("Audio/main_music.mp3")
win_music = pygame.mixer.Sound("Audio/Here comes the money - meme [ ezmp3.co ].mp3")
loss_music = pygame.mixer.Sound("Audio/Sad Trombone - Sound Effect (HD).mp3")

# In diesen 2 Codeblöcken fügen wir die meisten unserer Sprites und Bilder ein.

home_Screen = pygame.image.load("Sprites/19-playing-cards-png.png").convert_alpha()
home_Screen = pygame.transform.scale_by(home_Screen, 0.3)
poker_Chips = pygame.image.load("Sprites/chips-poker 1-Photoroom.png").convert_alpha()
poker_Chips = pygame.transform.scale_by(poker_Chips, 0.4)

x_button = pygame.image.load("Sprites/Screenshot_2025-03-25_103206-removebg-preview.png").convert_alpha()
x_button = pygame.transform.scale_by(x_button, 0.2)
O_button = pygame.image.load("Sprites/Screenshot_2025-03-25_103112-removebg-preview.png").convert_alpha()
O_button = pygame.transform.scale_by(O_button, 0.2)
square_button = pygame.image.load("Sprites/Screenshot_2025-03-25_103052-removebg-preview.png").convert_alpha()
square_button = pygame.transform.scale_by(square_button, 0.2)
triangle_button = pygame.image.load("Sprites/Screenshot_2025-03-25_103122-removebg-preview.png").convert_alpha()
triangle_button = pygame.transform.scale_by(triangle_button, 0.2)

losing_image = pygame.image.load("Sprites/WompWomp.png").convert_alpha()
losing_image = pygame.transform.scale_by(losing_image, 0.3)
winning_image = pygame.image.load("Sprites/mikeyross.jpeg").convert()
winning_image = pygame.transform.scale_by(winning_image, 0.3)

# Das ist der Code für unsere Überschrift oben auf dem Fenster
pygame.display.set_caption("BLACKJACK - Sam & Sid")

# Hier definieren wir genauere Farben, die wir immerwieder benutzen möchten. Sie kommen hauptsächlich in den verschiedenen Game-States vor.
Green = (0, 50, 0)
White = (255, 255, 255)
Red = (255, 0, 9)
Blue = (0, 255, 170)
Purple = (240, 0, 255)

#Unsere Game States. Hier setzen wir auch unseren Status auf Menu
MENU = 0
BETTING = 1
GAME = 2
END = 3
state = MENU

#Fonts
small_font = pygame.font.SysFont('Impact', 50)
small_font_1 = pygame.font.SysFont('Impact', 45)
small_font_cards = pygame.font.SysFont('Times New Roman', 40)
final_font = pygame.font.SysFont('Comic Sans MS', 55)
final_font_Trevor = pygame.font.SysFont('Comic Sans MS', 40)

#Betting variables
total_bet_amount = 0
total_displayed = small_font_1.render("$" + str(total_bet_amount), True, (0, 255, 170))
current_money = 500
money_displayed_betting_screen = small_font.render("$" + str(current_money), True, (240, 0, 255))

# GAME variables
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
    display.blit(small_font.render(f'You: {player}', True, 'white'), (350, 400))
    if reveal_dealer:
        display.blit(small_font.render(f'Dealer: {dealer}', True, 'white'), (350, 100))

def draw_cards(player, dealer, reveal):
    # Draw player cards
    for i in range(len(player)):
        x = 400 + (70 * i)
        y = 460 + (5 * i)
        pygame.draw.rect(display, 'white', [x, y, 120, 220], 0, 5)
        display.blit(small_font_cards.render(player[i], True, 'black'), (x + 30, y + 5))
        display.blit(small_font_cards.render(player[i], True, 'black'), (x + 30, y + 170))
        pygame.draw.rect(display, 'red', [x, y, 120, 220], 5, 5)

    # Draw dealer cards
    for i in range(len(dealer)):
        x = 400 + (70 * i)
        y = 160 + (5 * i)
        pygame.draw.rect(display, 'white', [x, y, 120, 220], 0, 5)

        if i != 0 or reveal:
            display.blit(small_font_cards.render(dealer[i], True, 'black'), (x + 30, y + 5))
            display.blit(small_font_cards.render(dealer[i], True, 'black'), (x + 30, y + 170))
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

        if current_money >= total_bet_amount:

            pygame.draw.rect(display, 'white', [0, 700, 900, 100], 0, 5)

            double_down_text = small_font_1.render('DOUBLE DOWN', True, 'black')
            display.blit(double_down_text, (340, 730))
            display.blit(triangle_button, (240, 705))

            hit_text = small_font_1.render('       HIT', True, 'black')
            display.blit(hit_text, (75, 730))
            display.blit(square_button, (15, 700))

            stand_text = small_font_1.render('      STAND', True, 'black')
            display.blit(stand_text, (695, 730))
            display.blit(O_button, (630, 695))

        else:

            pygame.draw.rect(display, 'white', [185, 700, 600, 100], 0, 5)

            hit_text = small_font_1.render('     HIT', True, 'black')
            display.blit(hit_text, (250, 730))
            display.blit(square_button, (190, 700))


            stand_text = small_font_1.render('      STAND', True, 'black')
            display.blit(stand_text, (580, 730))
            display.blit(O_button, (510, 695))




    if outcome == 1:
        display.blit(small_font_1.render("You Win", True, 'gold'), (15, 25))
        display.blit(triangle_button, [50, 300])
        display.blit(small_font_1.render("Keep going!", True, 'white'), (15, 225))
        display.blit(small_font_1.render("To bet again", True, 'white'), (15, 400))
    elif outcome == 3:
        display.blit(small_font_1.render("You Lose", True, 'red'), (15, 25))
        display.blit(triangle_button, [50, 300])
        display.blit(small_font_1.render("Can't end on a loss!", True, 'white'), (15, 225))
        display.blit(small_font_1.render("To bet again", True, 'white'), (15, 400))

    elif outcome == 2:
        display.blit(small_font_1.render("Draw", True, 'gray'), (15, 25))
        display.blit(triangle_button, [50, 300])
        display.blit(small_font_1.render("Basically a loss", True, 'white'), (15, 225))
        display.blit(small_font_1.render("To bet again", True, 'white'), (15, 400))



    return button_list



# check endgame conditions function




def start_new_game():
    global game_deck, my_hand, dealer_hand, outcome, hand_active, reveal_dealer, add_score, dealer_score, player_score, initial_deal
    game_deck = copy.deepcopy(decks * single_deck) #global means that these variables can be modified outside of this area when the fuction is called, in other words it allows them to be updated outside the fuction and be used inside modified.
    my_hand = []
    dealer_hand = []
    outcome = 0
    hand_active = True
    reveal_dealer = False
    add_score = True
    dealer_score = 0
    player_score = 0
    initial_deal = True


# This simply starts our music
lobby_music.play()

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

        if event.type == pygame.JOYBUTTONDOWN and controller and not button_pressed:
            if event.button == 0:  # "X" button on PS controller (or adjust for Xbox)
                state = BETTING
                print("State: Betting")
                button_pressed = True
        if event.type == pygame.JOYBUTTONUP and controller:
            button_pressed = False
        pygame.display.flip()
    # Display different screens based on state

    while state == BETTING:
        Betting.set_betting(display=display, Green=Green, poker_Chips=poker_Chips, small_font=small_font, White=White, O_button=O_button, square_button=square_button, triangle_button=triangle_button, x_button=x_button, total_bet_amount=total_bet_amount)
        total_displayed = small_font_1.render("$" + str(total_bet_amount), True, Blue)
        money_displayed_betting_screen = small_font.render("$" + str(current_money), True, Purple)
        display.blit(money_displayed_betting_screen, (50, 50))
        display.blit(total_displayed, (355, 250))
        lobby_music.fadeout(4000)
        win_music.stop()
        loss_music.stop()
        main_music.play()
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
            if event.type == pygame.JOYBUTTONDOWN and controller and not button_pressed:
                if event.button == 0 and total_bet_amount > 0:  # "X" button on PS controller (or adjust for Xbox)
                    state = GAME
                    entered_game_state = True
                    button_pressed = True
                    break
            if event.type == pygame.JOYBUTTONDOWN and controller and not button_pressed:
                if event.button == 2:
                    if current_money - 50 >= 0:
                        total_bet_amount += 50
                        total_displayed = small_font_1.render("$" + str(total_bet_amount), True, Blue)
                        current_money -= 50
                        money_displayed_betting_screen = small_font.render("$" + str(current_money), True, Purple)
                    button_pressed = True
                elif event.button == 3:
                    if current_money - 100 >= 0:
                        total_bet_amount += 100
                        total_displayed = small_font_1.render("$" + str(total_bet_amount), True, Blue)
                        current_money -= 100
                        money_displayed_betting_screen = small_font.render("$" + str(current_money), True, Purple)
                    button_pressed = True
                elif event.button == 1:
                    if current_money - 250 >= 0:
                        total_bet_amount += 250
                        total_displayed = small_font_1.render("$" + str(total_bet_amount), True, Blue)
                        current_money -= 250
                        money_displayed_betting_screen = small_font.render("$" + str(current_money), True, Purple)
                    button_pressed = True
            if event.type == pygame.JOYBUTTONUP and controller:
                button_pressed = False
            display.blit(total_displayed, (355, 250))
            display.blit(money_displayed_betting_screen, (50, 50))
            pygame.display.flip()

    while state == GAME:
        Game.set_game(display, Green, small_font, White)
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
            Game.set_game(display, Green, small_font, White)
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

            if event.type == pygame.JOYBUTTONDOWN and controller and not button_pressed:
                if not active:
                    if event.button == 0:  # X - Start new hand
                        start_new_game()
                        button_pressed = True
                else:
                    if hand_active:
                        if event.button == 2 and player_score < 21:  # Square - Hit
                            my_hand, game_deck = deal_cards(my_hand, game_deck)
                            button_pressed = True
                        elif event.button == 1 and not reveal_dealer:  # Circle - Stand
                            reveal_dealer = True
                            hand_active = False
                            button_pressed = True
                        elif event.button == 3 and len(my_hand) == 2 and current_money >= total_bet_amount:
                            # Double the bet
                            current_money -= total_bet_amount
                            total_bet_amount *= 2

                            # Deal one card
                            my_hand, game_deck = deal_cards(my_hand, game_deck)

                            # Auto-stand
                            hand_active = False
                            reveal_dealer = True
                            button_pressed = True
            if event.type == pygame.JOYBUTTONUP and controller:
                button_pressed = False
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
        if reveal_dealer and not hand_active and player_score <= 21:
            while dealer_score < 17:
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
                reveal_dealer = True
                hand_active = False
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

                elif outcome == 2:
                    current_money += total_bet_amount  # Draw: return bet
                    total_bet_amount = 0

                elif outcome == 3:
                    total_bet_amount = 0

            add_score = False
            if current_money <= 0:
                state = END
                game_result = "Bankrupt"
            elif current_money >= 2500:
                state = END
                game_result = "Winner"


        if event.type == pygame.JOYBUTTONDOWN and controller and not button_pressed:
            if event.button == 3 and (outcome == 1 or outcome == 2 or outcome == 3):
                state = BETTING  # Move back to betting screen
                add_score = True
                button_pressed = True
        # Redraw everything
        display.fill(Green)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        draw_scores(player_score, dealer_score)
        buttons = draw_game(active, records, outcome)
        pygame.display.flip()

    while state == END:
        End.set_end(display=display, Green=Green, x_button=x_button, O_button=O_button, small_font_1=small_font_1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
                pygame.quit()
                break
            if event.type == pygame.JOYBUTTONDOWN and controller and not button_pressed:
                if event.button == 0:  # "X" button on PS controller (or adjust for Xbox)
                    button_pressed = True
                    state = MENU
                    current_money = 500
                    break
            if event.type == pygame.JOYBUTTONDOWN and controller and not button_pressed:
                if event.button == 1:
                    button_pressed = True
                    pygame.quit()
            if event.type == pygame.JOYBUTTONUP and controller:
                button_pressed = False
        if game_result == "Winner":
            display.blit(final_font.render("You've hit Relbmag status!", True, 'gold'),(65, 335))
            display.blit(final_font.render("$2500 to add to life savings!", True, 'gold'),(50, 395))
            display.blit(winning_image, (150, 15))
            main_music.fadeout(1000)
            win_music.play()
        elif game_result == "Bankrupt":
            display.blit(final_font.render("BANKRUPT!", True, 'red'),(285, 280))
            display.blit(final_font_Trevor.render("Grammy is upset you're friends with Trevor", True, 'red'),(30, 350))
            display.blit(losing_image, (275, 15))
            main_music.fadeout(1000)
            loss_music.play()
        pygame.display.flip()





