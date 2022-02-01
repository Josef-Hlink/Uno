import unittest

from game import Game
from player import *


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        """
        Sets up, for each testcase:
        -A game object
        -shuffles the deck of this game object
        -Creates two computer players within this game object
        -Deals cards to these player objects
        """
        self.game = Game()

        self.game.deck.shuffle(10)
        self.game.create_players((2, 0))
        self.game.deal()

    def test_handle_bully_response_cant_respond(self):
        """
        tests the case when a player cant respond to a bully card
        """
        self.game.put_on_pile(('any colour', 'Draw Two'))
        self.game.players[0].receive_hand([('Red', 0)])  # magic carding, need a player with a hand with no response
        self.game.bullyDraw = 2

        self.assertFalse(self.game.handle_bully_response(self.game.players[0]))
        self.assertEqual(len(self.game.players[0].hand), 3)

    def test_handle_bully_response_can_respond_two(self):
        """
        tests if a bully happens in game and can be responded to +2
        """
        self.game.put_on_pile(('any colour', 'Draw Two'))
        self.game.players[0].receive_hand([('Red', 'Draw Two'), ('Second', 'Card')])
        self.game.bullyDraw = 2

        self.assertTrue(self.game.handle_bully_response(self.game.players[0]))
        self.assertEqual(self.game.bullyDraw, 4)

    def test_handle_bully_response_can_respond_four(self):
        """
        tests if a bully happens in game and can be responded to +4
        """
        self.game.put_on_pile(('any colour', 'Draw Four'))
        self.game.players[0].receive_hand([('Black', 'Draw Four'), ('Second', 'Card')])
        self.game.bullyDraw = 4

        self.assertTrue(self.game.handle_bully_response(self.game.players[0]))
        self.assertEqual(self.game.bullyDraw, 8)

    # def test_handle_bully_response_refuse_respond(self):
    #     self.game.put_on_pile(('Red', 'Draw Two'))
    #     self.game.bullyDraw = 2
    #     self.game.players[0].receive_hand([('Red', 0)])
    #
    #     self.assertTrue(self.game.handle_bully_response(self.game.players[0]))
    #     self.assertEqual(self.game.players[0].hand, 2)

    def test_deal(self):
        """
        tests the deal function
        """
        for each in self.game.players:
            self.assertTrue(len(each.hand) == 7)

    def test_draw_single_card(self):
        """
        tests if the draw function correctly draws a single card
        """
        cards_in_deck = self.game.deck.count_cards()
        single_card = self.game.draw(1)[0]

        self.assertEqual(cards_in_deck - 1, self.game.deck.count_cards())
        self.assertIsInstance(single_card, tuple)

    def test_draw_multiple_cards(self):
        """
        tests if the draw function correctly draws multiple cards
        """
        cards_in_deck = self.game.deck.count_cards()
        cards = self.game.draw(4)

        self.assertEqual(len(cards), 4)
        self.assertEqual(self.game.deck.count_cards(), cards_in_deck - 4)
        for el in cards:
            self.assertIsInstance(el, tuple)

    def test_draw_deck_is_empty(self):
        """"
        tests the draw function in the case of the deck being empty
        """
        full_deck = self.game.draw(self.game.deck.count_cards() - 1)  # draw the full deck except one
        for el in full_deck:
            self.game.put_on_pile(el)  # place the cards back on pile
        self.assertEqual(self.game.deck.count_cards(), 1)
        cards = self.game.draw(2)
        self.assertEqual(len(cards), 2)
        self.assertEqual(self.game.deck.count_cards(), len(full_deck) - 1)
        for el in cards:
            self.assertIsInstance(el, tuple)

    def test_player_count(self):
        """
        tests player count function
        """
        player_count = (2, 0, 2)  # that being players, human players and computer players respectively

        self.assertEqual(self.game.number_of_players(), player_count[0])
        self.assertEqual(self.game.number_of_human_players(), player_count[1])
        self.assertEqual(self.game.number_of_computer_players(), player_count[2])

    def test_is_done_false(self):
        """
        tests is done function for the false case
        """
        self.assertFalse(self.game.is_done())

    def test_is_done_true(self):
        """
        tests the is done function in the true case
        """
        self.game.players[0].hand = []
        self.assertTrue(self.game.is_done())  # will then be done as there is only one player left

    def test_next_playerid_sideways(self):
        """
        tests if next playerid correctly yields the next playerID
        """
        self.assertEqual(self.game.next_player_id(1), 2)

    def test_next_playerid_rotate(self):
        """"
        tests if next playerid correctly yields the next playerId
        if it has to wrap the turns back around to start or end of playerlist
        """
        self.assertEqual(self.game.next_player_id(2), 1)

    def test_handle_action_normal(self):
        """
        tests handle action based on a normal card
        """
        card = self.game.draw(1)[0]  # will always return a list with a single item
        while not isinstance(card[1], int):
            card = self.game.deck.redraw(card)

        self.assertEqual(self.game.handle_action(card, self.game.players[0]), 2)
        self.assertEqual(self.game.top_of_pile(), card)

    def test_handle_action_Draw_Two(self):
        """
        tests handle action based on a draw two
        """
        card = self.game.draw(1)[0]
        while not card[1] == 'Draw Two':
            card = self.game.deck.redraw(card)

        self.assertEqual(self.game.handle_action(card, self.game.players[0]), 2)
        self.assertEqual(self.game.top_of_pile(), card)
        self.assertEqual(self.game.bullyDraw, 2)

    def test_handle_action_Draw_Four(self):
        """"
        Tests handle action based on a draw four
        """
        card = self.game.draw(1)[0]
        while not card[1] == 'Draw Four':
            card = self.game.deck.redraw(card)

        self.assertEqual(self.game.handle_action(card, self.game.players[0]), 2)
        self.assertEqual(self.game.top_of_pile()[1], card[1])  # the computer will choose a colour
        self.assertEqual(self.game.bullyDraw, 4)

    def test_handle_action_skip(self):
        """"
        Tests handle action based on a skip
        """
        card = self.game.draw(1)[0]
        while not card[1] == 'Skip':
            card = self.game.deck.redraw(card)

        self.assertEqual(self.game.handle_action(card, self.game.players[0]), 1)
        self.assertEqual(self.game.top_of_pile(), card)

    def test_handle_action_skip_with_winners(self):
        """"
        tests handle action skipping players who have already won properly
        """
        winnersgame = Game()
        winnersgame.create_players((3, 0))
        winnersgame.deal()
        winnersgame.players[1].receive_hand([])
        winnersgame.is_done()

        self.assertIsInstance(winnersgame.players[1], Winner)
        card = winnersgame.draw(1)[0]
        while not card[1] == 'Skip':
            card = winnersgame.deck.redraw(card)

        self.assertEqual(winnersgame.handle_action(card, winnersgame.players[0]), 1)

    def test_handle_action_reverse_two_player(self):
        """"
        tests if handle action properly stays on turn with 2 players
        """
        card = self.game.draw(1)[0]
        while not card[1] == 'Reverse':
            card = self.game.deck.redraw(card)

        self.assertEqual(self.game.handle_action(card, self.game.players[0]), 1)  # stays on turn as there is only 2 players

    def test_handle_action_reverse_three_players(self):
        """"
        tests if handle action properly reverses turn order
        """
        card = self.game.draw(1)[0]
        while not card[1] == 'Reverse':
            card = self.game.deck.redraw(card)

        self.game.create_players((1, 0))
        self.assertEqual(self.game.handle_action((card), self.game.players[0]), 3)
        self.assertEqual(self.game.direction, -1)


    def test_handle_action_wild(self):
        """"
        tests handle action on a wildcard
        """
        card = self.game.draw(1)[0]
        while not card[1] == 'Wild':
            card = self.game.deck.redraw(card)

        self.assertEqual(self.game.handle_action(card, self.game.players[0]), 2)
        self.assertNotEqual(self.game.top_of_pile()[0], 'Black')  # computer needs to have changed the colour

    def test_handle_action_pass(self):
        """"
        Tests handle action on a turn being passed
        """
        passing_card = ()  # use an empty tuple to signify a pass
        self.assertEqual(self.game.handle_action(passing_card, self.game.players[0]), 2)

    def test_handle_action_incorrect_uno(self):
        """"
        Tests handle action based on an incorrect uno call having happened
        """
        card = ('Uno', False)  # the tuple yielded by player.choose_move() on a bad uno call

        self.assertEqual(self.game.handle_action(card, self.game.players[0]), 1)
        self.assertEqual(len(self.game.players[0].hand), 10)


