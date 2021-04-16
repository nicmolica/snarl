from Snarl.src.Game.observer_impl import Observer
import unittest
from unittest.mock import Mock

class TestObserverImpl(unittest.TestCase):
    def test_inits_to_no_gamestate(self):
        o = Observer()
        self.assertIsNone(o.gamestate)

    def test_inits_to_no_ip(self):
        o = Observer()
        self.assertFalse(o.ip)
    
    def test_notify_sets_gamestate(self):
        o = Observer()
        gamestate = Mock()
        gamestate.render = lambda : [['X', 'X', 'X'], ['X', ' ', 'X'], ['X', 'X', 'X']]
        o.notify(gamestate)
        class MockStream:
            def write(self, text):
                self.text = text
        stream = MockStream()
        rendered = o._render_to_stream(stream)
        self.assertEqual(stream.text, "X   X   X\nX       X\nX   X   X")


if __name__ == '__main__':
    unittest.main()