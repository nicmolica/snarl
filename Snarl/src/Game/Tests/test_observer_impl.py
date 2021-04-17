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
        # Just to suppress some output
        o.render = lambda : 0
        gamestate = Mock()
        gamestate.render = lambda : [['X', 'X', 'X'], ['X', ' ', 'X'], ['X', 'X', 'X']]
        o.notify(gamestate)
        class MockStream:
            def write(self, text):
                self.text = text
        stream = MockStream()
        rendered = o._render_to_stream(stream)
        self.assertIsNotNone(stream.text)


if __name__ == '__main__':
    unittest.main()