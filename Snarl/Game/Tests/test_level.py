import sys
sys.path.append('../')
import unittest
from level import Level, Room, Hallway, Posn

class TestLevel(unittest.TestCase):
    def test_rooms_field_rejects_nonrooms(self):
        with self.assertRaises(TypeError):
            Level(["I am not a room", "I am not a room either"], [Hallway([], Posn(1, 0), Posn(10, 0))])
    
    def test_hallways_field_rejects_nonhallways(self):
        with self.assertRaises(TypeError):
            Level([], ["I am not a hallway", "I am not a hallway either"])

    def test_rejects_overlapping_rooms(self):
        room1 = Room(Posn(0, 0), 10, 10, [], [Posn(3, 10), Posn(10, 5)])
        room2 = Room(Posn(9, 9), 10, 10, [], [Posn(9, 9), Posn(19, 19)])
        with self.assertRaises(ValueError):
            Level([room1, room2], [])

    def test_rejects_overlapping_hallways(self):
        hallway1 = Hallway([], Posn(0, 5), Posn(10, 5))
        hallway2 = Hallway([], Posn(5, 10), Posn(5, 0))
        with self.assertRaises(ValueError):
            Level([], [hallway1, hallway2])
    
    def test_rejects_overlapping_room_and_hallway(self):
        room = Room(Posn(0, 0), 10, 10, [], [Posn(3, 10), Posn(10, 5)])
        hallway = Hallway([], Posn(0, 5), Posn(10, 5))
        with self.assertRaises(ValueError):
            Level([room], [hallway])

    def test_rejects_disconnected_hallway(self):
        hallway = Hallway([], Posn(0, 5), Posn(10, 5))
        Level([], [hallway])
        with self.assertRaises(ValueError):
            Level([], [hallway])

    def test_any_overlaps_accepts_valid_level(self):
        room1 = Room(Posn(0, 0), 10, 10, [], [Posn(3, 10), Posn(10, 5)])
        hallway1 = Hallway([], Posn(3, 10), Posn(3, 20))
        room2 = Room(Posn(0, 20), 10, 10, [], [Posn(3, 20)])
        hallway2 = Hallway([Posn(12, 5), Posn(12, 2), Posn(15, 2)], Posn(10, 5), Posn(18, 2))
        room3 = Room(Posn(18, 0), 5, 5, [], [Posn(18, 2)])
        Level([room1, room2, room3], [hallway1, hallway2])

if __name__ == '__main__':
    unittest.main()