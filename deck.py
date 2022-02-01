import random # for shuffling


class Deck:
    def __init__(self):
        self.cardDeck: list = [] # in this variable the entire deck will be stored
        self.create() # calls the function that actually puts the cards in the variable cardDeck

    def __str__(self) -> str:
        """Converts the object to a String representation"""
        return str(self.cardDeck)

    def create(self) -> bool:
        """Generates all needed cards and appends these to self.cardDeck"""
        for colour in ['Red', 'Yellow', 'Blue', 'Green']:
            for number in list(range(0, 10)) + list(range(1, 10)):
                self.cardDeck.append((colour, number))
            for actionCardType in ['Draw Two', 'Reverse', 'Skip']:
                self.cardDeck.append((colour, actionCardType))
                self.cardDeck.append((colour, actionCardType))
        for _ in range(4):
            for blackCardType in ['Draw Four', 'Wild']:
                blackCard = ('Black', blackCardType)
                self.cardDeck.append(blackCard)
        return True

    def recreate(self, pile: list) -> None:
        """If deck is empty, takes all cards on pile and shuffles them
        :param pile of cards:"""
        dirtyDeck: list = pile.copy()
        for card in dirtyDeck:
            if card[1] == 'Wild' or card[1] == 'Draw Four':
                self.cardDeck.append(('Black', card[1]))
            else:
                self.cardDeck.append(card)
        self.shuffle(10)
        return None

    def shuffle(self, times: int) -> None:
        """Shuffles the deck a specified amount of times"""
        for _ in range(times):
            random.shuffle(self.cardDeck)

    def draw(self) -> tuple:
        """Removes the last element of the deck and returns it"""
        return self.cardDeck.pop()

    def redraw(self, card: tuple) -> tuple:
        """Put a non-number card back in the deck somewhere randomly and return a new one"""
        self.cardDeck.append(card)
        self.shuffle(1) # shuffle just one time
        return self.cardDeck.pop()

    def count_cards(self) -> int:
        """Returns the number of cards currently in the deck"""
        return len(self.cardDeck)

    def contains(self, el: tuple) -> bool:
        """Checks if a given card exists in the deck"""
        return el in self.cardDeck

    def is_empty(self) -> bool:
        """Checks if deck has been emptied"""
        return len(self.cardDeck) == 0
