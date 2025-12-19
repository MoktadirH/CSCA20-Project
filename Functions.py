import random
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns
from fpdf import FPDF


colors = {
    "red": "[red]",
    "green": "[green]",
    "yellow": "[yellow]",
    "blue": "[blue]",
    "grey": "[grey]"
}
widcard_symbols={
    "skip": "⏭",
    "reverse": "↔",
    "two": "+",
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
    for wildcard in wildcards:
        #4 of each wildcard
        for i in range(4):
            deck.append("grey " + wildcard)
    return deck


def ShowHands (deck, template, picked_card):
    """
    This function takes in a player's deck as well as the last played card and shows it in a card format.
    It uses the a template so that cards look conistent, with the only change being the number/symbol inside.
    The function does not return anything as it just prints to the console and does not change anything.
    """
    #[/] turns the color off so that it does not leak later
    hand_lines = ["[bold cyan]Your hand:[/]\n"]
    for i in range(0, len(deck), 5):
        row = deck[i:i+5]
        for line in template:
            line_sections = []
            for each in row:
                hand_color, hand_card = each.split(" ")
                #If it is a wildcard, replace the card name with the. Will always be grey too
                if hand_color=="grey":
                    #card variable is what will appear on the card, hand_card is used for internal code
                    card=widcard_symbols.get(hand_card)
                else:
                    card=hand_card
                card_color=colors.get(hand_color.strip())
                card_line = card_color + line.replace("x", str(card)) + "[/]"
                line_sections.append(card_line)
            #Join individual card line with a space
            hand_lines.append("  ".join(line_sections))
    #joins the line of the hand together with a new line, also turns them into a string
    hand_text = "\n".join(hand_lines)
    panel = Panel(hand_text, title="Player Hand", border_style="green")
    
    #Making the card for the last played card and putting it in a panel
    picked_color,picked_number=picked_card.split(" ")
    #After wildcard is placed, the color changes so we need to see if the number appears in the wildcard dictionary
    if picked_number in widcard_symbols:
        picked_number=widcard_symbols.get(picked_number)
    picked_card_color=colors.get(picked_color)
    picked_card_lines=[]
    for line in template:
        card_line = picked_card_color + line.replace("x", str(picked_number)) + "[/]"
        picked_card_lines.append(card_line)
    picked_card_text = "\n".join(picked_card_lines)
    picked_panel = Panel(picked_card_text, title="Last Played Card", border_style="red")
    
    #Put the two panels into columns so that it shows up side by side
    console.print(Columns([panel,picked_panel]))

#Return a tuple of the deck and the last played card
def pick_card(deck, bot, current_card,pile) -> tuple:
    """
    This function makes the player pick a card from their deck or draw a card if they like to. If the player is a bot
    it automatically picks a card for them by finding which cards can be placed. The function takes in the player's deck,
    if they are a bot or not, the last card that was placed and the middle pile if they want to draw from.
    the function returns a tuple of both the player's deck and the newly last placed card.
    """
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
                picked_card=new_color +" "+ picked_card.split(" ")[1]
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
                        if color!="grey" and (color == current_color or number == current_number):
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


def log_play(deck, player, card,turn):
    """Update after every turn and adds a dictionary as an index in a list. Takes in the
    player's deck, player and turn number, and the card played."""
    if deck is None:
        game_logs.append({
            "player":player,
            "played_card":card,
            "deck":[],
            "turn":turn,
        })
    else:
        game_logs.append({
        "player":player,
        "played_card":card,
        "deck":deck.copy(),
        "turn":turn,
        })

def generate_game_pdf(winner):
    """
    Using a game log that was tracking every move, it creates a PDF with each turn's details so that the move can be traced back.
    It also shows the whole match so that player's can analyze their moves and see what they could've changed.
    The function does not return anything but outputs a PDF file in the folder of the python files.
    """
    pdf = FPDF()
    pdf.add_page()
    #Spacing margins, left, top and right side
    pdf.set_margins(15, 15, 20)
    pdf.set_font("Arial", "B", 16)
    #Cell acts as a line on the pdf, aligned to the center
    pdf.cell(0, 15, txt="Uno Game Activity", ln=True, align="C")
    #Spacing
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    #Aligned to the left margin. A heading for the logs
    pdf.cell(0, 10, txt="Turn Log", ln=True, align="L")
    pdf.ln(5)
    #Make font smaller for logs compared to heading and title
    pdf.set_font("Arial", size=11)
    for log in game_logs:
        #Soft purple color to make the pdf look visually pleasing. Only shows up when fill=True
        pdf.set_fill_color(188, 189, 211)
        pdf.cell(0, 10, f"Player {log['player']}: Turn {log.get('turn')}", ln=True, fill=True)
        pdf.cell(0, 10, f"Placed Card: {log['played_card']} | Cards left: {len(log['deck'])}", ln=True)
        pdf.multi_cell(0, 10, f"Deck: {', '.join(log['deck'])}", ln=True)
        pdf.ln(2)
    #Winner has been declared to a player
    if winner !=0:
        #Bolder and larger font to add emphasis at the end
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0,8, f"Player {winner} has won the game!", ln=True, fill=True)
    pdf.output("activity_log.pdf")


