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

    def __str__(self):
        special_chars = {
            1: "A",
            13: "K",
            11: "J",
            12: "Q",
            14: "J",
            15: "J",
        }
        if self.value in special_chars:
            return special_chars.get(self.value)
        return str(self.value)


class Suit(Enum):
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"
    JOKER1 = "joker1"
    JOKER2 = "joker2"

    def __str__(self):
        match self.value:
            case Suit.CLUBS.value:
                return "\u2667"
            case Suit.DIAMONDS.value:
                return "\u2662"
            case Suit.HEARTS.value:
                return "\u2661"
            case Suit.SPADES.value:
                return "\u2664"
            case Suit.JOKER1.value:
                return "\u24DB"
            case Suit.JOKER2.value:
                return "\u24B7"

    @staticmethod
    def joker_suits():
        return [Suit.JOKER1, Suit.JOKER2]

    @staticmethod
    def suits():
        return [member for member in Suit if member not in Suit.joker_suits()]


class PrintCardMixin:
    def __str__(self):
        return """
############
# {s}        #
#          #
#    {r:2}    #
#          #
#        {s} #
############
""".format(s=self.suit, r=self.rank)


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


def card_factory(with_jokers=False, card_class=Card) -> list[Card]:
    cards = []
    if with_jokers:
        cards += list(zip(Rank.jokers(), Suit.joker_suits()))
    cards += list(itertools.product(Rank.ace_to_king(), Suit.suits()))

    return [card_class(rank=rank, suit=suit) for (rank, suit) in cards]


class TerminalCard(Card, PrintCardMixin):
    pass
