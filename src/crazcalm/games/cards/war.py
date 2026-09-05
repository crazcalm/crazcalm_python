from crazcalm.cards import (
    TerminalDeck,
    TerminalCard,
    card_factory,
    Card,
)
from crazcalm.attributes import Name


class Player:

    NPC_PLAYER_COUNT = 1

    @classmethod
    def create_npcs(cls, num):
        return [Player.create_npc() for _ in range(num)]

    @classmethod
    def create_npc(cls):
        name = Name(name=f"NPC {cls.NPC_PLAYER_COUNT}")
        cls.NPC_PLAYER_COUNT += 1
        return cls(name=name)

    def __init__(self, name: Name):
        self.deck = TerminalDeck(cards=[])
        self.win_pile = TerminalDeck(cards=[])
        self._name = name

    @property
    def name(self):
        return self._name.name

    @property
    def id(self):
        return self._name.id

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

    def hand_winner(self, played_cards) -> list[str]:
        """
        Will return the player ids of the players with the best card.
        """
        pass

    def play(self):
        # WIP
        round = 0
        while self.have_winner() == False:
            print(f"round {round}")
            played_cards = {}
            for player in self.players:
                if not player.lose_the_game():
                    played_cards[player.id] = player.play_card()

            winners_of_hand = self.hand_winners(played_cards)
            if len(winners_of_hand) == 1:
                for player in self.players:
                    if player.am_I(winners_of_hand[0]):
                        # pass all the cards to the winner
                        player.add_cards_to_win_pile(played_cards.values())

            if len(winners_of_hand) > 1:
                # need to do i the clare war!
                pass

            round += 1

            
        print(f"The winner is {self.get_winner()}")

        
        


