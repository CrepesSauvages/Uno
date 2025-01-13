import unittest
from unittest.mock import Mock
from src.game.game_manager import GameManager
from src.ui.console_ui import ConsoleUI

class TestGameManager(unittest.TestCase):
    def setUp(self):
        self.game = GameManager("facile")
        # Mock de ConsoleUI pour éviter les interactions console
        self.game.ui = Mock(spec=ConsoleUI)
        
    def test_game_initialization(self):
        self.assertEqual(len(self.game.players), 4)
        self.assertEqual(self.game.direction, 1)
        self.assertEqual(self.game.current_player_index, 0)
        
    def test_start_game(self):
        self.game.start_game()
        
        # Vérifier que chaque joueur a 7 cartes
        for player in self.game.players:
            self.assertEqual(len(player.hand), 7)
            
        # Vérifier qu'une carte est sur la pile
        self.assertEqual(len(self.game.deck.discard_pile), 1)
        
    def test_direction_change(self):
        initial_direction = self.game.direction
        self.game.direction *= -1
        self.assertEqual(self.game.direction, -initial_direction)
