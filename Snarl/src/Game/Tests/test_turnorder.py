import sys
import unittest
from Snarl.src.Game.turnorder import Turnorder

class TestTurnorder(unittest.TestCase):
    def test_turnorder_inits_to_first_item(self):
        t = Turnorder([1, 2, 3, 4])
        self.assertEqual(t.next(), 1)
    
    def test_turnorder_preserves_order(self):
        t = Turnorder([1, 2, 3, 4])
        self.assertEqual(t.next(), 1)
        self.assertEqual(t.next(), 2)
        self.assertEqual(t.next(), 3)
        self.assertEqual(t.next(), 4)
    
    def test_turnorder_is_cyclic(self):
        l = [1, 2, 3, 4]
        t = Turnorder(l)
        for it in l:
            t.next()
        self.assertEqual(t.next(), 1)

    def test_add_without_pos_adds_at_end(self):
        l = [1, 2, 3, 4]
        t = Turnorder(l)
        t.add(5)
        self.assertEqual(t.order[-1], 5)

    def test_add_with_pos_adds_at_pos(self):
        l = [1, 2, 3, 4]
        t = Turnorder(l)
        t.add(5, 0)
        self.assertEqual(t.order[0], 5)

    def test_add_with_pos_raises_error_on_invalid_pos(self):
        with self.assertRaises(ValueError):
            l = [1, 2, 3, 4]
            t = Turnorder(l)
            t.add(5, -190)

    def test_add_at_next_changes_next(self):
        l = [1, 2, 3, 4]
        t = Turnorder(l)
        t.add(5, 0)
        self.assertEqual(t.next(), 5)

    def test_add_before_next_does_not_change_next(self):
        l = [1, 2, 3, 4]
        t = Turnorder(l)
        t.next() # 1
        t.next() # 2
        t.add(5, 0)
        self.assertEqual(t.next(), 3)

    def test_add_after_next_does_not_change_next(self):
        l = [1, 2, 3, 4]
        t = Turnorder(l)
        t.add(5, 1)
        self.assertEqual(t.next(), 1)

    def test_eject_at_next_changes_next(self):
        l = [1, 2, 3, 4]
        t = Turnorder(l)
        t.eject(1)
        self.assertEqual(t.next(), 2)

    def test_eject_after_next_does_not_change_next(self):
        l = [1, 2, 3, 4]
        t = Turnorder(l)
        t.eject(2)
        self.assertEqual(t.next(), 1)

    def test_eject_with_nonexistent_item_raises_error(self):
        with self.assertRaises(RuntimeError):
            l = [1, 2, 3, 4]
            t = Turnorder(l)
            t.eject(20000)

    def test_eject_before_next_does_not_change_next(self):
        l = [1, 2, 3, 4]
        t = Turnorder(l)
        t.next() # next is 2
        t.next() # next is 3
        t.eject(1) # next should still be 3
        self.assertEqual(t.next(), 3)

    def test_next_raises_error_when_order_empty(self):
        with self.assertRaises(RuntimeError):
            t = Turnorder([])
            t.next()

    def test_decrement_fails_when_order_empty(self):
        with self.assertRaises(RuntimeError):
            t = Turnorder([])
            t._decrement()
    
    def test_decrement_goes_to_previous_turn(self):
        l = [1, 2, 3]
        t = Turnorder(l)
        t.next()
        t._decrement()
        self.assertEqual(t.next(), 1)


if __name__ == '__main__':
    unittest.main()