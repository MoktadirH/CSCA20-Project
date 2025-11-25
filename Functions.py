import random
def ShowHands (deck, bot, template, colors):
    print("Your hand: ")
    for i in range(0, len(deck), 5):
        row = deck[i:i+5]
        for line in template:
            line_sections = []
            for each in row:
                color, card = each.split(" ")
                card_line = colors[color] + line.replace("x", str(card)) + colors["default"]
                line_sections.append(card_line)
            print("  ".join(line_sections))
    print(colors["default"])

def pick_card(deck, bot, current_card):
    if bot:
        #Pick a random card that is allowed
        possible_cards=[]
        for card in deck:
            color, number = card.split(" ")
            current_color, current_number = current_card.split(" ")
            if color == current_color or number == current_number:
                possible_cards.append(card)
        if possible_cards:
            picked_card=random.choice(possible_cards)
            deck.remove(picked_card)
            return picked_card, deck