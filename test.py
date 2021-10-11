from dirt import Dirt, DirtPair
from map import Map
import unittest


class TestMap0(unittest.TestCase):
    def setUp(self):
        with open('maps/b0') as f:
            lines = f.readlines()
            self.m = Map(lines[1:])
            self.m.calculate_dirt_paths()

    def test_dirt_loc(self):
        goal = [Dirt(0, 3, 1), Dirt(1, 1, 3), Dirt(2, 2, 3)]
        self.assertCountEqual(self.m.dirt_locations, goal)

    def test_dirt_paths(self):
        goal = [DirtPair(1, 2, 4), DirtPair(1, 3, 3), DirtPair(2, 3, 1)]
        self.assertCountEqual(self.m.dirt_paths, goal)


if __name__ == '__main__':
    unittest.main()
