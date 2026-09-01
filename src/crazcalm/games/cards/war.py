from crazcalm.cards import (
    TerminalDeck,
    TerminalCard,
    card_factory,
    Card,
)


class Player:
    def __init__(self):
        self.deck = TerminalDeck(cards=[])
        self.win_pile = TerminalDeck(cards=[])

    def reset(self):
        self.deck = TerminalDeck(cards=[])
        self.win_pile = TerminalDeck(cards=[])

    def lose_the_game(self) -> bool:
        return False if self.total_cards() else True

    def _play_card(self):
        result = None
        if self.deck.cards_left() > 0:
            result = self.deck.draw()
        elif self.win_pile.cards_left() > 0:
            while self.win_pile.cards_left() > 0:
                self.deck.put_on_bottom(self.win_pile.draw())
            result = self._play_card()
        return result

    def total_cards(self):
        return len(self.deck) + len(self.win_pile)

    def play_card(self) -> Card:
        return self._play_card()

    def play_war(self) -> list[Card]:
        result = []
        count = 4
        while count > 0:
            card = self.play_card()
            if not card.face_down:
                card.flip()

            result.append(card)
            count -= 1

            if self.total_cards() == 0:
                # Flippin the last card face up
                result[-1].flip()
                break

            if count == 1:
                # Flippin the last card face up
                result[-1].flip()
        return result

    def add_card_to_deck(self, card: Card):
        self.deck.put_on_top(card)

    def add_cards_to_win_pile(self, cards: list[Card]):
        for card in cards:
            self.win_pile.put_on_bottom(card)


    


class Game:
    def __init__(self, players: list[Player]):
        self.players = players

    def set_up_game(self):
        deck = TerminalDeck.create_52_card_deck(cls=TerminalDeck)
        count = 0
        while self.deck.cards_left() > 0:
            index = count % len(self.players)
            self.players[index].add_card_to_deck(deck.draw())
            count += 1

    def have_winner(self) -> bool:
        return len(self.players) - 1 == [player for player in self.players if player.lose_the_game()]

    def get_winner(self) -> Player | None:
        result = None
        if self.have_winner():
            result = [player for player in self.players if player.total_cards() != 0][0]        
        return result

    def play(self):
        round = 0
        while self.have_winner() == False:
            print(f"round {round}")
            """
            I am too tired to write it now, but I want use a dict to
            collect the cards the player plays. The key is the index of the
            player and the value is the card.

            Another method will compare the cards and return the index of the
            winner.

            I then pass the list of cards to the winner.
            """

            round += 1

            
        print(f"The winner is {self.get_winner()}")

        
        


