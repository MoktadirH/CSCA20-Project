import random
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from fpdf import FPDF
#We need this when players or a bot chooses a card and it is a wildcard
import Wildcards

colors = {
    "red": "[red]",
    "green": "[green]",
    "yellow": "[yellow]",
    "blue": "[blue]",
    "grey": "[grey]"
}

console = Console()
#keep track of decks after every turn for game log
game_logs = []

def makeDeck(wildcards) -> list:
    """
    This function makes the deck that is in the "middle" of the table. It takes in the wildcards that were selected
    and makes a deck with 2 copies of each card and 4 of each wildcard.
    The function takes a wildcard parameter and returns a list with all the cards
    """
    deck = []
    #Goes through all the colors for the regular cards
    for color in ["red", "green", "yellow", "blue", "grey"]:
        #For each color, it makes cards numbered 0-9
        for number in range(0, 10):
            #Makes two of each card
            deck.append(f"{color} {number}")
            deck.append(f"{color} {number}")
    #Adds the wildcards
    for wildcard in wildcards:
        #4 of each wildcard
        for i in range(4):
            deck.append(wildcard)


def ShowHands (deck, template):
    #[/] turns the color off so that it does not leak later
    hand_lines = ["[bold cyan]Your hand:[/]\n"]
    for i in range(0, len(deck), 5):
        row = deck[i:i+5]
        for line in template:
            line_sections = []
            for each in row:
                color, card = each.split(" ")
                card_color=colors.get(color)
                card_line = card_color + line.replace("x", str(card)) + "[/]"
                line_sections.append(card_line)
            #Join individual card line with a space
            hand_lines.append("  ".join(line_sections))
    #joins the line of the hand together with a new line, also turns them into a string
    hand_text = "\n".join(hand_lines)
    panel = Panel(hand_text, title="Player Hand", border_style="red")
    console.print(panel)

def pick_card(deck, bot, current_card,pile) -> list:
    if bot:
        #Pick a random card that is allowed
        possible_cards=[]
        current_color, current_number = current_card.split(" ")
        for card in deck:
            color, number = card.split(" ")
            if color == current_color or number == current_number:
                possible_cards.append(card)
        if possible_cards:
            picked_card=random.choice(possible_cards)
            if picked_card.split(" ")[0]=="grey":
                #assign wildcard abilities and choose a random color
                new_color=random.choice(["red","green","blue","yellow"])
                picked_card=new_color + picked_card.split(' ')[1]
            deck.remove(picked_card)
            last_card=picked_card
            return deck
        else:
            return deck.append(pile.pop(0))
    else:
        while True:
            try:
                choice=input("Choose a card by entering the position or type 'draw' to pick up a card: ")
                if choice.lower() == "draw":
                    deck.append(pile.pop(0))
                    return deck
                else:
                    #Len returns the actual size and the highest number will give an index error
                    if 0 <=int(choice)-1 <= len(deck)-1:
                        chosen_card=deck[int(choice)-1]
                        color, number = chosen_card.split(" ")
                        current_color, current_number = current_card.split(" ")
                        #grey means that it is a wildcard and can be placed anytime
                        if color == current_color or number == current_number:
                            deck.remove(chosen_card)
                            last_card=chosen_card
                            return deck
                        if color == "grey":
                            deck.remove(chosen_card)
                            #wildcard can change colors, ask for new color
                            new_color = input("You have played a wildcard! Choose a new color (red, green, blue, yellow): ").strip().lower()
                            #if a plus 4 is placed and they choose green, the last card will be green (plus) four, not green 4
                            last_card=f"{new_color} {number}"
                        else:
                            print("You cannot play that card. Try again.")
            except:
                print("Invalid input. Please try again.")
                continue

            

"else, pick up a card, not done yet"

def log_play(deck, card, player):
    #Update after every turn
    game_logs.append({
        "player": player,
        "deck_length": len(deck),
        "played_card": card,
        "deck": deck
    })

def generate_game_pdf(filename="game_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Uno Game Summary", ln=True, align='C')
    pdf.ln(10)


