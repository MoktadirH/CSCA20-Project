import time
from rich.progress import track

"""
Contains all menu functions, which includes starting the game, settings, changing wildcards and choosing amount of players.
The game will not start until the player chooses the "start" option from the menu.
"""

def player_selection() -> int:
    while True:
        try:
            num_players = int(input("Enter number of players (1-4): "))
            if 1 <= num_players <= 4:
                return num_players
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def wildcards(template,current) -> list:
    """
    Allows the user to change the wildcard selection, they can either choose to remove or add a wildcard into the pool
    Function returns the wildcard of interest and whether to add or remove it
    """
    #Keep asking until a proper response is given
    while True:
        #Clears the console
        print("\033[H\033[2J")
        print(f"Current wildcards: {', '.join(current)}")
        action = input("Would you like to add or remove a wildcard? (add/remove or exit to leave): ").strip().lower()
        if action != "add" and action != "remove":
            print("Invalid action. Please enter 'add' or 'remove'.")
        elif action == "exit":
            return current
        else:
            #While loop until proper answer is given
            while True:
                wildcard_name = input("Enter the name of the wildcard: ")
                if wildcard_name in template and action == "remove" and wildcard_name in current:
                    del current[current.index(wildcard_name)]
                    print(f"{wildcard_name} has been removed from the wildcard pool.")
                    return current
                elif wildcard_name in template and action == "add" and wildcard_name not in current:
                    current.append(wildcard_name)
                    print(f"{wildcard_name} has been added to the wildcard pool.")
                    return current
                elif wildcard_name in template and action == "remove" and wildcard_name not in current:
                    print(f"{wildcard_name} is not in the current wildcard pool. Try again.")
                    return current
                elif wildcard_name in template and action == "add" and wildcard_name in current:
                    print(f"{wildcard_name} is already in the current wildcard pool. Try again.")
                    return current
                else:
                    print("Invalid wildcard name. Please try again.")
        print("\033[H\033[2J")

def start_game():
    #Creates a loading bar before starting the game, transition
    for _ in track(range(100), description="[green]Starting Game..."):
        time.sleep(0.02)

def settings(template,current):
    #Ignore parameters, only used for consistency in main.py
    pass

def exit_game(template,current):
    #Ignore parameters, only used for consistency in main.py
    #Same transition for a smooth exit
    for _ in track(range(100), description="[red]Closing Game..."):
        time.sleep(0.01)
    quit()