import Functions
import Menu
import time
import random

class Player ():
    def __init__(self, deck, bot):
        self.deck = deck
        self.bot = bot


#variables to run the game properly
card_template=[
"╭══════╮",
"║      ║",
"║  x   ║",
"║      ║",
"╰══════╯"
]
menu_options={"start":Menu.start_game,
              "wildcards":Menu.wildcards,
              "players": Menu.player_selection,
              "exit":Menu.exit_game}


#List of wildcards available, will not be changed, acts as a template
wildcard_options=["skip", "reverse", "two", "wild", "four", "swap"]
#All active by default
current_wildcards=["skip", "reverse", "two", "wild", "four", "swap"]
#The main deck that will be used to get cards from, global so it can be accessed by all files
global main_deck
main_deck=[]
last_card=""
#The amount of actual players playing
player_count=1
#Holds all player classes, indexes are used as player numbers
players=[]

#Decides when to go into the game and when to stop, when someone gets rid of their deck
play_game=False

#Direction and the turn, starts off going forward unless a reverse card is placed
turn=0
direction=1
turn_count=1

debug=0



#Loop just for menu
while True:
    #Clear Console
    print("\033[H\033[2J")
    print("Main Menu:")
    for option in menu_options:
        print(f"- {option}")
    choice = input("Select an option: ").strip().lower()
    if choice in menu_options and choice != "start":
        #Every function are given these pararmeters even if not used to make code more efficient
        menu_options[choice](wildcard_options, current_wildcards)
    elif choice == "start":
        menu_options[choice]()
        play_game=True
        #Make the deck based on wildcards and shuffle it
        main_deck=Functions.makeDeck(current_wildcards)
        random.shuffle(main_deck)
        break
    else:
        print("Invalid option. Please try again.")
        #Allow people to see message before refreshing the console
        time.sleep(0.9)

#Making the player classes
#Making the players real based on total amount of players selected in menu
for i in range (4):
    #used to store the deck before assigning it
    temp_deck=[]
    #Grab 7 cards from the main deck
    for j in range (7):
        temp_deck.append(main_deck.pop(0))
    if player_count>i:
        players.append(Player(temp_deck,False))
    else:
        players.append(Player(temp_deck, True))
#Grab a card for the middle to start with
last_card=main_deck.pop(0)

while play_game:
    #Wipe the console each time to make it neat
    print("\033[H\033[2J")
    #Display who's turn it is so the player knows, only if the current player is not a bot
    if not players[turn].bot:
        print(f"It is player {turn+1}'s turn. Look away if it is not your turn!")
        time.sleep(1)
        print("\033[H\033[2J")
        #Show the current player's hand
        Functions.ShowHands(players[turn].deck, card_template,last_card)
    #At this point, the last card will be replaced by the new card and the old one will be readded back to the deck randomly
    main_deck.insert(random.randint(0, len(main_deck)-1), last_card)
    players[turn].deck,last_card=Functions.pick_card(players[turn].deck, players[turn].bot, last_card, main_deck)
    Functions.log_play(players[turn].deck, last_card, turn+1,turn_count)
    if players[turn].deck==[]:
        play_game=False
        print(f"Player {turn+1} has won the game!")
        Functions.generate_game_pdf()
        break
    else:
        if turn==3:
            turn=0
        else:
            turn=turn+1
    turn_count+=1
Functions.generate_game_pdf()