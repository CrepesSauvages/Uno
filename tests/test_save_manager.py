import unittest
from unittest.mock import patch
from src.game.save_manager import SaveManager
from src.game.game_manager import GameManager

class TestSaveManager(unittest.TestCase):
    def setUp(self):
        self.save_manager = SaveManager()
        self.game = GameManager("facile")
        
    def test_save_achievements(self):
        # Débloquer un achievement
        self.game.game_stats['games_won'] = 1
        self.game.achievements.check_achievement('first_win', self.game.game_stats)
        
        # Sauvegarder
        self.game.save_current_game()
        
        # Charger la sauvegarde
        save_files = self.save_manager.list_saves()
        loaded_state = self.save_manager.load_game(save_files[-1])
        
        # Vérifier que les achievements sont sauvegardés
        self.assertIn('first_win', loaded_state['achievements'])
        
    def test_save_game_stats(self):
        # Modifier les stats
        self.game.game_stats.update({
            'cards_played': 10,
            'special_cards_played': 3,
            'max_cards_in_hand': 8
        })
        
        # Sauvegarder
        self.game.save_current_game()
        
        # Charger la sauvegarde
        save_files = self.save_manager.list_saves()
        loaded_state = self.save_manager.load_game(save_files[-1])
        
        # Vérifier que les stats sont correctement sauvegardées
        self.assertEqual(loaded_state['game_stats']['cards_played'], 10)
        self.assertEqual(loaded_state['game_stats']['special_cards_played'], 3)
        self.assertEqual(loaded_state['game_stats']['max_cards_in_hand'], 8) 