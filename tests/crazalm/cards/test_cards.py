import unittest

from crazcalm.cards import (
    Card,
    Rank,
    Suit,
    card_factory,
)


class TestCardFactory(unittest.TestCase):
    def test_create_52_cards(self):
        cards = card_factory()
        self.assertEqual(len(cards), 52)

    def test_create_52_cards_and_jokers(self):
        cards = card_factory(with_jokers=True)
        self.assertEqual(len(cards), 54)


class TestCard(unittest.TestCase):
    def test_card_properties(self):
        card = Card(rank=Rank.ACE, suit=Suit.CLUBS)

        self.assertEqual(Rank.ACE, card.rank)
        self.assertEqual(Suit.CLUBS, card.suit)

        with self.assertRaises(AttributeError):
            card.rank = Rank.TWO

        with self.assertRaises(AttributeError):
            card.suit = Suit.HEARTS


if __name__ == "__main__":
    unittest.main()


