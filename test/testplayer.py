import unittest
from player import *
from game import Game


class TestPlayer(unittest.TestCase):

    def setUp(self) -> None:
        """
        create a player object at the start of each test
        """
        self.player = Computer(1)

    def test_computer_end_on_bully(self):
        """
        Tests if the computer successfully reports of being incapable on ending on a bully card
        """
        self.player.receive_hand([('any', 'Draw Two')])

        choice = self.player.choose_move(('any', 'Draw Two'))
        self.assertFalse(choice)
        self.assertIsInstance(choice, tuple)

    def test_computer_call_uno(self):
        """
        Tests if computer properly calls uno
        """
        self.player.receive_hand([('any colour', 'any value'), ('any colour', 'any value')])
        self.player.choose_move(('any colour', 'any value'))

        self.assertTrue(self.player.calledUno)

    def test_computer_bullies_draw_four(self):
        """
        Tests if computer correctly picks the bully card over other options
        """
        self.player.receive_hand([('Black', 'Draw Four'), ('Black', 0)])

        choice = self.player.choose_move(('Black', 'Draw Four'))
        self.assertEqual(choice, ('Black', 'Draw Four'))

    def test_computer_bullies_draw_two(self):
        """
        Tests if computer correctly picks the bully card over other options
        """
        self.player.receive_hand([('Red', 'Draw Two'), ('Blue', 0)])

        choice = self.player.choose_move(('Blue', 'Draw Two'))
        self.assertEqual(choice, ('Red', 'Draw Two'))

    def test_computer_no_valid_moves(self):
        """
        tests if the computer correctly reports having no valid moves
        """
        self.player.receive_hand([('Blue', 1), ('Yellow', 1)])

        choice = self.player.choose_move(('Red', 0))
        self.assertFalse(choice)
        self.assertIsInstance(choice, tuple)

    def test_has_card_true(self):
        """
        Tests if has_card function works correctly
        """
        self.player.receive_hand([("red", 0)])

        self.assertTrue(self.player.has_card(('red', 0)))

    def test_has_card_false(self):
        """
        Tests if has card function works properly
        """
        self.player.receive_hand([("red", 0)])

        self.assertFalse(self.player.has_card(('blue', 0)))

    def test_handle_uno_call_true(self):
        """
        Tests if handle uno works properly
        """
        self.player.receive_hand([('Red', 0), ('Blue', 0)])

        self.assertTrue(self.player.handle_uno_call(('Green', 0)))

    def test_handle_uno_call_false(self):
        """
        Tests if handle uno works properly
        """
        self.player.receive_hand([('Red', 0), ('Blue', 0)])

        self.assertFalse(self.player.handle_uno_call(('Green', 1)))
