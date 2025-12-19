import Functions
import Menu
import time
import random


#variables to run the game properly
card_template=[
"╭══════╮",
"║      ║",
"║  x   ║",
"║      ║",
"╰══════╯"
]

#Menu options on console and what function they are linked to
menu_options={"start":Menu.start_game,
              "wildcards":Menu.wildcards,
              "players": Menu.player_selection,
              "exit":Menu.exit_game}

#List of wildcards available, will not be changed, acts as a template
wildcard_options=["skip", "reverse", "two", "four", "swap"]
#All active by default
current_wildcards=["skip", "reverse", "two", "four", "swap"]
#The main deck that will be used to get cards from, global so it can be accessed by all files
global main_deck
main_deck=[]
last_card=""
#The amount of actual players playing
player_count=0
#Holds all player classes, indexes are used as player numbers
players=[]

#Decides when to go into the game and when to stop, when someone gets rid of their deck
play_game=False

#Direction and the turn, starts off going forward unless a reverse card is placed
turn=0
direction=1
turn_count=1

class Player ():
    def __init__(self, deck, bot):
        self.deck = deck
        self.bot = bot

def next_turn(current_turn, direction) ->int:
    """
    This function takes in the current turn and the direction and returns an integer of what the next turn would be.
    Useful for when a skip card is played or to know 
    """
    if direction==1:
        if current_turn==3:
            return 0
        else:
            return current_turn+1
    else:
        if current_turn==0:
            return 3
        else:
            return current_turn-1

#Loop just for menu
while True:
    #Clear Console
    print("\033[H\033[2J")
    print("Main Menu:")
    for option in menu_options:
        print(f"- {option}")
    choice = input("Select an option: ").strip().lower()
    if choice == "start":
        menu_options[choice]()
        play_game=True
        #Make the deck based on wildcards and shuffle it
        main_deck=Functions.makeDeck(current_wildcards)
        random.shuffle(main_deck)
        break
    elif choice == "exit":
        menu_options[choice]()
    elif choice == "wildcards":
        #Every function are given these pararmeters even if not used to make code more efficient
        current_wildcards=menu_options[choice](wildcard_options, current_wildcards)
    elif choice == "players":
        print("players")
        player_count=menu_options[choice]()
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
    #For loop starts from 0 not 1, so player count is adjusted
    if (player_count-1)>=i:
        players.append(Player(temp_deck,False))
    else:
        players.append(Player(temp_deck, True))
    print(temp_deck)
#Grab a card for the middle to start with
last_card=main_deck.pop(0)

while play_game:
    #Wipe the console each time to make it neat
    print("\033[H\033[2J")
    #Display who's turn it is so the player knows, only if the current player is not a bot
    if not players[turn].bot:
        print(f"It is player {turn+1}'s turn. Look away if it is not your turn!")
        #Pause the code for 2.5 seconds so the user can read the message
        time.sleep(2.5)
        print("\033[H\033[2J")
        #Show the current player's hand
        Functions.ShowHands(players[turn].deck, card_template,last_card)
    else:
        print(f"It is player {turn+1}'s turn. They are automatically taking their turn!")
        time.sleep(0.5)
    #At this point, the last card will be replaced by the new card and the old one will be readded back to the deck randomly
    main_deck.insert(random.randint(0, len(main_deck)-1), last_card)
    players[turn].deck,last_card=Functions.pick_card(players[turn].deck, players[turn].bot, last_card, main_deck)
    #Handle effects of wildcards, swap is not mentioned as it is handled in the pick_card function as all wildcards need to change colors
    if last_card.split(" ")[1]=="four":
        for i in range (4):
            players[next_turn(turn,direction)].deck.append(main_deck.pop(0))
    elif last_card.split(" ")[1]=="two":
        for i in range (2):
            players[next_turn(turn,direction)].deck.append(main_deck.pop(0))
    elif last_card.split(" ")[1]=="reverse":
        direction*=-1
    elif last_card.split(" ")[1]=="skip":
        #Takes an additional turn before the normal next turn change, skipping a player
        turn=next_turn(turn,direction)
    Functions.log_play(players[turn].deck, turn+1, last_card, turn_count)
    if players[turn].deck==[]:
        play_game=False
        print(f"Player {turn+1} has won the game!")
        Functions.generate_game_pdf(turn+1)
    else:
        turn=next_turn(turn,direction)
        turn_count+=1
        Functions.generate_game_pdf(0)