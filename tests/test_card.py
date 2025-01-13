import unittest
from src.game.card import Card, Color, CardType

class TestCard(unittest.TestCase):
    def setUp(self):
        self.number_card = Card(Color.RED, CardType.NUMBER, 5)
        self.special_card = Card(Color.BLUE, CardType.SKIP)
        self.wild_card = Card(Color.BLACK, CardType.WILD)
        
    def test_card_creation(self):
        self.assertEqual(self.number_card.color, Color.RED)
        self.assertEqual(self.number_card.value, 5)
        
    def test_can_be_played_on(self):
        # Test même couleur
        same_color = Card(Color.RED, CardType.NUMBER, 7)
        self.assertTrue(same_color.can_be_played_on(self.number_card))
        
        # Test même numéro
        same_number = Card(Color.BLUE, CardType.NUMBER, 5)
        self.assertTrue(same_number.can_be_played_on(self.number_card))
        
        # Test carte noire
        self.assertTrue(self.wild_card.can_be_played_on(self.number_card))
