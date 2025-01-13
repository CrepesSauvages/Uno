import unittest
from unittest.mock import Mock, patch
from src.game.achievements import Achievements
from src.game.game_manager import GameManager
from src.ui.console_ui import ConsoleUI
from src.game.card import Card, Color, CardType
from src.game.player import Player

class TestAchievements(unittest.TestCase):
    def setUp(self):
        self.game = GameManager("facile")
        # Créer un mock plus complet pour ConsoleUI
        self.ui_mock = Mock(spec=ConsoleUI)
        self.ui_mock.display_achievement = Mock()
        self.game.ui = self.ui_mock
        
        # Initialiser les achievements
        self.achievements = self.game.achievements
        
        # Créer un joueur de test avec des cartes
        self.test_player = Player("Test Player")
        self.test_player.hand = [
            Card(Color.RED, CardType.NUMBER, 1),
            Card(Color.BLUE, CardType.SKIP)
        ]
        self.game.players[0] = self.test_player
        
    def tearDown(self):
        # Réinitialiser les achievements après chaque test
        self.achievements.unlocked.clear()
        
    def test_first_win_achievement(self):
        # Simuler la première victoire
        self.game.game_stats['games_won'] = 1
        
        # Vérifier que l'achievement est débloqué
        self.assertTrue(
            self.achievements.check_achievement('first_win', self.game.game_stats)
        )
        
        # Vérifier qu'il ne peut pas être débloqué deux fois
        self.assertFalse(
            self.achievements.check_achievement('first_win', self.game.game_stats)
        )
        
    def test_perfect_game_achievement(self):
        # Simuler une partie sans pioche
        self.game.game_stats['cards_drawn'] = 0
        
        self.assertTrue(
            self.achievements.check_achievement('perfect_game', self.game.game_stats)
        )
        
        # Simuler une partie avec pioche
        self.game.game_stats['cards_drawn'] = 1
        
        # Réinitialiser les achievements pour le test
        self.achievements.unlocked.clear()
        self.assertFalse(
            self.achievements.check_achievement('perfect_game', self.game.game_stats)
        )
        
    def test_special_master_achievement(self):
        # Ajouter des cartes spéciales à la main du joueur
        special_card = Card(Color.RED, CardType.SKIP)
        self.test_player.hand.append(special_card)
        
        # Simuler directement l'état des statistiques
        self.game.game_stats['special_cards_played'] = 5
        
        # Vérifier l'achievement
        self.assertTrue(
            self.achievements.check_achievement('special_master', self.game.game_stats)
        )
        
    def test_comeback_achievement(self):
        # Simuler une grande main
        self.game.game_stats['max_cards_in_hand'] = 11
        
        # Vérifier directement avec les conditions
        achievement_unlocked = self.achievements._conditions_met('comeback', self.game.game_stats)
        self.assertTrue(achievement_unlocked)
        
        # Réinitialiser et tester avec une petite main
        self.game.game_stats['max_cards_in_hand'] = 5
        achievement_unlocked = self.achievements._conditions_met('comeback', self.game.game_stats)
        self.assertFalse(achievement_unlocked)
        
    def test_achievement_display(self):
        # Simuler le débloquage d'un achievement
        self.game.game_stats['games_won'] = 1
        self.game._check_achievements(self.test_player)
        
        # Vérifier que la méthode d'affichage a été appelée au moins une fois
        self.ui_mock.display_achievement.assert_called()
        
    def test_multiple_achievements(self):
        # Simuler une situation où plusieurs achievements peuvent être débloqués
        self.game.game_stats.update({
            'games_won': 1,
            'cards_drawn': 0,
            'special_cards_played': 5,
            'max_cards_in_hand': 10
        })
        
        # Vérifier les achievements
        self.game._check_achievements(self.test_player)
        
        # Vérifier que la méthode d'affichage a été appelée
        self.assertTrue(self.ui_mock.display_achievement.called) 