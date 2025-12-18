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
test_deck=["red 5", "blue 2", "green 9", "yellow 0",
           "grey 4", "red 7", "blue 1", "green 2"]

menu_options={"start":Menu.start_game,
              "wildcards":Menu.wildcards,
              "players": Menu.player_selection,
              "exit":Menu.exit_game}


#List of wildcards available, will not be changed, acts as a template
wildcard_options=["skip", "reverse", "two", "wild", "four", "swap"]
#All active by default
current_wildcards=["skip", "reverse", "two", "wild", "four", "swap"]
#The main deck that will be used to get cards from
main_deck=[]
#The amount of actual players playing
player_count=1
#Holds all player classes, indexes are used as player numbers
players=[]

#Decides when to go into the game and when to stop, when someone gets rid of their deck
play_game=False

#Direction of turn, starts off going forward unless a reverse card is placed
turn=1

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

while play_game:
    #Making the player classes
    #Making the players real based on total amount of players selected in menu
    for i in range (4):
        #used to store the deck before assigning it
        temp_deck=[]
        #Grab 7 cards from the main deck
        for i in range (7):
            temp_deck.append(main_deck.pop(0))
        if player_count>i:
            players.append(Player(temp_deck,False))
        else:
            players.append(Player(temp_deck, True))

    



