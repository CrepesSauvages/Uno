from typing import List
import random
from .card import Card, Color, CardType

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.discard_pile: List[Card] = []
        self._initialize_deck()
        
    def _initialize_deck(self):
        # Cartes numériques (0-9)
        for color in [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]:
            # Un seul 0 par couleur
            self.cards.append(Card(color, CardType.NUMBER, 0))
            # Deux cartes de chaque numéro 1-9
            for value in range(1, 10):
                self.cards.extend([Card(color, CardType.NUMBER, value)] * 2)
            
            # Cartes spéciales (2 de chaque par couleur)
            special_cards = [
                Card(color, CardType.SKIP),
                Card(color, CardType.REVERSE),
                Card(color, CardType.DRAW_TWO)
            ]
            self.cards.extend(special_cards * 2)
        
        # Cartes noires (4 +4 et 4 Jokers)
        black_cards = [
            Card(Color.BLACK, CardType.WILD),
            Card(Color.BLACK, CardType.WILD_DRAW_FOUR)
        ]
        self.cards.extend(black_cards * 4)
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def draw_card(self) -> Card:
        if not self.cards:
            self._reshuffle_discard_pile()
        return self.cards.pop() if self.cards else None
        
    def _reshuffle_discard_pile(self):
        if not self.discard_pile:
            return
        top_card = self.discard_pile.pop()
        self.cards = self.discard_pile
        self.discard_pile = [top_card]
        self.shuffle()
