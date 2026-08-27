import itertools
from enum import Enum

class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    JOKER1 = 14
    JOKER2 = 15

    @staticmethod
    def jokers():
        return [Rank.JOKER1, Rank.JOKER2]

    @staticmethod
    def ace_to_king():
        return [member for member in Rank if member not in Rank.jokers()]


class Suit(Enum):
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"
    NONE = "none"

    @staticmethod
    def suits():
        return [member for member in Suit if member != Suit.NONE]


class Card:
    def __init__(self, rank: Rank, suit: Suit):
        self._rank = rank
        self._suit = suit

    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit


def card_factory(with_jokers=False) -> list[Card]:
    cards = []
    if with_jokers:
        cards += list(itertools.product(Rank.jokers(), [Suit.NONE]))
    cards += list(itertools.product(Rank.ace_to_king(), Suit.suits()))

    return cards

