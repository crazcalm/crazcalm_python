
import random

from .card import card_factory, Card


class DeckException(Exception):
    pass

class NoCardsLeftInDeckException(DeckException):
    pass


class Deck:
    @classmethod
    def create_52_card_deck(cls, with_jokers=False) -> Deck:
        return cls(cards=card_factory(with_jokers=with_jokers))

    def __init__(self, cards: list[Card]):
        self._cards = cards

    def put_on_bottom(self, card: Card):
        self._cards.insert(0, card)

    def put_on_top(self, card: Card):
        self._cards.append(card)

    def shuffle(self):
        random.shuffle(self._cards)

    def draw(self) -> Card:
        if self.cards_left():
            return self._cards.pop()
        else:
            raise NoCardsLeftInDeckException

    def cards_left(self):
        return len(self._cards)
    
