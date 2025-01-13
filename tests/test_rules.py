import unittest
from unittest.mock import Mock
from src.game.rules import Rules
from src.game.card import Card, Color, CardType
from src.game.game_manager import GameManager
from src.ui.console_ui import ConsoleUI

class TestRules(unittest.TestCase):
    def setUp(self):
        self.game = GameManager("facile")
        self.game.ui = Mock(spec=ConsoleUI)  # Mock UI
        self.game.start_game()
        
    def test_skip_card_effect(self):
        initial_player = self.game.current_player_index
        skip_card = Card(Color.RED, CardType.SKIP)
        
        # La carte SKIP fait passer le tour une fois dans Rules.apply_card_effect
        # et une autre fois dans GameManager._play_card
        # Donc on ne doit tester que l'effet dans Rules
        Rules.apply_card_effect(skip_card, self.game)
        
        # Le joueur suivant (+1) est sauté, donc on passe au joueur d'après (+1)
        expected_player = (initial_player + 1) % len(self.game.players)
        self.assertEqual(self.game.current_player_index, expected_player)
        
    def test_draw_two_effect(self):
        next_player_index = (self.game.current_player_index + 1) % len(self.game.players)
        next_player = self.game.players[next_player_index]
        initial_cards = len(next_player.hand)
        
        draw_two = Card(Color.RED, CardType.DRAW_TWO)
        Rules.apply_card_effect(draw_two, self.game)
        
        self.assertEqual(len(next_player.hand), initial_cards + 2) 