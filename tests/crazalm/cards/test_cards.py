import unittest
from collections import namedtuple


from crazcalm.cards import (
    Card,
    Rank,
    Suit,
    card_factory,
    TerminalCard,
)


class TestTerminalCard(unittest.TestCase):
    def test_print(self):
        Case = namedtuple("Case", ["case", "card", "expected"])
        cases = [
            Case(
                "ace of clubs",
                TerminalCard(rank=Rank.ACE, suit=Suit.CLUBS, face_down=False),
                """
############
# ♧        #
#          #
#    A     #
#          #
#        ♧ #
############
""",
            ),
            Case(
                "two of hearts",
                TerminalCard(rank=Rank.TWO, suit=Suit.HEARTS, face_down=False),
                """
############
# ♡        #
#          #
#    2     #
#          #
#        ♡ #
############
""",
            ),
            Case(
                "Jack of diamonds",
                TerminalCard(rank=Rank.JACK, suit=Suit.DIAMONDS, face_down=False),
                """
############
# ♢        #
#          #
#    J     #
#          #
#        ♢ #
############
""",
            ),
            Case(
                "10 of spades",
                TerminalCard(rank=Rank.TEN, suit=Suit.SPADES, face_down=False),
                """
############
# ♤        #
#          #
#    10    #
#          #
#        ♤ #
############
""",
            ),
            Case(
                "little joker",
                TerminalCard(rank=Rank.JOKER1, suit=Suit.JOKER1, face_down=False),
                """
############
# ⓛ        #
#          #
#    J     #
#          #
#        ⓛ #
############
""",
            ),
            Case(
                "big joker",
                TerminalCard(rank=Rank.JOKER2, suit=Suit.JOKER2, face_down=False),
                """
############
# Ⓑ        #
#          #
#    J     #
#          #
#        Ⓑ #
############
""",
            ),
        Case(
                "face down card",
                TerminalCard(rank=Rank.JOKER2, suit=Suit.JOKER2, face_down=True),
                """
############
############
############
### CARD ###
############
############
############
""",
            ),
        ]

        for num, case in enumerate(cases):
            with self.subTest(f"Case {num}: {case.case}"):
                card = str(case.card)
                self.assertEqual(card, case.expected)


class TestCardFactory(unittest.TestCase):
    def test_create_52_cards(self):
        cards = card_factory()
        self.assertEqual(len(cards), 52)

    def test_create_52_cards_and_jokers(self):
        cards = card_factory(with_jokers=True)
        self.assertEqual(len(cards), 54)


class TestCard(unittest.TestCase):
    def test_eq(self):
        card_1 = Card(rank=Rank.ACE, suit=Suit.CLUBS)
        card_2 = Card(rank=Rank.ACE, suit=Suit.CLUBS)
        card_3 = Card(rank=Rank.TEN, suit=Suit.CLUBS)
        card_4 = Card(rank=Rank.ACE, suit=Suit.HEARTS)
        card_5 = Card(rank=Rank.TEN, suit=Suit.HEARTS)

        Case = namedtuple("Case", ["card_1", "card_2", "expected"])
        cases = [
            Case(card_1, card_2, True),
            Case(card_1, card_3,  False),
            Case(card_1, card_4,  False),
            Case(card_1, card_5,  False),
        ]

        for num, case in enumerate(cases, start=1):
            with self.subTest(f"case {num}: "):
                self.assertEqual(case.card_1 == case.card_2, case.expected)

    def test_card_properties(self):
        card = Card(rank=Rank.ACE, suit=Suit.CLUBS)

        self.assertEqual(Rank.ACE, card.rank)
        self.assertEqual(Suit.CLUBS, card.suit)
        self.assertTrue(card.face_down)
        card.flip()
        self.assertFalse(card.face_down)

        with self.assertRaises(AttributeError):
            card.rank = Rank.TWO

        with self.assertRaises(AttributeError):
            card.suit = Suit.HEARTS


if __name__ == "__main__":
    unittest.main()


