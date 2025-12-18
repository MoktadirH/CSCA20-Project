import Functions
import Menu
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
              "exit":Menu.exit_game}


#List of wildcards available, will not be changed, acts as a template
wildcard_options=["skip", "reverse", "draw two", "wild", "draw four", "swap hands"]
#All active by default
current_wildcards=["skip", "reverse", "draw two", "wild", "draw four", "swap hands"]

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
        menu_options[choice]
        break
    else:
        print("Invalid option. Please try again.")


#Loop for the actual game



Functions.ShowHands(test_deck,False , card_template)
