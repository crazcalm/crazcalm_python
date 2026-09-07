from crazcalm.cards import (
    TerminalDeck,
    TerminalCard,
    card_factory,
    Card,
)
from crazcalm.attributes import Name

class PlayerException(Exception):
    pass

class PlayerNoCardsLeftException(PlayerException):
    pass


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

    def am_I(self, name: str):
        return self._name.am_I(name)

    def reset(self):
        self.deck = TerminalDeck(cards=[])
        self.win_pile = TerminalDeck(cards=[])

    def lose_the_game(self) -> bool:
        return False if self.total_cards() else True

    def _play_card(self) -> Card | None:
        result = None
        if self.deck.cards_left() > 0:
            result = self.deck.draw()
        elif self.win_pile.cards_left() > 0:
            while self.win_pile.cards_left() > 0:
                self.deck.put_on_bottom(self.win_pile.draw())
            result = self._play_card()
        return result

    def total_cards(self):
        return self.deck.cards_left() + self.win_pile.cards_left()

    def play_card(self) -> Card:
        result = self._play_card()
        if result is None:
            raise PlayerNoCardsLeftException()
        return result

    def play_war(self) -> list[Card]:
        result = []
        count = 4
        while count > 0:
            card = self.play_card()
            if not card.face_down:
                card.flip()

            result.append(card)

            if self.total_cards() == 0:
                # Flippin the last card face up
                result[-1].flip()
                break

            if count == 1:
                # Flippin the last card face up
                result[-1].flip()

            count -= 1
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
        deck = TerminalDeck.create_52_card_deck(card_class=TerminalCard)
        deck.shuffle()
        count = 0
        while deck.cards_left() > 0:
            index = count % len(self.players)
            self.players[index].add_card_to_deck(deck.draw())
            count += 1

    def have_winner(self) -> bool:
        return len(self.players) - 1 == len([player for player in self.players if player.lose_the_game()])

    def get_winner(self) -> Player | None:
        result = None
        if self.have_winner():
            result = [player for player in self.players if player.total_cards() != 0][0]        
        return result

    def hand_winner(self, played_cards: dict[str: Card]) -> list[str]:
        """
        Will return the player ids of the players with the best card.
        """
        result = []
        played = list(played_cards.items())
        played.sort(key=lambda item: item[1].rank.value, reverse=True)
        result.append(played[0])
        for (player_id, card) in played[1:]:
            if card.rank == result[0][1].rank:
                result.append((player_id, card))

        return [player_id for (player_id, _) in result]

    def play(self) -> Player:
        # WIP
        round = 0
        while self.have_winner() == False:
            cards_to_win = []
            print(f"round {round}")
            played_cards = {}
            for player in self.players:
                if not player.lose_the_game():
                    card = player.play_card()
                    played_cards[player.id] = card
                    cards_to_win.append(card)
            winners_of_hand = self.hand_winner(played_cards)
            while len(winners_of_hand) > 1:
                played_cards = {}
                winners = []
                for player_id in winners_of_hand:
                    for player in self.players:
                        if player.am_I(player_id):
                            winners.append(player)
                
                for player in winners:
                    if not player.lose_the_game():
                        cards = player.play_war()
                        played_cards[player.id] = cards[-1]
                        cards_to_win += cards
                    if len(played_cards.keys()) > 1:
                        winners_of_hand = self.hand_winner(played_cards)
                    elif len(played_cards.keys()) == 1:
                        winners_of_hand = played_cards.keys()
                    else:
                        print("I am not sure what to do in this case...")


            if len(winners_of_hand) == 1:
                for player in self.players:
                    if player.am_I(winners_of_hand[0]):
                        # pass all the cards to the winner
                        player.add_cards_to_win_pile(cards_to_win)        
            round += 1
        winner = self.get_winner()          
        print(f"The winner is {winner}")
        return winner

        
        


