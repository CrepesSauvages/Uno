from typing import List
from .card import Card

class Player:
    def __init__(self, name: str, is_ai: bool = False):
        self.name = name
        self.hand: List[Card] = []
        self.is_ai = is_ai
        
    def add_card(self, card: Card):
        self.hand.append(card)
        
    def remove_card(self, card: Card):
        self.hand.remove(card)
        
    def has_playable_card(self, top_card: Card) -> bool:
        return any(card.can_be_played_on(top_card) for card in self.hand)
