import typing
import numpy as np
from card import Card
from deck import Deck
from player import Player
from player import Human
from player import Computer
from player import Winner
from bigvalue import Bigvalue

class Game:
    def __init__(self):
        self.deck = Deck() # this line generates a deck
        self.players: typing.List[Player] = [] # a list that contains all of the player instances
        self.pile: typing.List[Card] = [] # discard pile, all played cards get appended to this
        self.direction: int = 1 # for keeping track of the turn direction
        self.currentCard: Card = () # card on top of discard pile, card that needs to be reacted to
        self.bullyDraw: int = 0 # for keeping track of +2's and +4's
        self.winners: int = 0 # keeps track of all players that are finished

    def __call__(self) -> None:
        """Starts the game when called"""
        self.start()
        return

    def start(self) -> None:
        """
        Initializes the game
        ---
        1. Create player instances
        2. Shuffle deck ten times
        3. Deal cards to the players
        4. Draw starting card to discard pile
        5. Call function that actually run the game
        """
        self.create_players()
        self.deck.shuffle(10)
        self.deal()
        card: Card = self.deck.draw()
        while not isinstance(card.value, int):
            card = self.deck.redraw(card)
        self.put_on_pile(card)
        self.run()
        return
    
    def run(self) -> None:
        """Very large and potentially confusing method that kind of handles everything:
        the main body of class Game that actually runs a Uno game"""
        currentPlayerId: int = 1 # player 1 starts
        while not self.is_done():
            
            nextPlayerId = currentPlayerId # why is this line here?
            currentPlayer = self.players[currentPlayerId-1] # get current player by their id

            if isinstance(currentPlayer, Winner): # checking if current player is still active
                print('-' * 64 + f'player {currentPlayerId} is already done')
                currentPlayerId = self.next_player_id(currentPlayerId)
                currentPlayer = self.players[currentPlayerId-1]
                continue
            
            if len(currentPlayer.hand) == 1 and not currentPlayer.calledUno: # checking for forgotten Uno Calls
                print('-' * 64 + f'player {currentPlayerId} did not call uno and has to draw 3 cards')
                currentPlayer.draw(self.draw(3))
            currentPlayer.calledUno = False
                   
            if self.bullyDraw != 0: # checking for "active" bullying
                passOnToNext: int = self.handle_bully_response(currentPlayer)
                if passOnToNext: # when passed on to next player, the non-zero int will evaluate to true
                    nextPlayerId = passOnToNext # this int is also the next player's id
                    currentPlayerId = nextPlayerId # this can be done in one line, but it would be more confusing right now
                    continue
            
            # "normal" behavior starts here
            self.display_options(currentPlayer)
            if not currentPlayer.has_valid_move(self.currentCard):
                if isinstance(currentPlayer, Human):
                    _ = input(f'You (player {currentPlayer.id}) currently have no valid moves, press Enter to draw a card: ')
                print('-' * 64 + f'player {currentPlayerId} could not play')                
                currentPlayer.draw(self.draw())
                self.display_options(currentPlayer)
            # for the next turn, current player id is set to next player id, which is returned by handle_action
            currentPlayerId = self.handle_action(currentPlayer.choose_move(self.currentCard), currentPlayer)
        return

    def handle_action(self, action: typing.Union[Card, str], currentPlayer: Player) -> int:
        """Handles all possible choices a player could make, including passing and calling Uno incorrectly
        :param card: :param current player: :return next player id:"""
        currentPlayerId = currentPlayer.id
        
        if action == 'pass': # player passed
            print('-' * 64 + f'player {currentPlayerId} passed')
            return self.next_player_id(currentPlayerId)
        elif action == 'wrongcall': # player did an incorrect uno call
            currentPlayer.draw(self.draw(3))
            return currentPlayerId
        else: # player played an actual card
            print('-' * 64 + f'player {currentPlayerId} played {action}')

        card = action
        value = card.value

        try:
            int(value)
        except ValueError:
            if value == 'Draw Two':
                self.bullyDraw += 2
            elif value == 'Draw Four':
                self.bullyDraw += 4
                card.colour = self.players[currentPlayerId-1].pick_colour()

            elif value == 'Skip': # id gets changed to next until an active player is skipped
                while isinstance(self.players[self.next_player_id(currentPlayerId) - 1], Winner):
                    currentPlayerId = self.next_player_id(currentPlayerId)
                    print('-' * 64 + f'player {currentPlayerId} is already done')
                currentPlayerId = self.next_player_id(currentPlayerId) # skip the active player
                print('-' * 64 + f'player {currentPlayerId} was skipped')
            
            elif value == 'Reverse' and self.number_of_players() >= 3:
                self.direction *= -1
            elif value == 'Reverse' and self.number_of_players() == 2: # special behavior!
                self.put_on_pile(card) # immediately put the card on pile
                return currentPlayerId # and return the player's own id

            elif value == 'Wild':
                card.colour = self.players[currentPlayerId-1].pick_colour()
        
        self.put_on_pile(card)
        return self.next_player_id(currentPlayerId)

    def handle_bully_response(self, currentPlayer: Player) -> int:
        """Handles a player's response to being bullied with +2 or +4
        :param current player: :return 0 [falsy] or next player's id [truthy]:"""
        currentPlayerId = currentPlayer.id
        col, val = self.currentCard.colour, self.currentCard.value
        aDrawTwo: Card = Card('*', 'Draw Two')
        aDrawFour: Card = Card('Black', 'Draw Four')

        if (    val == 'Draw Two' and \
                (currentPlayer.has_card(aDrawTwo) or currentPlayer.has_card(aDrawFour))) or (
                val == 'Draw Four' and \
                (currentPlayer.has_card(aDrawFour) or currentPlayer.has_card(Card(col, 'Draw Two')))):

            self.display_options(currentPlayer)
            chosenMove = currentPlayer.choose_move(self.currentCard)
            if isinstance(chosenMove, Card): # they could technically choose to not play their own +2 or +4
                if chosenMove.value != 'Draw Two' and chosenMove.value != 'Draw Four':
                    self.draw_bully(currentPlayer) # but then they would still have to draw the cards
                currentPlayerId = self.handle_action(chosenMove, currentPlayer)
                return currentPlayerId # for a truthy value
        else:
            self.draw_bully(currentPlayer)
            return 0  # for a falsy value

    def draw_bully(self, currentPlayer: Player) -> None:
        """Makes a player draw the total number of cards that they have been bullied with
        :param current player:"""
        currentPlayer.draw(self.draw(self.bullyDraw))
        print('-' * 64 + f'player {currentPlayer.id} had to draw {self.bullyDraw} cards')
        self.bullyDraw = 0
        return

    def how_many_players(self) -> tuple:
        """Asks the user for the total number of players and the number of human players
        :return tuple(total no. players, no. human players):"""
        validInput = False
        while not validInput:
            try:
                numPlayers = int(input("How many players?:\n>"))
                while numPlayers < 2 or numPlayers > 10:
                    numPlayers = int(input("Invalid. Please enter a number between 2-10. How many players?:\n>"))
                validInput = True
            except ValueError:
                print("Please use a numerical value")
                continue
        validInput = False
        while not validInput:
            try:
                numHumanPlayers = int(input("How many human players?:\n>"))
                while numHumanPlayers < 0 or numHumanPlayers > numPlayers:
                    numHumanPlayers = int(input(
                        "Invalid. Please enter a number between zero and total number of players. How many human players?:\n>"))
                validInput = True
            except ValueError:
                print("Please use a numerical value")
                continue
        print('\n' * 20)
        return (numPlayers, numHumanPlayers)

    def create_players(self, playerCount: tuple = None) -> None:
        """Creates instances of Human and/or Computer players and appends these to the game's self.players list
        :param tuple(total no. players, no. human players):"""
        if playerCount is not None:
            numPlayers = playerCount[0]
            numHumanPlayers = playerCount[1]
        else:
            numPlayers, numHumanPlayers = self.how_many_players()
        for i in range(1, numHumanPlayers+1):
            self.players.append(Human(id = i))
        for i in range(numHumanPlayers+1, numPlayers+1):
            self.players.append(Computer(id = i))
        return

    def deal(self) -> None:
        """Deals seven cards to every player"""
        for player in self.players:
            player.receive_hand(self.draw(7))
        return

    def put_on_pile(self, card: Card) -> None:
        """Adds a given card to the pile :param card:"""
        if card:
            self.pile.append(card)
            self.currentCard = card
        return

    def top_of_pile(self) -> Card:
        """Removes the most recently played card from pile :return card:"""
        return self.pile.pop()

    def draw(self, times: int = 1) -> typing.List[Card]:
        """Draws a specified number of cards from the deck
        :param no. cards: :return list of drawn cards:"""
        cards: typing.List[Card] = []
        for _ in range(times):
            if self.deck.is_empty():
                self.deck.recreate(self.pile)
                self.pile = [self.top_of_pile()]
            cards.append(self.deck.draw())
        return cards
 
    def next_player_id(self, currentPlayerId: int) -> int:
        """Determines what player is next to move
        :param current id: :return next id:"""
        next = currentPlayerId + self.direction # base case
        if next == 0 or next == self.number_of_players() + 1: # if exception
            next = 1 if self.direction == 1 else self.number_of_players() # handling
        return next

    def is_done(self) -> bool:
        """Checks for winners until only one loser is left
        :return answer to question posed in method name:"""
        for player in self.players:
            playerId = player.id
            if not isinstance(player, Winner) and len(player.hand) == 0: # check for new winners
                self.winners += 1
                print('\n|-_-_-_-_-_-_-_-_-_-_-_-|'+
                f'\n |Player {playerId} is number {self.winners}!|'+
                '\n|-_-_-_-_-_-_-_-_-_-_-_-|\n')
                # player's place in game's self.playerslist is overwritten by winner object
                self.players[playerId-1] = Winner(playerId)
            if self.number_of_players() - self.winners <= 1: # game is done, only one loser left
                return True
        return False


    def display_options(self, currentPlayer: Player) -> None:
        """Displays the card a player need to react to, as well as
        all of the player's options, including Pass & Call Uno"""
        print('\n' * 17)
        
        for player in self.players:
            if player.calledUno:
                print('-' * 64 + f'player {player.id} called Uno!\n')

        self.display_top_card()
        print(f'---player {currentPlayer.id}\'s turn---')
        if isinstance(currentPlayer, Human) and self.number_of_human_players() >= 2:
            # so the previous human player can't see the current player's cards after they chose their move
            _ = input('Press Enter to view your options: ')

        cardsDisplayed: int = 0 # for making multiple lines work
        shortHand: list = self.to_short_hand(currentPlayer.hand)
        rowsNeeded: int = 1 + len(currentPlayer.hand) // 15 # only 14 cards fit in one row
        shortHandDivided: list[np.array] = np.array_split(shortHand, rowsNeeded)
        for row in range(1, rowsNeeded+1):
            self.display_hand(shortHandDivided[row-1], cardsDisplayed)
            cardsDisplayed += len(shortHandDivided[row-1])
        print('Other options:\n' +
              f'{len(shortHand)+1} - Pass\n' +
              f'{len(shortHand)+2} - Call Uno\n')
        return

    def display_hand(self, shortHand: typing.List[tuple], cardsDisplayed: int) -> None:
        """Displays a player's hand, and if needed it does so on multiple rows"""
        space: str = ' ' # needed to make faststrings work since f'{' ' * n}' is illegal
        horizontalBound: str = ('+' + '-' * 5 + '+ ') * len(shortHand)
        line1, line2, line3, optionLine = '', '', '', ''
        for idx, card in enumerate(shortHand):
            line1 += f'| {card[0]} | ' # prints the short colour
            line2 += f'|     | '
            line3 += f'| {card[1]} | ' # prints the short value
            optionNumber: str = f'{cardsDisplayed + idx+1}' # gets the correct option nr. for every card
            optionLine += f'   {optionNumber} {space * (3 - len(optionNumber))} '
        
        print(horizontalBound + '\n' +
              line1 + '\n' +
              line2 + '\n' +
              line3 + '\n' +
              horizontalBound + '\n' +
              optionLine + '\n')
        return

    def display_top_card(self) -> None:
        """Displays a single card with size 34 by 21 (ASCII characters)"""
        colourDict: dict = {'Black': '#',
                            'Blue': '\033[0;34m' + 'B' + '\033[0m',
                            'Red': '\033[0;31m' + 'R' + '\033[0m',
                            'Yellow': '\033[0;33m' + 'Y' + '\033[0m',
                            'Green': '\033[0;32m' + 'G' + '\033[0m'}
        smallValueDict: dict = {'Reverse': '<', 'Skip': '>', 'Draw Four': '+', 'Draw Two': '+', 'Wild': 'W'}
        bigValueGetter: dict = Bigvalue()

        try:
            char: str = colourDict[self.currentCard.colour]
            val: str = self.currentCard.value if isinstance(self.currentCard.value, int) \
                       else smallValueDict[self.currentCard.value]
            bigValue: list[str] = bigValueGetter(self.currentCard.value)
        except KeyError:
            return

        line1: str = '|' + char * 15 + ' ' * 6 + char * 11 + '|'
        line2: str = '|' + char * 11 + ' ' * 13 + char * 8 + '|'
        line3: str = '|' + char * 9 + ' ' * 16 + char * 7 + '|'
        line4: str = '|' + char * 7 + ' ' * 18 + char * 7 + '|'
        line5: str = '|' + char * 6 + bigValue[0] + char * 6 + '|'
        line6: str = '|' + char * 6 + bigValue[1] + char * 6 + '|'
        line7: str = '|' + char * 6 + bigValue[2] + char * 6 + '|'
        line8: str = '|' + char * 6 + ' ' * 20 + char * 6 + '|'
        line9: str = '|' + char * 7 + ' ' * 18 + char * 7 + '|'
        line10: str = '|' + char * 7 + ' ' * 16 + char * 9 + '|'
        line11: str = '|' + char * 8 + ' ' * 13 + char * 11 + '|'
        line12: str = '|' + char * 11 + ' ' * 6 + char * 15 + '|'

        topLine: str = '  ' + '_' * 30 + '\n' + f' /{val}|' + char * 26 + f'|{val}\\'
        almostFullLine: str = '|--' + char * 28 + '--|'
        fullLine: str = '|' + char * 32 + '|'
        bottomLine: str = f' \\{val}|' + char * 26 + f'|{val}/'

        for line in [topLine, almostFullLine, fullLine, fullLine,
                    line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12,
                    fullLine, fullLine, almostFullLine, bottomLine + '\n']:
            print(line)
        return

    def to_short_hand(self, longHand: typing.List[Card]) -> typing.List[tuple]:
        """For a players hand, converts all of the values to short printables
        by combining to_short_colour and to_short_value calls
        :param player's hand: :return same hand, but shorter strings:"""
        return [(self.to_short_colour(card.colour), self.to_short_value(card.value)) for card in longHand]

    def to_short_colour(self, colour: str) -> str:
        """For any colour, returns three-letter abbreviation :param cardcolour:"""
        try:
            return {'Black': 'blk',
                    'Blue': '\033[0;34m' + 'blu' + '\033[0m',
                    'Yellow': '\033[0;33m' + 'ylw' + '\033[0m',
                    'Red': '\033[0;31m' + 'red' + '\033[0m',
                    'Green': '\033[0;32m' + 'grn' + '\033[0m'}[colour]
        except KeyError:
            return '   '

    def to_short_value(self, value: str) -> str:
        """For any value, returns three-letter abbreviation :param cardvalue:"""
        try:
            return {'Reverse': 'rev',
                    'Skip': 'skp',
                    'Draw Two': '+ 2',
                    'Draw Four': '+ 4',
                    'Wild': 'wld'
                    }[value]
        except KeyError:
            return f' {value} ' # number, but with one leading and trailing space

    def old_display_options(self, currentPlayer: Player) -> None:
        """Calls display_pile, and displays a player's hand including Pass and Call Uno options"""
        # this method is not accessed in this version, but might be used again in the future
        space: str = ' ' # needed to make faststrings work since f'{' ' * n}' is illegal
        self.display_pile()
        print(f'+---------player {currentPlayer.id}\'s turn--------+')
        for i, card in enumerate(currentPlayer.hand):
            viewColour: str = f'{i+1}. | {card.colour} {space * (8 - len(card.colour) - len(str(i+1)))}'
            viewValue: str = f'{card.value} {space * (13 - len(str(card.value)))}'
            print(f'| {viewColour} | {viewValue} |')
        print('+--------------------------------+')
        passLine: str = f'{len(currentPlayer.hand)+1}. | Pass'
        unoLine: str = f'{len(currentPlayer.hand)+2}. | Call Uno'
        print(f'| {passLine} {space * (29-len(passLine))} |')
        if not currentPlayer.calledUno:
            print(f'| {unoLine} {space * (29-len(unoLine))} |')
        print('+--------------------------------+')
        return

    def display_pile(self) -> bool:
        """Displays the four most recent items in pile"""
        # this method is not accessed in this version, but might be used again in the future
        space: str = ' '
        shown: int = 0
        print('\n+~~~~~~~~~~top of pile~~~~~~~~~~~+')
        for i in range(len(self.pile)-1, -1, -1): # start, stop, step
            card = self.pile[i]
            viewColour: str = f'{i+1}.| {card.colour} {space * (9 - len(card.colour) - len(str(i+1)))}'
            viewValue: str = f'{card.value} {space * (13 - len(str(card.value)))}'
            print(f'| {viewColour} | {viewValue} |')
            shown += 1
            if shown >= 4:
                break
        print('+~~~~~~~~~~~~~~~V~~~~~~~~~~~~~~~~+\n')
        return True


    def number_of_players(self) -> int:
        """returns total number of players in the game"""
        return len(self.players)

    def number_of_human_players(self) -> int:
        """Returns number of human players in the game"""
        return len([player for player in self.players if isinstance(player, Human)])
    
    def number_of_computer_players(self) -> int:
        """Returns number of human players in the game"""
        return len([player for player in self.players if isinstance(player, Computer)])
