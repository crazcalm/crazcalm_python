import unittest
import itertools
from collections import namedtuple
from copy import deepcopy

from crazcalm.cards import (
    Card,
    Rank,
    Suit,
    Deck,
    NoCardsLeftInDeckException,
    TerminalDeck,
    TerminalCard,
)

class TestTerminalDeck(unittest.TestCase):
    def test_print(self):
        deck = TerminalDeck(cards=[])
        card = TerminalCard(rank=Rank.ACE, suit=Suit.CLUBS, face_down=False)
        expected_card_str = """
############
# ♧        #
#          #
#    A     #
#          #
#        ♧ #
############
"""
        expected_deck_str = """
############
############
############
### Deck ###
############
############
############
"""

        self.assertEqual(expected_deck_str, str(deck))

        # Add face up card on top of the deck
        deck.put_on_top(card)
        self.assertEqual(expected_card_str, str(deck))
        # putting the card face down
        card.flip()
        self.assertEqual(expected_deck_str, str(deck))


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.cards = list(itertools.product(Rank.ace_to_king(), [Suit.CLUBS]))
        self.deck = Deck(cards=deepcopy(self.cards))
        self.joker = Card(rank=Rank.JOKER1, suit=Suit.JOKER1)

    def test_create_52_card_deck(self):
        deck = Deck.create_52_card_deck()
        deck_with_jokers = Deck.create_52_card_deck(with_jokers=True)

        self.assertEqual(52, deck.cards_left())
        self.assertEqual(54, deck_with_jokers.cards_left())

    def test_draw(self):
        expected_num_of_cards = self.deck.cards_left() - 1
        _ = self.deck.draw()

        self.assertEqual(expected_num_of_cards, self.deck.cards_left())

    def test_draw_exception(self):
        deck = Deck(cards=[])
        with self.assertRaises(NoCardsLeftInDeckException):
            deck.draw()

    def test_shuffle(self):
        non_shuffled_cards = [x for x in self.cards[::-1]]
        cards = []
        self.deck.shuffle()

        while self.deck.cards_left():
            cards.append(self.deck.draw())

        self.assertNotEqual(cards, non_shuffled_cards)

    def test_put_on_top(self):
        self.deck.put_on_top(self.joker)
        self.assertEqual(self.joker, self.deck.draw())

    def test_put_on_bottom(self):
        self.deck.put_on_bottom(self.joker)

        while self.deck.cards_left() > 1:
            _ = self.deck.draw()

        self.assertEqual(self.joker, self.deck.draw())



if __name__ == "__main__":
    unittest.main()


