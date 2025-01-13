import unittest
from unittest.mock import patch
from src.ui.console_ui import ConsoleUI
from src.game.card import Card, Color, CardType
from src.game.player import Player

class TestConsoleUI(unittest.TestCase):
    def setUp(self):
        self.ui = ConsoleUI()
        self.test_card = Card(Color.RED, CardType.NUMBER, 5)
        self.test_player = Player("Test Player")

    @patch('builtins.input', return_value='1')
    def test_get_color_choice(self, mock_input):
        color = self.ui.get_color_choice()
        self.assertEqual(color, Color.RED)

    @patch('builtins.input', return_value='o')
    def test_ask_play_drawn_card(self, mock_input):
        result = self.ui.ask_play_drawn_card()
        self.assertTrue(result) 