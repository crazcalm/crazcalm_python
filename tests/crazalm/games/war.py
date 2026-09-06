import unittest
from collections import namedtuple

from crazcalm.attributes import Name
from crazcalm.games.cards.war import (
    Player,
    PlayerNoCardsLeftException,
    Game,
)
from crazcalm.cards import (
    Deck,
    Card,
    Rank,
    Suit,
)


class TestWarGame(unittest.TestCase):
    def setUp(self):
        self.players = Player.create_npcs(3)
        self.game = Game(players=self.players)
        self.deck = Deck.create_52_card_deck()

    def test_setup(self):
        expected = [18, 17, 17]
        self.game.set_up_game()

        self.assertListEqual(
            [player.total_cards() for player in self.game.players],
            expected,
        )

    def test_have_winner(self):
        self.assertFalse(self.game.have_winner())
        self.game.players[0].add_cards_to_win_pile([self.deck.draw()])
        self.assertTrue(self.game.have_winner())
        self.game.players[1].add_cards_to_win_pile([self.deck.draw()])
        self.assertFalse(self.game.have_winner())

    def test_get_winner(self):
        self.assertIsNone(self.game.get_winner())
        self.game.players[1].add_cards_to_win_pile([self.deck.draw()])
        winner = self.game.get_winner()
        self.assertEqual(self.game.players[1].id, winner.id)

    def test_hand_winner(self):
        Case = namedtuple("Case", ["hands", "expected"])
        cases = [
            Case(
                {
                    "1": Card(rank=Rank.ACE, suit=Suit.CLUBS),
                    "2": Card(rank=Rank.TWO, suit=Suit.HEARTS),
                    "3": Card(rank=Rank.TEN, suit=Suit.DIAMONDS),
                },
                ["3"],
            ),
            Case(
                {
                    "1": Card(rank=Rank.ACE, suit=Suit.CLUBS),
                    "2": Card(rank=Rank.TWO, suit=Suit.HEARTS),
                    "3": Card(rank=Rank.TEN, suit=Suit.DIAMONDS),
                    "4": Card(rank=Rank.TEN, suit=Suit.SPADES),
                },
                ["3", "4"],
            ),

        ]

        for num, case in enumerate(cases, start=1):
            with self.subTest(f"Case {num}:"):
                breakpoint()
                result = self.game.hand_winner(case.hands)
                self.assertListEqual(result, case.expected)

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.name = Name("Noname")
        self.deck = Deck.create_52_card_deck()
        self.player = Player(name=self.name)

    def test_generate_npcs(self):
        expected = ['NPC 1', 'NPC 2', 'NPC 3', 'NPC 4', 'NPC 5']
        players = Player.create_npcs(5)

        self.assertListEqual(
            [player.name for player in players],
            expected,
        )

    def test_id(self):
        player = Player(self.name)

        self.assertEqual(player.id, player.id)

    def test_lose_to_game(self):
        self.assertEqual(self.player.total_cards(), 0)
        self.assertTrue(self.player.lose_the_game())

        card_1 = self.deck.draw()
        self.player.add_cards_to_win_pile(cards=[card_1, card_1, card_1])
        self.assertFalse(self.player.lose_the_game())

    def test_play_card(self):
        card_1 = self.deck.draw()
        card_2 = self.deck.draw()

        self.player.add_cards_to_win_pile([card_1, card_2])

        self.assertEqual(card_1, self.player.play_card())
        self.assertEqual(card_2, self.player.play_card())

        with self.assertRaises(PlayerNoCardsLeftException):
            self.player.play_card()

    def test_total_left(self):
        self.assertEqual(self.player.total_cards(), 0)
        self.player.add_card_to_deck(self.deck.draw())
        self.assertEqual(self.player.total_cards(), 1)
        self.player.add_cards_to_win_pile([self.deck.draw()])
        self.assertEqual(self.player.total_cards(), 2)

    def test_play_war(self):
        expected_war_1 = [True, True, True, False]
        expected_war_2 = [True, True, False]
        cards = [self.deck.draw() for _ in range(7)]
        self.player.add_cards_to_win_pile(cards)

        war_1 = self.player.play_war()
        war_2 = self.player.play_war()

        self.assertListEqual(
            [x.face_down for x in war_1],
            expected_war_1
        )
        self.assertListEqual(
            [x.face_down for x in war_2],
            expected_war_2,
        )

if __name__ == "__main__":
    unittest.main()