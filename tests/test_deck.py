import unittest
from src.game.deck import Deck

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        
    def test_deck_initialization(self):
        # Le deck doit contenir 108 cartes au total
        self.assertEqual(len(self.deck.cards), 108)
        
    def test_draw_card(self):
        initial_count = len(self.deck.cards)
        card = self.deck.draw_card()
        
        self.assertIsNotNone(card)
        self.assertEqual(len(self.deck.cards), initial_count - 1)
        
    def test_reshuffle_discard_pile(self):
        # Vider le deck
        while self.deck.cards:
            self.deck.discard_pile.append(self.deck.draw_card())
            
        # Tester le remélange
        self.deck._reshuffle_discard_pile()
        self.assertGreater(len(self.deck.cards), 0) 