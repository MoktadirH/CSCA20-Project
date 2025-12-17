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

def change_wildcards(wildcard) -> list:
    """
    Allows the user to change the wildcard selection, they can either choose to remove or add a wildcard into the pool
    Function returns the wildcard of interest and whether to add or remove it
    """
    print(f"Current wildcards: {', '.join(wildcard)}")