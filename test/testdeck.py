import unittest

from deck import Deck


class TestDeck(unittest.TestCase):

    def setUp(self) -> None:
        """"
        For each testcase:
        Create a Deck object, create lists of lefthands and righthands of cards in there
        """
        self.deck = Deck() #instantiate a deck object for testing

        self.card_lefthand = []
        self.card_righthand = []
        for el in self.deck.cardDeck:
            self.card_lefthand.append(el[0])
            self.card_righthand.append(el[1])

    def test_to_String(self):
        self.assertIsInstance(self.deck.__str__(), str)

    def test_create_same_tuples(self):
        """
        tests if deck object properly has its cards created
        """
        second_deck = Deck()
        self.assertEqual(self.deck.cardDeck, second_deck.cardDeck)

    def test_create_card_colour_occurrences(self):
        """"
        Tests if deck is filled with the proper colours
        """
        expected_cards_per_colour = 25  # 25 cards, 19 numbered cards (0 through 9 and 1 through 9) and 6 bully cards

        self.assertEqual(self.card_lefthand.count('Red'), expected_cards_per_colour)
        self.assertEqual(self.card_lefthand.count('Blue'), expected_cards_per_colour)
        self.assertEqual(self.card_lefthand.count('Yellow'), expected_cards_per_colour)
        self.assertEqual(self.card_lefthand.count('Green'), expected_cards_per_colour)
        self.assertEqual(self.card_lefthand.count('Black'), 8)  # 8, 4 times 2 different type of black card

    def test_create_card_number_occurrences(self):
        """"
        Tests if deck is filled with the proper numbers
        """
        expected_number_count = 8  # 8, 4 for each colour and then the second run
        expected_count_zero = 4  # 4, once each colour and is excluded from second run

        for i in range(0, 10):
            if i == 0:
                self.assertEqual(self.card_righthand.count(i), expected_count_zero)
            else:
                self.assertEqual(self.card_righthand.count(i), expected_number_count)

    def test_create_bully_card_occurrences(self):
        """"
        tests if the deck is filled with the proper bully cards
        """
        expected_colour_bully_count = 8  # 8, two for each colour
        expected_black_bully_count = 4  # 4, four times one card type

        for i in ['Draw Two', 'Reverse', 'Skip']:
            self.assertEqual(self.card_righthand.count(i), expected_colour_bully_count)
        for i in ['Draw Four', 'Wild']:
            self.assertEqual(self.card_righthand.count(i), expected_black_bully_count)

    def test_recreate(self):
        """"
        tests if the deck properly gets recreated from pile/shuffled
        """
        pseudo_card_pile = ['card 1', 'card 2', 'card 3', "card 4"]

        self.deck.recreate(pseudo_card_pile)
        for el in pseudo_card_pile:
            self.assertIn(el, self.deck.cardDeck)
        self.assertNotEqual(self.deck.cardDeck, pseudo_card_pile)

    def test_recreate_restore_black(self):
        """"
        tests if upon deck recreation black cards are properly restored
        """
        pile = [('Purple', 'Draw Four'), ('Purple', "Wild")]
        self.deck.recreate(pile)

        self.assertIn(('Black', 'Draw Four'), self.deck.cardDeck)
        self.assertIn(("Black", "Wild"), self.deck.cardDeck)

    def test_shuffle(self):
        """"
        tests if shuffling happens properly
        """
        second_deck = Deck()

        self.deck.shuffle(1)  # one time, deck should be properly shuffled after one time
        self.assertNotEqual(self.deck.cardDeck, second_deck.cardDeck)

    def test_draw(self):
        """
        tests if cards are properly drawn and removed from the deck
        """
        initial_deck_size = self.deck.count_cards()
        drawn_card = self.deck.draw()

        self.assertIsInstance(drawn_card, tuple)
        self.assertEqual(self.deck.count_cards(), initial_deck_size - 1)

    def test_redraw_new_card(self):
        """"
        tests redrawing from the deck
        """
        initial_draw = self.deck.draw()
        self.assertNotEqual(initial_draw, self.deck.redraw(initial_draw))

    def test_redraw_return_card(self):
        """
        tests if the redraw card is properly returned
        """
        initial_draw = self.deck.draw()
        card_occurrences = self.deck.cardDeck.count(initial_draw)
        self.deck.redraw(initial_draw)
        self.assertNotEqual(card_occurrences, self.deck.cardDeck.count(initial_draw))

    def test_contains(self):
        """"
        test contains function
        """
        card = self.deck.draw()
        self.deck.redraw(card)

        self.assertTrue(self.deck.contains(card))

    def test_is_empty(self):
        """"
        test is empty function
        """
        while not self.deck.is_empty():
            self.deck.draw()  # draw until empty
        self.assertTrue(self.deck.is_empty())


