import random
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from fpdf import FPDF

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
            return picked_card
"else, pick up a card, not done yet"

def log_play(deck, card, player):
    #Update after every turn
    game_logs.append({
        "player": player,
        "deck_before": len(deck),
        "played_card": card,
        "deck_after": deck
    })

def generate_game_pdf(filename="game_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Uno Game Summary", ln=True, align='C')
    pdf.ln(10)


