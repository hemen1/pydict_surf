import unittest
from pydict_surf.dict_walk import DictWalk
import json


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        with open('template.json', 'r') as f:
            walks = DictWalker(json.load(f))
        it1 = walks.walk()
        self.assertEqual(next(it1), ([], [], [], [], ""))
        self.assertEqual(next(it1), ([], [], [], [], ""))
        self.assertEqual(next(it1), ([], [], [], [], ""))



if __name__ == '__main__':
    unittest.main()
