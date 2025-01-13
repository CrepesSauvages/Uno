from typing import List
from .card import Card, CardType, Color

class AIStrategy:
    @staticmethod
    def choose_card(difficulty: str, hand: List[Card], top_card: Card, 
                   other_players_cards: dict) -> Card:
        if difficulty == "facile":
            return AIStrategy._easy_strategy(hand, top_card)
        elif difficulty == "moyen":
            return AIStrategy._medium_strategy(hand, top_card)
        else:
            return AIStrategy._hard_strategy(hand, top_card, other_players_cards)
            
    @staticmethod
    def _easy_strategy(hand: List[Card], top_card: Card) -> Card:
        playable = [c for c in hand if c.can_be_played_on(top_card)]
        return playable[0] if playable else None
        
    @staticmethod
    def _medium_strategy(hand: List[Card], top_card: Card) -> Card:
        playable = [c for c in hand if c.can_be_played_on(top_card)]
        if not playable:
            return None
            
        # Priorité aux cartes de même couleur
        same_color = [c for c in playable if c.color == top_card.color]
        if same_color:
            return same_color[0]
            
        return playable[0]
        
    @staticmethod
    def _hard_strategy(hand: List[Card], top_card: Card, 
                      other_players_cards: dict) -> Card:
        playable = [c for c in hand if c.can_be_played_on(top_card)]
        if not playable:
            return None
            
        # Trouver le joueur avec le moins de cartes
        min_cards_player = min(other_players_cards.items(), 
                             key=lambda x: x[1])[0]
        
        # Si un joueur est proche de gagner, priorité aux cartes d'action
        if min(other_players_cards.values()) <= 2:
            action_cards = [c for c in playable 
                          if c.card_type != CardType.NUMBER]
            if action_cards:
                return action_cards[0]
                
        # Sinon, stratégie normale
        return AIStrategy._medium_strategy(hand, top_card) 