import unittest
import random


from crazcalm.attributes import Name
from crazcalm.games.cards.war import (
    Player,
)
from crazcalm.cards import Deck


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




if __name__ == "__main__":
    unittest.main()