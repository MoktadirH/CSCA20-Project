import Functions
card_template=[
"╭══════╮",
"║      ║",
"║  x   ║",
"║      ║",
"╰══════╯"
]
test_deck=["red 5", "blue 2", "green 9", "yellow 0",
           "grey 4", "red 7", "blue 1", "green 2"]
colors={
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "grey": "\033[90m",
    "default": "\033[0m"}

"""menu_options={"start":functions.start_game,
              "settings":functions.settings,
              "wildcards":functions.wildcards,
              "exit":functions.exit_game}

class Person (deck, bot):
    self.deck = deck
    self.bot=bot"""

Functions.ShowHands(test_deck,False , card_template, colors)




print("hello")