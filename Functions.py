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
wildcard_symbols={
    "skip": "⏭",
    "reverse": "↔",
    "two": "+",
    "wild": "*",
    "four": "#",
    "swap": "↩"}

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
    for color in ["red", "green", "yellow", "blue"]:
        #For each color, it makes cards numbered 0-9
        for number in range(0, 10):
            #Makes two of each card
            deck.append(color + " " + str(number))
            deck.append(color + " " + str(number))
    #Adds the wildcards
    """for wildcard in wildcards:
        #4 of each wildcard
        for i in range(4):
            deck.append("grey " + wildcard)"""
    return deck


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

#Return a tuple of the deck and the last played card
def pick_card(deck, bot, current_card,pile) -> tuple:
    if bot:
        #Pick a random card that is allowed
        possible_cards=[]
        current_color, current_number = current_card.split(" ")
        for card in deck:
            color, number = card.split(" ")
            if color == current_color or number == current_number or color=="grey":
                possible_cards.append(card)
        if possible_cards:
            picked_card=random.choice(possible_cards)
            deck.remove(picked_card)
            if picked_card.split(" ")[0]=="grey":
                #assign wildcard abilities and choose a random color
                new_color=random.choice(["red","green","blue","yellow"])
                picked_card=new_color +" "+ picked_card.split(' ')[1]
            last_card=picked_card
            return (deck,last_card)
        else:
            deck.append(pile.pop(0))
            return (deck, current_card)
    else:
        while True:
            try:
                choice=input("Choose a card by entering the position or type 'draw' to pick up a card: ")
                if choice.lower() == "draw":
                    deck.append(pile.pop(0))
                    return (deck, current_card)
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
                            return (deck,last_card)
                        if color == "grey":
                            deck.remove(chosen_card)
                            while True:
                                #wildcard can change colors, ask for new color
                                new_color = input("You have played a wildcard! Choose a new color (red, green, blue, yellow): ").strip().lower()
                                if new_color in ["red", "green", "blue", "yellow"]:
                                    #if a plus 4 is placed and they choose green, the last card will be green (plus) four, not green 4
                                    last_card=new_color+" "+number
                                    return (deck,last_card)
                                else:
                                    print("Invalid color. Please try again.")
                        else:
                            print("You cannot play that card. Try again.")
            except:
                print("Invalid input. Please try again.")
                continue

            

"else, pick up a card, not done yet"

def log_play(deck, card, player,turn):
    #Update after every turn, a dictionary as an index in a list
    if deck is None:
        game_logs.append({
            "player": player,
            "deck_length": 0,
            "played_card": card,
            "deck": [],
            "turn": turn
        })
    else:
        game_logs.append({
        "player": player,
        "deck_length": len(deck),
        "played_card": card,
        "deck": deck.copy()
        })

def generate_game_pdf(filename="game_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    #Spacing margins
    pdf.set_margins(15, 15, 15)
    pdf.set_font("Arial", "B", 16)
    #Code for blue
    pdf.set_text_color(0, 0, 128)
    pdf.cell(200, 15, txt="Uno Game Summary", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt="Game Activity Log", ln=True, align='L')
    pdf.ln(5)
    pdf.set_font("Arial", size=11)
    for log in game_logs:
        pdf.set_fill_color(240, 240, 240)  # Light gray background for each log entry
        pdf.cell(200, 8, txt=f"Player {log['player']}: Turn {log.get('turn')}", ln=True, fill=True)
        pdf.cell(200, 8, txt=f"Played: {log['played_card']} | Cards left: {log['deck_length']}", ln=True)
        pdf.multi_cell(200, 8, txt=f"Deck: {', '.join(log['deck'])}", ln=True)
        pdf.ln(2)  # Small space between entries
    pdf.output("activity_log.pdf")


