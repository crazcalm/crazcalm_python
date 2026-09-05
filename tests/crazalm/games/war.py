import unittest
import random


from crazcalm.attributes import Name
from crazcalm.games.cards.war import (
    Player,
)


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.name = Name("Noname")

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
    


if __name__ == "__main__":
    unittest.main()