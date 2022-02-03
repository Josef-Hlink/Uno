import random
import typing
from card import Card

class Player():
    """Parent class, contains all of the methods for a human player, and some methods
    that are shared among all three Player types: Human, Computer & Winner"""
    
    def __init__ (self, id: int):
        self.id: int = id # for differentiating between instances
        self.type: str = 'Human' # for differentiating between humans and computers
        self.hand: typing.List[Card] = [] # for keeping track of their hand
        self.calledUno: bool = False # for checking whether or not they called uno

    def choose_move(self, currentCard: Card) -> typing.Union[Card, str]:
        """Makes a human player choose a card (or other option) when it's their turn"""
        validInput = False
        while not validInput:
            try:
                inp = int(input('Choose option (enter number):\n>'))
                while not self.is_valid_choice(inp, currentCard): # move has to exist, and be valid
                    inp = int(input('Invalid (move)\nPlease enter one of the displayed numbers:\n>'))
                validInput = True
                if inp == len(self.hand) + 1: # Pass
                    return 'pass'
                elif inp == len(self.hand) + 2: # Uno Call
                    self.calledUno = True
                    validUnoCall = self.handle_uno_call(currentCard) # prints if valid or not
                    if validUnoCall:
                        validInput = False
                        continue # the player can now input the actual move they want to play
                    return 'wrongcall' # false Uno Call gets returned to Game class' function
            except ValueError:
                print('Please use a numerical value')
                continue
        choice = self.hand[inp-1]
        self.hand.remove(choice)
        return choice # returns the corresponding card

    def pick_colour(self) -> str:
        """Prompts a new colour to be picked (generally after playing a wildcard)"""
        colour: str = 'Purple'
        while colour.upper() not in ['BLUE', 'RED', 'GREEN', 'YELLOW']:
            colour = input('Pick a colour from:\nblue, yellow, green or red\n>')
            if colour.upper() == 'BLUE':
                return 'Blue'
            elif colour.upper() == 'RED':
                return 'Red'
            elif colour.upper() == 'GREEN':
                return 'Green'
            elif colour.upper() == "YELLOW":
                return 'Yellow'

    def is_valid_choice(self, choiceInput: int, topCard: Card) -> bool:
        """Checks whether a certain card can be played on the current top card,
        also checks if the the card is a valid last move (when there is only one move left"""
        if len(self.hand) == 1 and choiceInput == 1:
            card = self.hand[choiceInput-1]
            return card.is_valid_last_move(topCard)
        elif choiceInput == len(self.hand) + 1 or choiceInput == len(self.hand) + 2:
            return True # these correspond to Pass and Call Uno, so they are always valid choices
        try:
            card = self.hand[choiceInput-1]
            return card.is_valid_move(topCard)
        except IndexError: # for example, when the input would be hand size + 3
            return False

    def has_valid_move(self, topCard: Card) -> bool:
        """Checks if a player has any valid moves"""
        for card in self.hand:
            if card.is_valid_move(topCard):
                return True
        return False

    def has_card(self, card: Card) -> bool:
        """Checks if a player has a specific move"""
        for candidate in self.hand:
            if candidate == card:
                return True
            elif (card.colour == "*" and card.value == candidate.value) or \
               (card.value == "*" and card.colour == candidate.colour):
                return True
        return False

    def draw(self, cards: typing.List[Card]) -> None:
        """Makes a player draw one or multiple card(s)"""
        self.hand += cards
        return

    def receive_hand(self, hand: typing.List[Card]) -> None:
        """Initializes a player's hand"""
        self.hand = hand
        return

    def correct_uno_call(self, topCard: Card) -> bool:
        """Check if an uno call was correct"""
        return len(self.hand) <= 2 and self.has_valid_move(topCard)

    def handle_uno_call(self, currentCard: Card) -> bool:
        """Handle what happens when a player calls uno: prints information to the right"""
        if self.correct_uno_call(currentCard):
            print('-' * 64 + f'player {self.id} called uno correctly')
            return True
        else:
            print('-' * 64 + f'player {self.id} called uno incorrectly and has to draw 3 cards')
            return False

class Computer(Player):
    """Inherits some of the methods of human player, but some functions need to work automatically,
    so these are overridden by redefining them here."""
    def __init__(self, id: int):
        super().__init__(id)
        self.type: str = 'Computer' # for differentiating between humans and computers

    def choose_move(self, currentCard: Card) -> tuple:
        """Overrides Player's method"""
        if self.correct_uno_call(currentCard): # computer calls uno correctly every time
            self.calledUno = True
            self.handle_uno_call(currentCard)

        validMoves: list = []
        currentVal: str = currentCard.value

        if currentVal == 'Draw Four':
            for i in range(1, len(self.hand)+1):
                card = self.hand[i-1]
                if card.value == 'Draw Four':
                    validMoves.append(card)
        elif currentVal == 'Draw Two':
            for i in range(1, len(self.hand)+1):
                card = self.hand[i-1]
                if card.value == 'Draw Two':
                    validMoves.append(card)
        if not validMoves:
            for i in range(1, len(self.hand)+1):
                card = self.hand[i-1]
                if self.is_valid_choice(i, currentCard):
                    validMoves.append(card)

        print('COMPUTER MOVE')
        if not validMoves:
            return 'pass'
        choice = random.choice(validMoves)
        self.hand.remove(choice)
        return choice

    def pick_colour(self) -> str:
        """Makes the computer player picks a new colour, based on what it has most of in its hand"""
        choice, maxCount = 'Red', 0 # default choice has to be a colour, for if there's no colours left in hand
        coloursInHand: list = [card.colour for card in self.hand] # make a list with all of the colours
        for colour in ['Red', 'Yellow', 'Green', 'Blue']:
            count: int = coloursInHand.count(colour) # the amount of times a colour is in the hand
            if count > maxCount:
                choice, maxCount = colour, count # variables should be updated
        return choice

class Winner(Player):
    """Winner, inactive player"""
    def __init__(self, id: int):
        super().__init__(id)
        self.type: str = 'Winner'
    
    def choose_move(self, currentCard: Card) -> str:
        """Overrides Player's method"""
        return 'pass'