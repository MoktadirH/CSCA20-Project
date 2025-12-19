def skip(turn_index, direction):
    if direction == 1:
        turn_index += 1
    else:
        turn_index -= 1
    return turn_index
def reverse(direction):
    #positive=negative and negative=positve
    #siwtches the direction
    return direction * -1
def draw_cards(player_deck, main_deck, number_of_cards):
    for i in range (number_of_cards):
        player_deck.append(main_deck.pop(0))
    return player_deck
def color_swap(new_color):
    return new_color + "swap"
"""
for draw two and draw four, get the deck from the player class plus the main deck and get 4 from the main deck
and add it to the player deck
return the new player deck
"""


