import unittest
import random
from collections import namedtuple

from crazcalm.attributes import Name


class TestName(unittest.TestCase):
    def setUp(self):
        self.name = "Marcus"
        self.aliases = ["Crazcalm"]
        self.prefered_name = "Marcus the Great"

    def test_am_I(self):
        Case = namedtuple("Case", ["name", "expected"])
        cases = [
            Case("Crazcalm", True),
            Case("Marcus the Great", True),
            Case("Marcus", True),
            Case("MARCUS", False),
        ]

        name = Name(name=self.name, aliases=self.aliases, prefered_name=self.prefered_name)

        for num, case in enumerate(cases, start=1):
            with self.subTest(f"case {num}: "):
                self.assertEqual(name.am_I(case.name), case.expected)

    def test_who_am_i(self):
        random.seed(42)
        expected_names = [
            'Crazcalm',
            'Marcus the Great',
            'Marcus',
            'Marcus the Great-1043321819',
        ]

        name = Name(name=self.name, aliases=self.aliases, prefered_name=self.prefered_name)

        self.assertListEqual(name.who_am_I(), expected_names)

    def test_id(self):
        expected_id = "Marcus-1043321819"
        expected_id_2 = "Marcus the Great-6001338908"

        random.seed(42)
        name = Name(name=self.name)

        # make sure it doesn't change when called multiple times
        self.assertEqual(expected_id, name.id)
        self.assertEqual(expected_id, name.id)

        with self.assertRaises(AttributeError):
            name.id = "hi"

        name_2 = Name(name=self.name, prefered_name=self.prefered_name)
        self.assertEqual(expected_id_2, name_2.id)


if __name__ == "__main__":
    unittest.main()